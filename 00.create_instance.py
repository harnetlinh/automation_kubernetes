import boto3
import botocore
import paramiko
import time
import pprint
import random


ec2 = boto3.resource('ec2', region_name='ap-northeast-1')
ecs = boto3.client('ecs', region_name='ap-northeast-1')

security_groups = ec2.describe_security_groups()
security_group_ids = [sg['GroupId'] for sg in security_groups['SecurityGroups']]



def create_instance(ec2, security_group_ids, type_ = 'NA', num_instances =1):

    if type_ == 'master' or type_ == 'slave':
       
       instance = ec2.create_instances(
        #change ImageId to your ImageId
        ImageId = 'ami-0a5866d87afdfdfd3',
        MinCount = num_instances,
        MaxCount = num_instances,
        InstanceType = 't2.medium',
        #change Keyname to your KeyName
        KeyName = 'awspem',
        #change SecurityGroupIds to your SecurityGroupIds
        SecurityGroupIds=security_group_ids,
        )
        # instance[0].wait_until_running()           
        # instance[0].reload()
        return instance

    else:
        return None
    

def create_cluster(ecs):
    random_num = random.randint(1, 100)
    cluster = ecs.create_cluster(
        clusterName = 'cluster_boto3_' + str(random_num),
        tags = [{'key': 'cluster_boto3', 'value': 'cluster_boto3'}],
    )
    return cluster

def create_nodegroup(ec2):
    nodegroup = ec2.create_nodegroup(
        clusterName = 'eks_boto3' + str(time.time()),
        nodegroupName = 'eks_boto3' + str(time.time()),
        subnets = ['subnet-0b0c0d0e0f0a0b0c0'],
        tags = [{'key': 'eks_boto', 'value': 'eks_boto'}],
    )
    return nodegroup


ins_master = create_instance(ec2, security_group_ids, type_  = 'master')
ins_slave = create_instance(ec2, security_group_ids, type_  = 'slave', num_instances = 4)

ecs = create_cluster(ecs)
print(ecs)




client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()

# setup master and slave instances
def setup_instance(instance_type, client, instance):

    client.connect(hostname=instance.public_ip_address, username="ubuntu", key_filename='./awspem.pem')
    print ("Connected to " + instance_type + " instance")
    stdin, stdout, stderr = client.exec_command('sudo apt install git -y')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('git clone https://github.com/harnetlinh/automation_kubernetes.git')
    print(stdout.readlines())
    stdin, stdout, stderr = client.exec_command('sudo bash')
    if instance_type == 'master':
        stdin, stdout, stderr = client.exec_command('chmod +x automation_kubernetes/master.sh')
        stdin, stdout, stderr = client.exec_command('sudo ./automation_kubernetes/master.sh')
        print(stdout.readlines())
    else:
        stdin, stdout, stderr = client.exec_command('chmod +x automation_kubernetes/slave.sh')
        stdin, stdout, stderr = client.exec_command('sudo ./automation_kubernetes/slave.sh')
        print(stdout.readlines())
    print ("Finished")