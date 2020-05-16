#!/bin/bash

<<<<<<< HEAD
# chmod +x inventories/dynamic.py  # make script executable
# inventories/dynamic.py --list  # test by retrieving instance information
# ansible-playbook security_groups.yaml  # create security groups
# ansible-playbook keypairs.yaml  # generate keypairs
# ansible-playbook -i inventories/hosts.yaml instances.yaml  # launch compute instances
# ansible-playbook -i inventories/hosts.yaml volumes.yaml  # create volumes
# ansible-playbook -i inventories/hosts.yaml volumes_attach.yaml  # attach volumes to instances
# ansible-playbook -i inventories/dynamic.py -i inventories/hosts.yaml inventory_export.yaml  # generate inventory file with IP addresses
# ansible-playbook -i inventories/hosts_auto.ini proxy_config.yaml  # Add proxy to etc/environment and docker environment
# ansible-playbook -i inventories/hosts_auto.ini dependencies.yaml -> maybe removed???
# ansible-playbook -i inventories/hosts_auto.ini formatvolume.yaml  # Format attached volume, *under construction
# ansible-playbook -i inventories/hosts_auto.ini docker.yaml
# copy master project directory to attached volume of instance clone.yaml

ansible-playbook -i inventories/hosts_auto.ini applications.yaml  # Docker-compose application under 
ansible-playbook -i inventories/hosts_auto.ini couchDB_setup.yaml  # Create couchDB cluster
=======
chmod +x inventories/dynamic.py  # make script executable
inventories/dynamic.py --list  # test by retrieving instance information
ansible-playbook security_groups.yaml  # create security groups
ansible-playbook keypairs.yaml  # generate keypairs
ansible-playbook -i inventories/hosts.yaml instances.yaml  # launch compute instances
ansible-playbook -i inventories/hosts.yaml volumes.yaml  # create volumes
ansible-playbook -i inventories/hosts.yaml volumes_attach.yaml  # attach volumes to instances
ansible-playbook -i inventories/dynamic.py -i inventories/hosts.yaml inventory_export.yaml  # generate inventory file with IP addresses
ansible-playbook -i inventories/hosts_auto.ini proxy_config.yaml  # Add proxy to etc/environment and docker environment
ansible-playbook -i inventories/hosts_auto.ini dependencies.yaml
ansible-playbook -i inventories/hosts_auto.ini formatvolume.yaml --skip-tags "format" # Format attached volume, *under construction
ansible-playbook -i inventories/hosts_auto.ini docker.yaml
ansible-playbook -i inventories/hosts_auto.ini sync_repo.yaml
>>>>>>> 98208986900a4eadc5ed1c680edd5ed80c931440


# Use for Debugging 
# ansible-playbook -i inventories/hosts.yaml test.yaml
