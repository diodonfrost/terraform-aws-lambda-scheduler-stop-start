""" autoscaling instances scheduler """

import logging
import boto3
from botocore.exceptions import ClientError

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def autoscaling_handler(schedule_action, tag_key, tag_value):
    """
       Aws autoscaling scheduler function, suspend or
       resume all scaling processes by using the tag defined.
    """

    # Define the connection
    autoscaling = boto3.client('autoscaling')
    ec2 = boto3.client('ec2')

    autoscaling_group_list = autoscaling_list_groups(tag_key, tag_value)

    # Suspend autoscaling group and terminate all its instances
    if schedule_action == 'stop':
        for scaling_name in autoscaling_group_list:

            # Suspend autoscaling group
            autoscaling.suspend_processes(AutoScalingGroupName=scaling_name)
            LOGGER.info("Suspend autoscaling group %s", scaling_name)

        # Retrieve instances ID in autoscaling group
        instance_list = autoscaling_list_instances(autoscaling_group_list)

        # Terminate all instances in autoscaling group
        try:
            ec2.terminate_instances(InstanceIds=instance_list)
            LOGGER.info("Terminate autoscaling instances %s", instance_list)
        except ClientError:
            print('No instance found')

    # Resume autoscaling group
    elif schedule_action == 'start':
        for scaling_name in autoscaling_group_list:

            # Resume autoscaling group
            autoscaling.resume_processes(AutoScalingGroupName=scaling_name)
            LOGGER.info("Resume autoscaling group %s", scaling_name)


def autoscaling_list_groups(tag_key, tag_value):
    """
       Aws autoscaling list function, list name of
       all autoscaling group and return it in list.
    """

    # Define the connection
    autoscaling = boto3.client('autoscaling')

    # List autoscaling groups and autoscaling instances
    paginator = autoscaling.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate()

    # Initialize autoscaling group list
    autoscaling_group_list = []

    # Retrieve ec2 autoscalinggroup tags
    for page in page_iterator:
        for group in page['AutoScalingGroups']:

            # Check if the right tag is present
            for tag in group['Tags']:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve and add in list autoscaling name
                    autoscaling_group = group['AutoScalingGroupName']
                    autoscaling_group_list.insert(0, autoscaling_group)

    return autoscaling_group_list


def autoscaling_list_instances(autoscaling_group_list):
    """
       Aws autoscaling instance list function, list name of
       all autoscaling instances and return it in list.
    """

    # Define the connection
    autoscaling = boto3.client('autoscaling')

    # List autoscaling groups and autoscaling instances
    paginator = autoscaling.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate(
        AutoScalingGroupNames=autoscaling_group_list)

    # Initialize autoscaling instance list
    autoscaling_instance_list = []

    # Retrieve instance in specific autoscaling group
    for page in page_iterator:
        for scalinggroup in page['AutoScalingGroups']:
            for instance in scalinggroup['Instances']:

                autoscaling_instance = instance['InstanceId']
                autoscaling_instance_list.insert(0, autoscaling_instance)

    return autoscaling_instance_list
