#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:  Stadt Luzern, Zentrale Informatikdienste
# Contact: https://github.com/stadtluzernio
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: networker_vcenter_vm
author:
  - Stadt Luzern, Zentrale Informatikdienste
requirements: []
notes:
version_added: 0.0.1
short_description: Add or remove a vcenter virtual machine from a networker protection group.
description:
  - Add an exisiting vm from vcenter to networker protection group.
  - Remove an existing or non existing vm in vcenter from a networker protection group
  - You may provide multiple vm names for the same protection group.
extends_documentation_fragment:
  - stadtluzernio.networker.networker_api_connect
options:
    vcenter:
        description: FQDN of networker integrated vcenter.
        type: str
        required: true
    vm_names:
        description: A list of virtual machines names. Use the same names as in vcenter.
        type: list
        required: true
    protection_group:
        description: Name of an existing protection group in networker.
        type: str
        required: true
    state:
        description: Specifies the desired state of the VM in the protection group.
        type: str
        default: present
        choices: [ present, absent ]

'''

EXAMPLES = '''
---
- name: Add a vm to a specific networker protection group
  stadtluzernio.networker.networker_vcenter_vm:
    hostname: https://networker.company.com:9090
    username: api
    password: mySuperSecretPassword
    vcenter: vcenter.company.com
    vm_names:
    - demo01
    protection_group: gold
    state: present
- name: Remove a vm from a specific networker protection group
  stadtluzernio.networker.networker_vcenter_vm:
    hostname: https://networker.company.com:9090
    username: api
    password: mySuperSecretPassword
    vcenter: vcenter.company.com
    vm_names:
    - demo01
    protection_group: gold
    state: absent
'''

RETURN = '''
uuids:
    description: A list of UUIDs for the VMs that were added or removed from the protection group.
    returned: always
    type: list
    sample: ["eb6200e2-b8d7-423c-5789-039bf6f52a81"]
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.stadtluzernio.networker.plugins.module_utils import networker_errors, networker_api
from ansible.module_utils.common.text.converters import to_native

def main():
    result = {"json": {}, "changed": False}
    changed = False

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hostname            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_HOSTNAME'])),
        username            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_USERNAME'])),
        password            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_PASSWORD']), no_log=True),
        vcenter             = dict(type='str', required=True),
        vm_names            = dict(type='list', required=True),
        protection_group    = dict(type='str', required=True),
        validate_certs      = dict(type='bool', required=False, default=True),
        state               = dict(type='str', required=False, default='present'),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    try:
        api_client = networker_api.create_client(module)
        if module.params.get("state") == 'present':
            action = 'add'
        else:
            action = 'remove'

        api_response            = {}    
        api_response            = api_client.update_vm_protectiongroup(module.params.get("vm_names"), action, module.params.get("protection_group"), module.params.get("vcenter"))
        changed                 = True if api_response['uuids'] is not None else False

        result.update({"json": api_response, "changed": bool(changed)})
    except networker_errors.Error as e:
        result.update({"msg": to_native(e)})
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()