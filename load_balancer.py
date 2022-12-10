import pprint
from libs import *

# find a security group that allows port 80 and tcp
security_groups = ec2_get_security_group_list()
for security_group in security_groups:
    security_group_ip_perms = security_group['IpPermissions']
    for security_group_ip_perm in security_group_ip_perms:
        if security_group_ip_perm['IpProtocol'] == 'tcp' and security_group_ip_perm['FromPort'] == 80:
            vpc_id = security_group['VpcId']
            security_group_id = security_group['GroupId']
            break

# find subnet and VPC ID associated with security group
subnet_list = ec2_get_subnet_list()
subnet_id_list = []
for subnet in subnet_list:
    if subnet['VpcId'] == vpc_id:
        subnet_id_list.append(subnet['SubnetId'])

print (subnet_id_list, vpc_id, security_group_id)

# Create a target group
target_group = elb_create_target_group('unbiased-coder-target-group', vpc_id)
target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']

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

# response = ecs.register_targets(
#     TargetGroupArn=target_group_arn,
#     Targets=[
#         {
#             'Id': 'string',
#             'Port': 123,
#             'AvailabilityZone': 'string'
#         },
#     ]
)

# response = client.register_targets(
#     TargetGroupArn='arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067',
#     Targets=[
#         {
#             'Id': 'i-80c8dd94',
#         },
#         {
#             'Id': 'i-ceddcd4d',
#         },
#     ],
# )