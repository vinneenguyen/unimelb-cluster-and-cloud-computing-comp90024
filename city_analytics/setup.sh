#!/bin/bash

ansible-galaxy install -r roles/requirements.yml  # install roles
chmod +x inventories/dynamic.py  # make script executable
inventories/dynamic.py --list  # test by retrieving instance information
ansible-playbook security_groups.yaml  # create security groups
ansible-playbook keypairs.yaml  # generate keypairs
ansible-playbook -i inventories/hosts.yaml instances.yaml  # launch compute instances
ansible-playbook -i inventories/hosts.yaml volumes.yaml  # create volumes
ansible-playbook -i inventories/hosts.yaml volumes_attach.yaml  # attach volumes to instances
ansible-playbook -i inventories/dynamic.py -i inventories/hosts.yaml inventory_export.yaml  # generate inventory file with IP addresses
ansible-playbook -i inventories/hosts.yaml proxy_config.yaml  # Add proxy to etc/environment and docker environment