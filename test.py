import boto3
import botocore
import paramiko
import time
import pprint
import random
from libs import *

session = init_aws_session()
ec2 = session.resource('ec2')
# ec2 = boto3.resource('ec2', region_name='ap-northeast-1')
# ecs = boto3.client('ecs', region_name='ap-northeast-1')


instance = ec2.create_instances(
            # change ImageId to your ImageId
            ImageId='ami-0a5866d87afdfdfd3',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.medium',
            # change Keyname to your KeyName
            KeyName='awspem',
            # change SecurityGroupIds to your SecurityGroupIds
            SecurityGroupIds=['sg-00e6d61858d13a8d5'],
        )
print(instance)