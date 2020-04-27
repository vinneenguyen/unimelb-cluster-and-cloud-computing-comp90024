*Note: This project is built completely upon OpenStack cloud computing platform, in which context this documentation
shall proceed to be interpreted if any further.*  

### Dependencies ###
[Python 3](https://www.python.org/downloads/)  
[Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)  
[OpenStack Client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)  
[OpenStack Compute (nova)](https://docs.openstack.org/nova/latest/#installation)  

### Dynamic inventory ###
Dynamic inventory is available with the use of script `inventories/openstack_all.py`.  
For comprehensive demonstration, see [Inventory script example](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html#inventory-script-example-openstack).  

### Common commands ###
#### Set environment variables for connection
```shell script
source openrc.sh
```

#### Compute instance information retrieval
```shell script
chmod +x inventories/openstack_all.py  # make executable
inventories/openstack_all.py --list  # retrieve instance information
```

#### Launch compute instances
```shell script
ansible-playbook instances.yaml
```

#### Delete instances
```shell script
nova list | awk '$2 && $2 != "ID" {print $2}' | xargs -n1 nova delete
```
See [Openstack -Delete Bulk Instances](https://maestropandy.wordpress.com/2016/08/24/openstack-delete-bulk-instances/)  

#### Create volumes
```shell script
ansible-playbook volumes.yaml
```
