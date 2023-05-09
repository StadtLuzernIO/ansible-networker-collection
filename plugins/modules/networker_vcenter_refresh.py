#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:  Stadt Luzern, Zentrale Informatikdienste
# Contact: https://github.com/stadtluzernio
# License: The Unlicense, see LICENSE file.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: networker_vcenter_refresh
author:
  - Stadt Luzern, Zentrale Informatikdienste
requirements: []
notes:
version_added: 0.0.1
short_description: Refresh all vcenters configured in networker.
description:
  - This module can be used to refresh the networker information for all the vcenters.
  - Mainly used, when adding a vm to vcenter and want to immediately add the same vm to a protection group.
extends_documentation_fragment:
  - stadtluzernio.networker.networker_api_connect
options:
    wait_for:
        description: Seconds to wait for vcenter refresh before proceed.
        type: int
        required: false
'''

EXAMPLES = '''
---
- name: Refresh vCenter
  stadtluzernio.networker.networker_vcenter_refresh:
    hostname: https://networker.company.com:9090
    username: api
    password: mySuperSecretPassword
    wait_for: 10
  delegate_to: localhost
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.stadtluzernio.networker.plugins.module_utils import networker_errors, networker_api
from ansible.module_utils.common.text.converters import to_native
import os

def main():
    result = {"json": {}, "changed": False}
    changed = False

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        hostname            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_HOSTNAME'])),
        username            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_USERNAME'])),
        password            = dict(type='str', required=False, fallback=(env_fallback, ['NETWORKER_PASSWORD']), no_log=True),
        validate_certs      = dict(type='bool', required=False, default=True),
        wait_for            = dict(type='int', required=False),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        api_client = networker_api.create_client(module)
        api_client.refresh_vcenters(module.params.get("wait_for"))
        result.update({"changed": bool(changed)})
    except networker_errors.Error as e:
        result.update({"msg": to_native(e)})
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()