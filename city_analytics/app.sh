#!/bin/bash

# ansible-playbook -i inventories/hosts.yaml db_security.yaml 
# ansible-playbook -i inventories/hosts_auto.ini applications.yaml #--skip-tags "kill_container" # Docker-compose application under 
# ansible-playbook -i inventories/hosts_auto.ini couchDB_setup.yaml  # Create couchDB cluster


# ansible-playbook -i inventories/hosts_auto.ini couchdb_view.yaml
# ansible-playbook -i inventories/hosts_auto.ini harvest.yaml 
ansible-playbook -i inventories/hosts_auto.ini webapp.yaml 
# ansible-playbook -i inventories/hosts_auto.ini geo.yaml 