
# DevOps Home Lab

## Description
This project is a home lab setup using Vagrant to provision hosts on KVM, and Ansible for configuration management. It is part of my portfolio showcasing DevOps skills.

## Pre req for Linux 

1. Install vagrant-libvert https://vagrant-libvirt.github.io/vagrant-libvirt/#installation
2. Install qemu (above doc miss ) https://www.qemu.org/download/#linux

## Set up VM's and Ansible
1. Define vm's in Vagrantfile feel free to use actuale vm as template for future one
2. Run vagrant with `vagrant up` command
3. Log in master node via `vagrant ssh master` command and run `python3 /vagrant/tools/set_ssh.py vagrant` this script generate new ssh-keys and copy to each node.
4. Copy ansible.pum to `bootstrap.yml` for user ansible

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## Authors and Acknowledgment
This project was developed by Uncle Moris. Special thanks to all contributors.

## License
This project is licensed under the MIT License.

## Project Status
This project is actively maintained.
