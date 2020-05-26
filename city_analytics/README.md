This is the documentation for project deployment.

*Note:*  
\- *This project is built completely upon OpenStack cloud computing platform, in which context this documentation
shall proceed to be interpreted if any further.*  
\- *The targeted operating system (on servers) is Unix-like operating system, in which the project is tested. In other
other operating systems (like Mac, Windows), commands might not work as expected.*  
\- *If not specified, all commands below are run from the project directory.*  

---

### Dependencies ###
On control:  
[Python](https://www.python.org/)  
[pip - The Python Package Installer](https://pip.pypa.io/en/stable/)  
[Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)  
[OpenStack Client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)  
[OpenStack Compute (nova)](https://docs.openstack.org/nova/latest/#installation)  
[OpenStack SDK](https://docs.openstack.org/openstacksdk/latest/user/)  
*Note: Installing [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) with*
*[pip](https://pip.pypa.io/en/stable/) may be simpler and thus the more preferable way than*
 *some other methods.*  

On servers:  
[Python 3](https://www.python.org/downloads/)  
[pip](https://pip.pypa.io/en/stable/) (Python 3)  
[Docker](https://docs.docker.com/get-docker/)  
[Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)  

### Provide credentials for connection ###
*Note: if it is the first time you are granted access to the cloud service or you did not register for the service with
a password, you may have to reset your password for valid authentication.*  

One way to input credentials is through environment variables.  
```shell script
source credentials/openrc.sh  # set credentials to environment variables
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
ansible -i inventories/hosts_auto.ini all -m ping  # test by pinging instances for response
```
*Note: New inventory file is stored at `inventories/hosts_auto.ini`*  

### Proxies configuration ###
As the instance is behind the University network, instances will need to add proxy settings to access the internet. Append block of proxy settings into /etc/environment for instances. Same needed for docker service, http-proxy.conf.j2 is copied into to /etc/systemd/system/docker.service.d. Daemon and docker are restarted to have new settings to take effect.
```shell script
ansible-playbook -i inventories/hosts_auto.ini proxy_config.yaml 
```

### Install dependencies ###
The following packages are installed on servers:  
\- [apt-transport-https] This APT transport allows the use of repositories accessed via the HTTP Secure protocol
\- [build-essential] Packages needed to compile a Debian package
\- [ca-certificates] program that updates the directory /etc/ssl/certs to hold SSL certificates and generates ca-certificates
\- [curl] URL syntax to transfer data to and from servers.
\- [git] A version control system
\- [python-dev] Package that contains the header files for the Python C API
\- [python-pip] Package installer for Python
\- [python-setuptools] Facilitate packaging Python projects by enhancing the Python standard library distutils
\- [software-properties-common] This software provides an abstraction of the used apt repositories
\- [unzip] Unzip file
\- [vim] My favorite editor
\- [pip](https://pip.pypa.io/en/stable/)  
\- [Docker](https://docs.docker.com/get-docker/)  

```shell script
ansible-playbook -i inventories/hosts_auto.ini dependencies.yaml
```

### Format External /dev/vdb Volume ###
This command install XFS file system on the attached volume /dev/vdb. To avoid reinstalling file system again, install xfs and make file system tasks are tagged with format. Using --skip-tags on the command skip these tasks. The formatted volume is mounted on /external. 
```shell script
ansible-playbook -i inventories/hosts_auto.ini formatvolume.yaml --skip-tags "format"
```

### Install Docker ###
This playbook uninstall old docker, new docker installer is obtained from (https://download.docker.com/linux/ubuntu/gpg). Docker and Docker compose is installed after using apt and pip.
```shell script
ansible-playbook -i inventories/hosts_auto.ini docker.yaml
```

### Install Docker ###
This playbook uninstall old docker, new docker installer is obtained from (https://download.docker.com/linux/ubuntu/gpg). Docker and Docker compose is installed after using apt and pip.
```shell script
ansible-playbook -i inventories/hosts_auto.ini docker.yaml
```

### Copy project folder to Cloud instances ###
Execute following to copy city_analytics directory to cloud's external storage, if already exist, files will be overwritten. Prior that, /external permission is changed to allow read and write remotely. 
```shell script
ansible-playbook -i inventories/hosts_auto.ini sync_repo.yaml
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
\- Add proxy
\- Install dependencies
\- Format external volume
\- Install docker
\- Copy project repo to cloud
```shell script
./setup.sh
```


### Create and Add security group for CouchDB ###
Execute following to create a security group that opens internal ports 4369, 5000, 5986, 6379, 9100-9200
```shell script
ansible-playbook -i inventories/hosts.yaml db_security.yaml 
```

### CouchDB application ###
Execute following to create a security group that opens internal ports 4369, 5000, 5986, 6379, 9100-9200
```shell script
ansible-playbook -i inventories/hosts.yaml db_security.yaml 
```

---

### Applications ###
Execute the following series of orchestrations (described in playbooks):  
\- Add security group
\- CouchDB application

```shell script
./app.sh
```

---



### References ###
[Running Ansible within Windows](https://www.jeffgeerling.com/blog/running-ansible-within-windows)  
[chmod WSL (Bash) doesn't work](https://stackoverflow.com/questions/46610256/chmod-wsl-bash-doesnt-work)  
[Playbooks, Roles and Ansible Galaxy](https://azurecitadel.com/automation/packeransible/lab4/)  
[How to install apps remotely with Ansible](https://www.techrepublic.com/article/how-to-install-apps-remotely-with-ansible/)  
