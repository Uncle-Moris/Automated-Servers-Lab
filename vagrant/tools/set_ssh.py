import argparse
import subprocess

def run_command(command):
    """ Uruchamia polecenie i zwraca kod wyjścia, wyjście standardowe oraz błędy. """
    print(f"Running command: {command}")  # Debug: Wypisz komendę przed jej uruchomieniem
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error}")  # Wypisz błędy jeśli wystąpią
    return process.returncode, output, error

def main(password):
    gen_key_command = 'ssh-keygen -C "ansible" -f /home/vagrant/.ssh/ansible -N ""'
    code, output, error = run_command(gen_key_command)

    if code == 0:
        print("SSH key successfully generated")
        print(output)
    else:
        print("Failed to generate SSH key")

    nodes = ['master','node1', 'node2', 'node3', 'node8', 'node9']
    for node in nodes:
        copy_key_command = f"sshpass -p {password} ssh-copy-id -o StrictHostKeyChecking=no -i /home/vagrant/.ssh/ansible.pub {node}"
        code, output, error = run_command(copy_key_command)
        if code == 0:
            print(f"SSH key successfully copied to {node}.")
            print(output)
        else:
            print(f"Error copying SSH key to {node}:")
            print(error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automatically copy SSH keys to nodes.')
    parser.add_argument('password', help='SSH password used for ssh-copy-id.')
    args = parser.parse_args()

    main(args.password)

    
