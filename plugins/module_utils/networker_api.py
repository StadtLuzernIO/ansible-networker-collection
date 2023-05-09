# Author:  Stadt Luzern, Zentrale Informatikdienste
# Contact: https://github.com/stadtluzernio
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import sys
import time

from urllib.error import HTTPError
from ansible.module_utils.urls import basic_auth_header,fetch_url
from ansible.module_utils.six.moves.urllib.parse import urlencode, quote, urlunparse, urlparse
from ansible_collections.stadtluzernio.networker.plugins.module_utils import networker_errors

def create_client(module):
    if not module.params.get("username") or not module.params.get("password") or not module.params.get("hostname"):
        raise networker_errors.AccessDeniedError(message="Username, password or hostname not defined")
  
    return networker(
        hostname=module.params["hostname"],
        username=module.params["username"],
        password=module.params["password"],
        module=module
    )

class networker:
    API_VERSION = "v3"
    API_BASE_PATH = "nwrestapi"

    def __init__(self, hostname, username, password, module):
        self.hostname = hostname
        self.username = username
        self.password = password
        self._module = module

    def _send_request(self, path, method="GET", data=None, params=None, headers=None):
        fetch_kwargs = {
            "url": build_endpoint(self.hostname, path, params=params, api_base_path=None, api_version=None),
            "method": method,
            "headers": self._build_headers(headers),
        }

        if method.upper() in ["POST", "PUT", "PATCH"] and data != None:
            fetch_kwargs["data"] = self._module.jsonify(data)

        resp, info = fetch_url(self._module, **fetch_kwargs)

        if info.get("status") == 200:
            try:
                resp_body = json.loads(resp.read().decode("utf-8"))
            except (AttributeError, ValueError):

                msg = "Server returned error with invalid JSON: {err}".format(
                    err=info.get("msg", "<Undefined error>")
                )
                self._module.fail_json(msg=msg)
        elif info.get("status") in [201,204]:
            resp_body = None
        else:
            raise_for_error(info)

        return resp_body

    def _build_headers(self, headers=None):
        fetch_kwargs = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": basic_auth_header(self.username, self.password),
        }

        if headers != None:
            for enty in headers:
                fetch_kwargs[enty] = headers[enty]

        return fetch_kwargs

    def refresh_vcenters(self, wait_for):
        path = f"/global/vmware/op/refreshvcenters"
        refresh_vcenters = self._send_request(path, method="POST")

        if wait_for:
            time.sleep(wait_for) # wait for vcenters to refresh

        return refresh_vcenters

    def get_vm_uuid(self, vm_names, action):
        path = "/global/vmware/vms?fl=name,uuid"
        networker_all_vms = self._send_request(path, method="GET")

        networker_all_vms_dict = {}
        for vm in networker_all_vms['vms']:
            networker_all_vms_dict[vm['name']] = vm['uuid']

        vm_uuid = []

        for vm_name in vm_names:
            try:
                vm_uuid.append(networker_all_vms_dict[vm_name]) 
            except:
                if action != 'remove':
                    raise networker_errors.NotFoundError(
                        message= f"VM {vm_name} not found in Networker"
                    )

        return vm_uuid

    def get_vms_from_protection_group(self, protection_group):
        path = f"/global/protectiongroups/{protection_group}"
        protection_group = self._send_request(path, method="GET")

        return protection_group['vmwareWorkItemSelection']['vmUuids']

    def update_vm_protectiongroup(self, vm_names, action, protection_group, vcenter):
        path = f"/global/protectiongroups/{protection_group}/op/updatevmwareworkitems"

        vms_uuid_cleaned = []

        result = {}
        result['uuids'] = None

        vms_uuid = self.get_vm_uuid(vm_names, action)
        vms_uuid_protection_group = self.get_vms_from_protection_group(protection_group)

        for uuid in vms_uuid:
            if uuid not in vms_uuid_protection_group and action == 'add':
                vms_uuid_cleaned.append(uuid)
            elif uuid in vms_uuid_protection_group and action == 'delete':
                vms_uuid_cleaned.append(uuid)

        if vms_uuid_cleaned:
            data = {
                action+"WorkItems": {
                    "vCenterHostname": vcenter,
                    "vmUuids": vms_uuid_cleaned,
                }
            }
            print("heeeeeeeeeeeeeeereee")
            print(data)
            self._send_request(path, method="POST", data=data)
            
            result['uuids'] = vms_uuid_cleaned
        
        return result
        

def build_endpoint(hostname, path, params=None, api_base_path=None, api_version=None):
    url_parts = list(urlparse(hostname))

    if not api_base_path:
        api_base_path = networker.API_BASE_PATH

    if not api_version:
        api_version = networker.API_VERSION

    url_parts[2] = "{api_base_path}/{api_version}/{path}".format(
        api_base_path=quote(api_base_path.strip('/')),
        api_version=api_version,
        path=path.strip('/')
    )

    if params:
        url_parts[4] = urlencode(params)
    return urlunparse(url_parts)

def raise_for_error(response_info):
    try:
        response_info_body = json.loads(response_info.get("body").decode("utf-8"))
        err_details = {
            "message": response_info_body.get("message"),
            "status_code": response_info_body.get("status")
        }
    except (AttributeError, ValueError):
        # `body` key not present if urllib throws an error ansible doesn't handle
        err_details = {
            "message": response_info.get("msg", "Error not defined"),
            "status_code": response_info.get("status")
        }

    print(err_details)

    # error handling
    if err_details["status_code"] >= 500:
        raise networker_errors.ServerError(**err_details)
    elif err_details["status_code"] == 404:
        raise networker_errors.NotFoundError(**err_details)
    elif err_details["status_code"] in [401, 403]:
        raise networker_errors.AccessDeniedError(**err_details)
    elif err_details["status_code"] == 400:
        raise networker_errors.BadRequestError(**err_details)
    else:
        raise networker_errors.APIError(**err_details)