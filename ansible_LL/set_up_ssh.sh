#!/bin/bash

ssh-keygen -C "ansible" -f ~/.ssh/ansible -N "" &&

ssh-copy-id -i /home/vagrant/.ssh/ansible.pub node1 &&
ssh-copy-id -i /home/vagrant/.ssh/ansible.pub node2 &&
ssh-copy-id -i /home/vagrant/.ssh/ansible.pub node8
