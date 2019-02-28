""" ec2 instances scheduler """

import logging
import boto3
from botocore.exceptions import ClientError

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def ec2_handler(schedule_action, tag_key, tag_value):
    """
       Aws ec2 scheduler function, stop or
       start ec2 instances by using the tag defined.
    """

    # Define the connection
    ec2 = boto3.client('ec2')

    # Initialize instance list
    instance_list = []

    # List instances with specific tag
    reservations = ec2.describe_instances(
        Filters=[{'Name': 'tag:'+tag_key, 'Values': [tag_value]},
                 {'Name': 'instance-state-name', 'Values': ['pending',
                                                            'running',
                                                            'stopping',
                                                            'stopped']}])

    # Retrieve ec2 instances tags
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:

            # Retrieve ec2 instance id and add in list
            instance_id = instance['InstanceId']
            instance_list.insert(0, instance_id)

    # Stop ec2 instances in list
    if schedule_action == 'stop':
        try:
            ec2.stop_instances(InstanceIds=instance_list)
            LOGGER.info("Stop instances %s", instance_list)
        except ClientError:
            print('No instance found')

    # Start ec2 instances in list
    elif schedule_action == 'start':
        try:
            ec2.start_instances(InstanceIds=instance_list)
            LOGGER.info("Start instances %s", instance_list)
        except ClientError:
            print('No instance found')
