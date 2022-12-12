import os

import paramiko
from libs import *
from dotenv import load_dotenv
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
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance['PublicIpAddress'],
                   username=ssh_username, key_filename=pem_key_name)
    print("Connected to " + instance_type + " instance")
    
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    stdin, stdout, stderr = client.exec_command(
        'rm -rf automation_kubernetes_test')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command(
        'git clone https://github.com/harnetlinh/automation_kubernetes_test.git')
    out = stdout.readlines()
    print('git cloned')
    print(out) 
    stdin, stdout, stderr = client.exec_command('sudo bash')
    if instance_type == 'master':
        stdin, stdout, stderr = client.exec_command(
            'chmod +x ~/automation_kubernetes_test/01.master01.sh')
        print('chmod +x /home/ubuntu/automation_kubernetes_test/01.master01.sh')
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print(out) 
        
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        print('chmod +x /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print(out) 
        stdin, stdout, stderr = client.exec_command(
            'sudo ~/automation_kubernetes_test/01.master01.sh')
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print(out) 
        
        join = get_join_command_from_master(client)
        stdin, stdout, stderr = client.exec_command(
            'sudo /home/ubuntu/automation_kubernetes_test/01.master02.sh')
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print(out)  
        
        return join

    else:
        if join_command is None:
            raise Exception('join command is None')
            
        stdin, stdout, stderr = client.exec_command(
            'chmod +x /home/ubuntu/automation_kubernetes_test/02.slave.sh')
        stdin, stdout, stderr = client.exec_command(
            'sudo ~/automation_kubernetes_test/02.slave.sh')
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print(out)            
        stdin, stdout, stderr = client.exec_command(join_command)
        err = stderr.readlines()
        out = stdout.readlines()
        if len(err) > 0:
            print(err)
            return
        else:
            print('Slave ip: ' + instance['PublicIpAddress'] + ' is joined to master')
            print(out)   
        return "ok"

def get_join_command_from_master(client):
    """get join command from master instance"""

    stdin, stdout, stderr = client.exec_command('sudo kubeadm token create --print-join-command')
    print('get join command from master instance')
    if stderr.readlines():
        print(stderr.readlines())
        return
    else:
        print(stdout.readlines()) 
    join_command = stdout.readlines()
    join_command = join_command[0]  #.split(' ')[-2].split(':')[-1]
    print('join command is: ')
    print(join_command)
    return join_command

# get all running instances with function in libs and setup master and slave instances
reservations = get_running_instances()
reservation = reservations[0]
instances = reservation['Instances']
master = instances[0]
list_slave = instances[1:]
print('SETUP MASTER IP: ' + master['PublicIpAddress'] + '')
join_command = setup_instance('master', master)
print('DONE: MASTER IP ' + master['PublicIpAddress'] + ' IS READY')
if join_command != '' and join_command is not None:
    for slave in list_slave:
        print('SETUP SLAVE IP: ' + slave['PublicIpAddress'] + '')
        setup_instance('slave', slave, join_command)
        print('DONE: SLAVE IP ' + slave['PublicIpAddress'] + ' IS READY')
    print('DONE: CLUSTER IS READY, WAITING FOR WEB APP')
else:
    print('ERROR: JOIN COMMAND IS EMPTY')


