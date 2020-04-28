This is the documentation for project deployment.

*Note:*  
\- *This project is built completely upon OpenStack cloud computing platform, in which context this documentation
shall proceed to be interpreted if any further.*  
\- *If not specified, all commands below are run from the project directory.*  

### Dependencies ###
[Python 3](https://www.python.org/downloads/)  
[Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)  
[OpenStack Client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)  
[OpenStack Compute (nova)](https://docs.openstack.org/nova/latest/#installation)  

### Provide credentials for connection ###
*Note: if it is the first time you are granted access to the cloud service or you did not register for the service with
a password, you may have to reset your password for valid authentication.*  

One way to input credentials is through environment variables.  
```shell script
source credentials/openrc.sh  # set credentials to environment variables
```

Alternatively, `credentials/clouds-template.yaml` can be used. See the documentation inside file for details.  

### Enable use of dynamic inventory ###
Dynamic inventory is available with the use of script `inventories/openstack_all.py`. For comprehensive demonstration,
see [Inventory script example](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html#inventory-script-example-openstack).  
```shell script
chmod +x inventories/openstack_all.py  # make script executable

# Retrieve instance information
inventories/openstack_all.py --list
```

### Create volumes ###
```shell script
ansible-playbook volumes.yml
```

### Launch compute instances ###
```shell script
ansible-playbook instances.yml
```

### Delete instances ###
```shell script
nova list | awk '$2 && $2 != "ID" {print $2}' | xargs -n1 nova delete
```
See [Openstack -Delete Bulk Instances](https://maestropandy.wordpress.com/2016/08/24/openstack-delete-bulk-instances/)  


