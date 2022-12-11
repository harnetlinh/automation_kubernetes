import boto3
import botocore
import time
import pprint
import random
from libs import *

session = init_aws_session()
ec2 = boto3.resource('ec2', region_name='ap-northeast-1')
ecs = boto3.client('ecs', region_name='ap-northeast-1')

security_groups = ec2_get_security_group_list()
sec_group = []

for security_group in security_groups:
    security_group_ip_perms = security_group['IpPermissions']
    for security_group_ip_perm in security_group_ip_perms:
        if security_group_ip_perm['IpProtocol'] == 'tcp' and security_group_ip_perm['FromPort'] == 80:
            vpc_id = security_group['VpcId']
            security_group_id = security_group['GroupId']
            sec_group.append(security_group)
            break
security_group_ids = [sg['GroupId']
                      for sg in sec_group]
print(security_group_ids)

def create_instance(ec2, security_group_ids, type_='NA', num_instances=1):

    if type_ == 'master' or type_ == 'slave':

        instance = ec2.create_instances(
            # change ImageId to your ImageId
            ImageId='ami-0a5866d87afdfdfd3',
            MinCount=num_instances,
            MaxCount=num_instances,
            InstanceType='t2.medium',
            # change Keyname to your KeyName
            KeyName='awspem',
            # change SecurityGroupIds to your SecurityGroupIds
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
        clusterName='cluster_boto3_' + str(random_num),
        tags=[{'key': 'cluster_boto3', 'value': 'cluster_boto3'}],
    )
    return cluster


def create_nodegroup(ec2):
    nodegroup = ec2.create_nodegroup(
        clusterName='eks_boto3' + str(time.time()),
        nodegroupName='eks_boto3' + str(time.time()),
        subnets=['subnet-0b0c0d0e0f0a0b0c0'],
        tags=[{'key': 'eks_boto', 'value': 'eks_boto'}],
    )
    return nodegroup


ins_master = create_instance(ec2, security_group_ids, type_='master')
ins_slave = create_instance(ec2, security_group_ids,  type_='slave', num_instances=4)

# ecs = create_cluster(ecs)
# print(ecs)



