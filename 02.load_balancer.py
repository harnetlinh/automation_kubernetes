import os
from dotenv import load_dotenv
import pprint
from libs import *
import time
load_dotenv()

def create_instance(ec2, security_group_ids, type_ = 'NA', num_instances =1):

    if type_ == 'master' or type_ == 'slave':
       
        instance = ec2.create_instances(
        #change ImageId to your ImageId
        ImageId = 'ami-0a5866d87afdfdfd3',
        MinCount = num_instances,
        MaxCount = num_instances,
        InstanceType = 't2.medium',
        #change Keyname to your KeyName
        KeyName = os.getenv('AWS_PEM_KEY'),
        #change SecurityGroupIds to your SecurityGroupIds
        SecurityGroupIds=security_group_ids,
        )
        # instance[0].wait_until_running()           
        # instance[0].reload()
        return instance

    else:
        return None


sec_group = []

# =================== [1] Get Security
# find a security group that allows port 80 and tcp
security_groups = ec2_get_security_group_list()
for security_group in security_groups:
    security_group_ip_perms = security_group['IpPermissions']
    for security_group_ip_perm in security_group_ip_perms:
        if security_group_ip_perm['IpProtocol'] == 'tcp' and security_group_ip_perm['FromPort'] == 80:
            vpc_id = security_group['VpcId']
            security_group_id = security_group['GroupId']
            sec_group.append(security_group)
            break

# =================== [2] Get Subnet
# find subnet and VPC ID associated with security group
subnet_list = ec2_get_subnet_list()
subnet_id_list = []
for subnet in subnet_list:
    if subnet['VpcId'] == vpc_id:
        subnet_id_list.append(subnet['SubnetId'])

print (subnet_id_list, vpc_id, security_group_id)

# =================== [3] Create Target
# Create a target group
target_group = elb_create_target_group('unbiased-coder-target-group', vpc_id)
target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']

# =================== [4] Create Balancer
session = init_aws_session()
elb = session.client('elbv2')

response = elb.create_load_balancer(
    Name='UnbiasedCoderLoadBalancer',
    Subnets = subnet_id_list,
    SecurityGroups=[
        security_group_id,
    ],

    Scheme='internal',
    
    Type='application',
    IpAddressType='ipv4',
)
pprint.pprint(response)


# session = init_aws_session()
# elb = session.client('elbv2')

# =================== [5] Create Instances
security_group_ids = [sg['GroupId'] for sg in sec_group]
ec2 = boto3.resource('ec2', region_name='ap-northeast-1',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

ins_master = create_instance(ec2, security_group_ids, type_  = 'master')
ins_slave = create_instance(ec2, security_group_ids, type_  = 'slave', num_instances = 3)
time.sleep(30)
reserve = get_running_instances()

# =================== [6] Create Target list
targets_group = []
for reservation in reserve:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            temp_ = {}
            temp_['Id'] = str(instance_id)
            targets_group.append(temp_)
        

response = elb.register_targets(
    TargetGroupArn=target_group_arn,
    Targets= targets_group
)

print(response)
response = elb.describe_load_balancers()
pprint.pprint(response['LoadBalancers'][0]['LoadBalancerArn'])

response = elb.create_listener(
    DefaultActions=[
        {
            'TargetGroupArn': target_group_arn,
            'Type': 'forward',
        },
    ],
    LoadBalancerArn= response['LoadBalancers'][0]['LoadBalancerArn'],
    Port=80,
    Protocol='HTTP',
)

print(response)