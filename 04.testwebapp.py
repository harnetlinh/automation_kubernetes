import os

import paramiko
from libs import *
from dotenv import load_dotenv
import pprint
import time

load_dotenv()

def create_apache_docker_image(instance):
    """create apache docker image
    Args:
        instance (object): instance object
    """
    pem_key_name = os.getenv('AWS_PEM_KEY') + '.pem'
    ssh_username = os.getenv('SSH_USERNAME')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(hostname=instance['PublicIpAddress'],
                   username=ssh_username, key_filename=pem_key_name)
    stdin, stdout, stderr = client.exec_command('mkdir docker-hello-world && cd docker-hello-world')
    print('mkdir docker-hello-world && cd docker-hello-world')
    if stderr.readlines():
        print(stderr.readlines())
        return        
    stdin, stdout, stderr = client.exec_command('sudo bash')
    stdin, stdout, stderr = client.exec_command('docker build -t tutum/hello-world .')
    print('running docker build -t tutum/hello-world .')
    if stderr.readlines():
        print(stderr.readlines())
        return
    else:
        print(stdout.readlines())
        
    stdin, stdout, stderr = client.exec_command('sudo docker push tutum/hello-world')
    print('running docker push tutum/hello-world')
    if stderr.readlines():
        print(stderr.readlines())
        return
    else:
        print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo docker run -d -p 80 tutum/hello-world')
    print('running docker run -d -p 80 tutum/hello-world')
    if stderr.readlines():
        print(stderr.readlines())
        return
    else:
        print(stdout.readlines())
    print("Finished deploying docker image")



reservations = get_running_instances()
reservation = reservations[0]
instances = reservation['Instances']
instance = instances[0]
create_apache_docker_image(instance)


        


