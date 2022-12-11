import os

import paramiko
from libs import *
from dotenv import load_dotenv
import ppprint

load_dotenv()
# setup master and slave instances
def setup_instance(instance_type, instance, join_command=None):
    """setup master and slave instances

    Args:
        instance_type (string): "master" or "slave"
        instance (object): instance object
    """
    pem_key_name = os.getenv('AWS_PEM_KEY') + '.pem'
    pprint("Connecting to " + instance_type + " instance")
    pprint('pem_key_name: ' + pem_key_name)
    pprint('public ip: ' + instance['PublicIpAddress'])
    pprint('ssh_username: ' + os.getenv('SSH_USERNAME'))
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance['PublicIpAddress'],
                   username=ssh_username, key_filename=pem_key_name)
    pprint("Connected to " + instance_type + " instance")
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    pprint(stdout.readlines())
    stdin, stdout, stderr = client.exec_command(
        'git clone https://github.com/harnetlinh/automation_kubernetes.git')
    pprint(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo bash')
    if instance_type == 'master':
        stdin, stdout, stderr = client.exec_command(
            'chmod +x automation_kubernetes/01.master-01.sh')
        
        stdin, stdout, stderr = client.exec_command(
            'chmod +x automation_kubernetes/01.master-02.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ./automation_kubernetes/01.master-01.sh')
        join = get_join_command_from_master(client)
        stdin, stdout, stderr = client.exec_command(
            'sudo ./automation_kubernetes/01.master-02.sh')
        pprint(stdout.readlines())
        return join

    else:
        if join_command is None:
            raise Exception('join command is None')
            
        stdin, stdout, stderr = client.exec_command(
            'chmod +x automation_kubernetes/02.slave.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ./automation_kubernetes/02.slave.sh')
        stdin, stdout, stderr = client.exec_command(join_command)
        pprint(stdout.readlines())
        return "ok";
        
    pprint("Finished")

def get_join_command_from_master(client):
    """get join command from master instance"""

    stdin, stdout, stderr = client.exec_command('sudo kubeadm token create --print-join-command')
    join_command = stdout.readlines()[0]
    pprint(join_command)
    return join_command

# get all running instances with function in libs and setup master and slave instances
reservations = get_running_instances()
reservation = reservations[0]
instances = reservation['Instances']
master = instances[0]
list_slave = instances[1:]
join_command = setup_instance('master', master)
for slave in list_slave:
    setup_instance('slave', slave, join_command)

        


