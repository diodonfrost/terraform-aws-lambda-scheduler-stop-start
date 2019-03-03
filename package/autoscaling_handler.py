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

    # List autoscaling groups and autoscaling instances
    paginator = autoscaling.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate()

    # Initialize instance list
    autoscaling_list = []

    # Retrieve ec2 autoscalinggroup tags
    for page in page_iterator:
        for group in page['AutoScalingGroups']:

            # Check if the right tag is present
            for tag in group['Tags']:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve and add in list autoscaling name
                    autoscaling_name = group['AutoScalingGroupName']
                    autoscaling_list.insert(0, autoscaling_name)

    # Suspend or resume autoscaling group
    for scaling_name in autoscaling_list:

        # Suspend autoscaling group
        if schedule_action == 'stop':
            autoscaling.suspend_processes(AutoScalingGroupName=scaling_name)
            LOGGER.info("Suspend autoscaling group %s", scaling_name)

            # Retrieve instances ID in autoscaling group
            scalinggroup = autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=autoscaling_list)

            # Terminate all instances in autoscaling group
            for instance in scalinggroup['AutoScalingGroups'][0]['Instances']:
                try:
                    autoscaling.terminate_instance_in_auto_scaling_group(
                        InstanceId=instance['InstanceId'],
                        ShouldDecrementDesiredCapacity=False)
                    LOGGER.info("Terminate autoscaling instance %s", instance['InstanceId'])
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ScalingActivityInProgressFault':
                        LOGGER.info("instance %s is in progress", instance['InstanceId'])
                    else:
                        print("Unexpected error: %s" % e)

        # Resume autoscaling group
        elif schedule_action == 'start':
            # Resume autoscaling group for startup instances
            autoscaling.resume_processes(AutoScalingGroupName=scaling_name)
            LOGGER.info("Resume autoscaling group %s", scaling_name)
