This is the documentation for project deployment.

*Note:*  
\- *This project is built completely upon OpenStack cloud computing platform, in which context this documentation
shall proceed to be interpreted if any further.*  
\- *The targeted operating system (on servers) is Unix-like operating system, in which the project is tested. In other
other operating systems (like Mac, Windows), commands might not work as expected.*  
\- *If not specified, all commands below are run from the project directory.*  

---

### Dependencies ###
[Python 3](https://www.python.org/downloads/)  
[Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)  
[OpenStack Client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)  
[OpenStack Compute (nova)](https://docs.openstack.org/nova/latest/#installation)  

On servers:  
[Docker](https://docs.docker.com/get-docker/)  
[Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)  

### Provide credentials for connection ###
*Note: if it is the first time you are granted access to the cloud service or you did not register for the service with
a password, you may have to reset your password for valid authentication.*  

One way to input credentials is through environment variables.  
```shell script
source credentials/openrc.sh  # set credentials to environment variables
```

### Install roles ###
The following roles are required for installation of dependencies:  
\- [Docker on Linux](https://galaxy.ansible.com/geerlingguy/docker)  
\- [Pip on Linux](https://galaxy.ansible.com/geerlingguy/pip)  
all by [Jeff Geerling](https://github.com/geerlingguy).  
```shell script
ansible-galaxy install -r roles/requirements.yml
```

Alternatively, `credentials/clouds_template.yaml` can be used. See the documentation inside file for details.  

### Enable use of dynamic inventory ###
Dynamic inventory is available with the use of script `inventories/dynamic.py`. For comprehensive demonstration,
see [dynamic inventory example](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html#inventory-script-example-openstack).  
```shell script
chmod +x inventories/dynamic.py  # make script executable
inventories/dynamic.py --list  # test by retrieving instance information
```

### Create security groups ###
```shell script
ansible-playbook security_groups.yaml
```
Parameters set for security groups are defined in `vars/security.yaml`.  

### Generate keypairs ###
```shell script
ansible-playbook keypairs.yaml
```
Parameters set for keypairs are defined in `vars/access.yaml`.  
Generated private key is stored at `credentials/common.pem`, access permission was changed to 600.  

### Launch compute instances ###
Instances created with specified keypair, then added to appointed security groups.  
```shell script
ansible-playbook -i inventories/hosts.yaml instances.yaml
```
Common parameters shared between instances are defined in `inventories/group_vars/webservers.yaml`.  

### Create volumes ###
```shell script
ansible-playbook -i inventories/hosts.yaml volumes.yaml
```
Parameters set for volumes are defined in `inventories/group_vars/webservers.yaml`.  

### Attach volumes to instances ###
```shell script
ansible-playbook -i inventories/hosts.yaml volumes_attach.yaml
```

### Export inventory file with IP addresses ###
Since instances were created with dynamic IP addresses, it is necessary to obtain the those IP addresses for later use
(e.g establishing SSH connection).  
```shell script
ansible-playbook -i inventories/dynamic.py -i inventories/hosts.yaml inventory_export.yaml
```
*Note: New inventory file is stored at `inventories/hosts_auto.ini`*  

### Detach volumes from instances ###
```shell script
ansible-playbook -i inventories/hosts.yaml volumes_detach.yaml
```

### Delete instances ###
___Warning: this command should be used with high caution as it will delete all instances currently available in connected
cloud projet.___
```shell script
nova list | awk '$2 && $2 != "ID" {print $2}' | xargs -n1 nova delete
```
Source: [Openstack - Delete Bulk Instances](https://maestropandy.wordpress.com/2016/08/24/openstack-delete-bulk-instances/)  

---

### Set up servers ###
Execute the following series of orchestrations (described in playbooks):  
\- Install roles  
\- Enable dynamic inventory  
\- Create security groups  
\- Generate keypairs  
\- Launch instances  
\- Create volumes  
\- Attach volumes  
\- Generate inventory file with IP addresses  
```shell script
./setup.sh
```

---

### References ###
[chmod WSL (Bash) doesn't work](https://stackoverflow.com/questions/46610256/chmod-wsl-bash-doesnt-work)  
[Playbooks, Roles and Ansible Galaxy](https://azurecitadel.com/automation/packeransible/lab4/)  
