import os

import paramiko
from dotenv import load_dotenv


# setup master and slave instances
def setup_instance(instance_type, client, instance):
    load_dotenv()
    pem_key_name = './' + os.getenv('AWS_PEM_KEY') + '.pem'
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance.public_ip_address,
                   username=ssh_username, key_filename=pem_key_name)
    print("Connected to " + instance_type + " instance")
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command(
        'git clone https://github.com/harnetlinh/automation_kubernetes.git')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo bash')
    if instance_type == 'master':
        stdin, stdout, stderr = client.exec_command(
            'chmod +x automation_kubernetes/master.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ./automation_kubernetes/master.sh')
        print(stdout.readlines())
    else:
        stdin, stdout, stderr = client.exec_command(
            'chmod +x automation_kubernetes/slave.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ./automation_kubernetes/slave.sh')
        print(stdout.readlines())
    print("Finished")
