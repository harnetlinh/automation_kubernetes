import os
from urllib import response
import boto3
import pprint
from dotenv import load_dotenv


def get_aws_keys():
    load_dotenv()
    return os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY')


def init_aws_session():
    access_key, secret_key = get_aws_keys()
    return boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=os.getenv('AWS_REGION'))


def ec2_get_security_group_list():
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.describe_security_groups()
    return response['SecurityGroups']


def ec2_add_security_group(desc, grp_name, vpc_id):
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.create_security_group(
        Description=desc, GroupName=grp_name, VpcId=vpc_id)
    return response


def ec2_delete_security_group(grp_id):
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.delete_security_group(GroupId=grp_id)
    return response


def elb_create_target_group(target_group_name, vpc_id):
    session = init_aws_session()
    elb = session.client('elbv2')
    response = elb.create_target_group(
        Name=target_group_name, Protocol='HTTP', Port=80, VpcId=vpc_id)
    return response


def ec2_add_security_group_rule(grp_id, proto, start_port, end_port, ip_range):
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.authorize_security_group_egress(
        GroupId=grp_id,
        IpPermissions=[{
            'IpProtocol': proto,
            'FromPort': start_port,
            'ToPort': end_port,
            'IpRanges': [{
                'CidrIp': ip_range
            }]
        }])
    return response


def ec2_delete_security_group_rule(security_grp_id, security_grp_rule_id):
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.revoke_security_group_egress(
        GroupId=security_grp_id, SecurityGroupRuleIds=[security_grp_rule_id])
    return response


def ec2_get_subnet_list():
    session = init_aws_session()
    ec2 = session.client('ec2')
    response = ec2.describe_subnets()
    return response['Subnets']


def get_running_instances():
    """get all running instances in the region

    Returns:
        list: list of running instances
    """
    print("Getting running instances...")
    print(os.getenv('AWS_REGION'))
    print(os.getenv('AWS_ACCESS_KEY'))
    print(os.getenv('AWS_SECRET_KEY'))
    ec2_client = boto3.client('ec2', region_name=os.getenv('AWS_REGION'),
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")
    return reservations
