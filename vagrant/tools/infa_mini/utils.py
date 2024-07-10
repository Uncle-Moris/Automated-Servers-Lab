import argparse
import subprocess
import os


def file_maker(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path,filename)
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)

def parser():
    pars = argparse.ArgumentParser(
        prog="mini_infra",
        description="This tiny script prepares infrastructure and runs nodes based on Vagrantfile"
    )
    # pars.add_argument('-p','--provider', help='choose provider', default='libvirt')
    # pars.add_argument('-m', '--master_node', help='define amount of masternodes', default=1, type=int)
    pars.add_argument('-n', '--nodes', help="define amount of nodes", default=1, type=int)
    
    return pars


def make_node_template(n: int) -> str:
    return f"""
        config.vm.define "node{n}" do |node| 
            node.vm.hostname = "node{n}"
            node.vm.box = "bento/ubuntu-24.04"
            node.vm.network :private_network, ip: "192.168.59.5{n}"
            node.vm.network "forwarded_port", guest: 22, host: 220{n}, id: "ssh"
            node.vm.synced_folder ".", "/vagrant", type: "9p", disabled: false
            node.vm.provision "shell", inline: <<-SHELL
                sudo cp /vagrant/hosts /etc/hosts
                SHELL
            node.vm.provider :libvirt do |libvirt|
                libvirt.memory = 1024
                libvirt.cpus = 1
            end
        end
    """

def make_hosts(nodes):
    m = "192.168.59.50 master\n"
    for node in range(1, nodes+1):
        m+=f"192.168.59.5{node} node{node}\n"
    file_maker(path="vagrant/", filename="hosts", content=m)

ansible_absolute_path = "/home/moris/Projects/Automated-Servers-Lab/ansible"

def make_vagrantfile_template(nodes: int) -> str:
    vagrantfile = f"""
    Vagrant.configure("2") do |config|
        config.vm.boot_timeout = 500
        # Master node
        config.vm.define "master" do |node|
            node.vm.box = "bento/ubuntu-24.04"
            node.vm.hostname = "master"
            node.vm.network :private_network, ip: "192.168.59.50"
            node.vm.network "forwarded_port", guest: 22, host: 2200, id: "ssh"

            node.vm.synced_folder ".", "/vagrant", type: "9p", disabled: false
            node.vm.provision "shell", inline: <<-SHELL
                sudo cp /vagrant/hosts /etc/hosts
                sudo apt-get update
                sudo apt-get install -y ansible sshpass
            SHELL


            node.vm.provider :libvirt do |libvirt|
                libvirt.memory = 1024
                libvirt.cpus = 1
            end
        end
    """
    #Nodes section
    for node in range(1, nodes+1):
        if nodes < 10:
            node_temp = make_node_template(node)
            vagrantfile+=node_temp
        else:
            print("more than 9 nodes is not allowed!!")
            os.esxit(1)
    
    #End
    vagrantfile+=f"""
    end
    """
    file_maker(path="vagrant/", filename="Vagrantfile", content=vagrantfile)
    
def run():
    os.chdir('vagrant')
    subprocess.run(["vagrant", "up"])