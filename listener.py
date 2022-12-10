import pprint
from libs import *

# response = elb.describe_load_balancers()

# pprint.pprint(response['LoadBalancers']['AvailabilityZones'][0]['LoadBalancerArn'])

session = init_aws_session()
elb = session.client('elbv2')

response = elb.describe_load_balancers()
pprint.pprint(response['LoadBalancers']['AvailabilityZones'][0]['LoadBalancerArn'])

response = elb.create_listener(
    DefaultActions=[
        {
            'TargetGroupArn': target_group_arn,
            'Type': 'forward',
        },
    ],
    LoadBalancerArn= response['LoadBalancers']['AvailabilityZones'][0]['LoadBalancerArn']
    Port=80,
    Protocol='HTTP',
)

print(response)