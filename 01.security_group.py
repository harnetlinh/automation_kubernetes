import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
load_dotenv()

ec2 = boto3.client('ec2', region_name='ap-northeast-1',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))


response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = ec2.create_security_group(GroupName='all traffic group',
                                         Description='allow all traffic',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print(f'Security Group Created {security_group_id} in vpc {vpc_id}')

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'TCP',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}],

             },
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print(f'Ingress Successfully Set {data}')
except ClientError as e:
    print(e)
