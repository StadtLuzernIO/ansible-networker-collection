from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment:

    DOCUMENTATION = r'''
    options:
        hostname:
            description: Networker rest api url. You also can set the environment variable NETWORKER_HOSTNAME as hostname.
            type: str
            required: true
        username:
            description: Networker username for api access. You also can set the environment variable NETWORKER_USER as username.
            type: str
            required: false
        password:
            description: Password for the Networker username for api access. You also can set the environment variable NETWORKER_PASSWORD as password.
            type: str
            required: false
        validate_certs:
            description: Enable or disable certificate check for api access.
            type: bool
            default: true
    '''