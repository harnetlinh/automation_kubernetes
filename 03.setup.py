import os

import paramiko
from libs import *
from dotenv import load_dotenv
import pprint
import time

load_dotenv()
# setup master and slave instances
def setup_instance(instance_type, instance, join_command=None):
    """setup master and slave instances

    Args:
        instance_type (string): "master" or "slave"
        instance (object): instance object
    """
    pem_key_name = os.getenv('AWS_PEM_KEY') + '.pem'
    # print("Connecting to " + instance_type + " instance")
    # print('pem_key_name: ' + pem_key_name)
    # print('public ip: ' + instance['PublicIpAddress'])
    # print('ssh_username: ' + os.getenv('SSH_USERNAME'))
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance['PublicIpAddress'],
                   username=ssh_username, key_filename=pem_key_name)
    # pprint("Connected to " + instance_type + " instance")
    
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    test = stdout.readlines()
    print('sudo apt install git -y')

    stdin, stdout, stderr = client.exec_command(
        'rm -rf automation_kubernetes_test')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command(
        'git clone https://github.com/harnetlinh/automation_kubernetes_test.git')
    # time.sleep(50);
    print(stdout.readlines())
    print(stderr.readlines())
    stdin, stdout, stderr = client.exec_command('cd automation_kubernetes_test/')
    print(stdout.readlines())
    print(stderr.readlines())
    stdin, stdout, stderr = client.exec_command('ls')

    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo bash')
    if instance_type == 'master':
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/01.master01.sh')
        print('chmod +x /home/ubuntu/automation_kubernetes_test/01.master01.sh')
        print(stdout.readlines())
        
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        print('check folder')
        print(stdout.readlines())
        stdin, stdout, stderr = client.exec_command(
            'sudo ~/automation_kubernetes_test/01.master01.sh')
        print(stdout.readlines())
        print(stderr.readlines())
        
        join = get_join_command_from_master(client)
        stdin, stdout, stderr = client.exec_command(
            'sudo /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        print(stdout.readlines())
        return join

    else:
        if join_command is None:
            raise Exception('join command is None')
            
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/02.slave.sh')
        print(stdout)
        print(stderr)
        stdin, stdout, stderr = client.exec_command(
            'sudo /home/ubuntu/automation_kubernetes_test/02.slave.sh')
        
        print(stderr)
        stdin, stdout, stderr = client.exec_command(join_command)
        print(stdout)
        print(stderr)
        return "ok"
        
def setup_instance_debug(instance_type, instance, join_command=None):
    """setup master and slave instances

    Args:
        instance_type (string): "master" or "slave"
        instance (object): instance object
    """
    pem_key_name = os.getenv('AWS_PEM_KEY') + '.pem'
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance['PublicIpAddress'],
                   username=ssh_username, key_filename=pem_key_name)
    """
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    test = stdout.readlines()
    print('sudo apt install git -y')

    stdin, stdout, stderr = client.exec_command(
        'rm -rf automation_kubernetes_test')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command(
        'git clone https://github.com/harnetlinh/automation_kubernetes_test.git')
    # time.sleep(50);
    print(stdout.readlines())
    print(stderr.readlines())
    stdin, stdout, stderr = client.exec_command('cd automation_kubernetes_test/')
    print(stdout.readlines())
    print(stderr.readlines())
    stdin, stdout, stderr = client.exec_command('ls')

    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo bash')
    """
    if instance_type == 'master':
        """
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/01.master01.sh')
        print('chmod +x /home/ubuntu/automation_kubernetes_test/01.master01.sh')
        print(stdout.readlines())
        
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        print('check folder')
        print(stdout.readlines())
        stdin, stdout, stderr = client.exec_command(
            'sudo ~/automation_kubernetes_test/01.master01.sh')
        print(stdout.readlines())
        print(stderr.readlines())
        """
        join = get_join_command_from_master(client)
        stdin, stdout, stderr = client.exec_command(
            'sudo /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        print(stdout)
        print(stderr)
        
        return join

    else:
        if join_command is None:
            raise Exception('join command is None')
            
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/02.slave.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ~/automation_kubernetes_test/02.slave.sh')
        if stderr.readlines() != []:
            print(stderr.readlines())
        else:
            print('slave is ready')
            print(stdout.readlines())            
        stdin, stdout, stderr = client.exec_command(join_command)
        if stderr.readlines() != []:
            print(stderr.readlines())
        else:
            print('slave ip ' + instance['PublicIpAddress'] + ' is joined to master')
            print(stdout.readlines())  
        
        return "ok"

def get_join_command_from_master(client):
    """get join command from master instance"""

    stdin, stdout, stderr = client.exec_command('sudo kubeadm token create --print-join-command')
    print('get join command from master instance')
    print(stderr.readlines())
    # print(stdout.readlines())
    join_command = stdout.readlines()
    print(join_command)
    join_command = join_command[0]  #.split(' ')[-2].split(':')[-1]
    print(join_command)
    return join_command

# get all running instances with function in libs and setup master and slave instances
reservations = get_running_instances()
reservation = reservations[0]
instances = reservation['Instances']
master = instances[0]
list_slave = instances[1:]
join_command = setup_instance_debug('master', master)
for slave in list_slave:
    print('setup slave')
    setup_instance_debug('slave', slave, join_command)
print('DONE: CLUSTER IS READY, WAITING FOR WEB APP')


