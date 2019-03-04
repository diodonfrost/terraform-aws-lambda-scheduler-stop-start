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

    # Retrieve instance list
    ec2_instance_list = ec2_list_instances(tag_key, tag_value)

    # Stop ec2 instances in list
    if schedule_action == 'stop':
        try:
            ec2.stop_instances(InstanceIds=ec2_instance_list)
            LOGGER.info("Stop instances %s", ec2_instance_list)
        except ClientError:
            print('No instance found')

    # Start ec2 instances in list
    elif schedule_action == 'start':
        try:
            ec2.start_instances(InstanceIds=ec2_instance_list)
            LOGGER.info("Start instances %s", ec2_instance_list)
        except ClientError:
            print('No instance found')


def ec2_list_instances(tag_key, tag_value):
    """
       Aws ec2 instance list function, list name of all ec2 instances
       all ec2 instances with specific tag and return it in list.
    """

    # Define the connection
    ec2 = boto3.client('ec2')
    paginator = ec2.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        Filters=[{'Name': 'tag:'+tag_key, 'Values': [tag_value]},
                 {'Name': 'instance-state-name', 'Values': ['pending',
                                                            'running',
                                                            'stopping',
                                                            'stopped']}])

    # Initialize instance list
    instance_list = []

    # Retrieve ec2 instances
    for page in page_iterator:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:

                # Retrieve ec2 instance id and add in list
                instance_id = instance['InstanceId']
                instance_list.insert(0, instance_id)

    return instance_list
