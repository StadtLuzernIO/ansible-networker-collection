# Ansible Collection - stadtluzernio.networker

Networker collection to interact with DELL EMC Networker. Currently it is only supported to add or remove vCenter VM's from a Networker Protection Group.

## Table of Content
- [Requirements](#requirements)
- [Installation](#installation)
- [Module & Environment Variables](#module--environment-variables)
- [`networker_vcenter_refresh` Module](#networker_vcenter_refresh-module)
- [`networker_vcenter_vm` Module](#networker_vcenter_vm-module)
- [Testing](#testing)
- [About DELL EMC Networker](#about-dell-emc-networker)
- [About stadtluzern.io](#about-stadtluzernio)
- [License](#license)

### Requirements
- Python >= 3.9.0 (lower versions are not tested)
- Ansible Core >= 2.13.8 (lower versions are not tested)

## Installation
You can install the Ansible collection from [Ansible Galaxy](https://galaxy.ansible.com/stadtluzernio/networker):

```shell
ansible-galaxy collection install stadtluzernio.networker
```

## Module & Environment Variables
All modules support the following variable definitions. You may either explicitly define the value on the task or let Ansible fallback to an environment variable to use the same value across all tasks.

Environment variables are ignored if the module variable is defined for a task.

| Module Variable | Environment Variable | Description                                                             |
|----------------:|----------------------|-------------------------------------------------------------------------|
|      `username` | `NETWORKER_USERNAME` | Networker username for api access.                                      |
|      `password` | `NETWORKER_PASSWORD` | Password for the Networker username for api access.                     |

### `networker_vcenter_refresh` Module
For more Details use docs: `ansible-doc stadtluzernio.networker.networker_vcenter_refresh`
```
- name: Refresh vCenter
  stadtluzernio.networker.networker_vcenter_refresh:
    hostname: https://networker.company.com:9090
    username: api
    password: mySuperSecretPassword
    wait_for: 10
```

### `networker_vcenter_vm` Module
For more Details use docs: `ansible-doc ansible-doc stadtluzernio.networker.networker_vcenter_vm`
```
- name: Add a vm to a specific Networker Protection Group
  stadtluzernio.networker.networker_vcenter_vm:
    hostname: https://networker.company.com:9090
    username: api
    password: mySuperSecretPassword
    vcenter: vcenter.company.com
    vm_names:
    - demo01
    protection_group: gold
    state: present
```

## Testing
Use Python3.9 and the following commands to test the module localy. To beginn edit the `json` files in `docs/tests` with your values.

```shell
# build the collection and install it to your python directory
ansible-galaxy collection build --force
ansible-galaxy collection install stadtluzernio-networker-0.0.1.tar.gz --force -p ~/.local/lib/python3.9/site-packages/ansible_collections

# export credentials
export NETWORKER_USERNAME='api'
export NETWORKER_PASSWORD='mySuperSecretPassword'

# for module networker_vcenter_refresh
python3.9 plugins/modules/networker_vcenter_refresh.py docs/tests/networker_vcenter_refresh.json

# for module networker_vcenter_vm
python3.9 plugins/modules/networker_vcenter_vm.py docs/tests/networker_vcenter_vm.json
```

## About DELL EMC Networker
Dell NetWorker is unified backup and recovery software for the enterprise: deduplication, backup to disk and tape, snapshots, replication and NAS.
[More Informations](https://www.dell.com/en-us/dt/data-protection/data-protection-suite/networker-data-protection-software.htm)

## About stadtluzern.io
stadtluzern.io is our public domain as dev's at the city government of luzern. Please refer to our [official website](https://www.stadtluzern.ch) for any other inquiries.

## License
The Unlicense, see [LICENSE](LICENSE) file.