""" autoscaling instances scheduler """

import logging
import boto3

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
    scalinggroup = autoscaling.describe_auto_scaling_groups()

    # Retrieve ec2 autoscalinggroup tags
    for group in scalinggroup['AutoScalingGroups']:

        # Check if the right tag is present
        autoscaling_tag = False
        for tag in group['Tags']:
            if tag['Key'] == tag_key and tag['Value'] == tag_value:
                autoscaling_tag = True

        # Retrieve autoscaling group name
        autoscaling_name = group['AutoScalingGroupName']

        # Suspend autoscaling group if the right tag is present
        if schedule_action == 'stop' and autoscaling_tag:
            autoscaling.suspend_processes(AutoScalingGroupName=autoscaling_name)
            LOGGER.info("Suspend autoscaling group %s", autoscaling_name)

            # Terminate all instances in autoscaling group
            for instance in group['Instances']:
                autoscaling.terminate_instance_in_auto_scaling_group(
                    InstanceId=instance['InstanceId'],
                    ShouldDecrementDesiredCapacity=False)
                LOGGER.info("Terminate autoscaling instance %s", instance['InstanceId'])

        # Resume autoscaling group if the right tag is present
        elif schedule_action == 'start' and autoscaling_tag:
            # Resume autoscaling group for startup instances
            autoscaling.resume_processes(AutoScalingGroupName=autoscaling_name)
            LOGGER.info("Resume autoscaling group %s", autoscaling_name)
