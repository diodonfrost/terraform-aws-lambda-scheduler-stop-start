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
    autoscaling_instances = autoscaling.describe_auto_scaling_instances()

    # Retrieve ec2 autoscalinggroup tags
    for group in scalinggroup['AutoScalingGroups']:
        response = autoscaling.describe_tags()
        taglist = response['Tags']

        # Filter ec2 autoscalinggroup with their tag and state
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value:
                # Retrieve autoscaling group name
                autoscaling_name = group['AutoScalingGroupName']

                # Suspend autoscaling group
                if schedule_action == 'stop':
                    autoscaling.suspend_processes(AutoScalingGroupName=autoscaling_name)
                    LOGGER.info("Suspend autoscaling group %s", autoscaling_name)

                    # Terminate all instances in autoscaling group
                    for instance in autoscaling_instances['AutoScalingInstances']:
                        autoscaling.terminate_instance_in_auto_scaling_group(
                            InstanceId=instance['InstanceId'],
                            ShouldDecrementDesiredCapacity=False)
                        LOGGER.info("Terminate autoscaling instance %s", instance['InstanceId'])

                # Resume autoscaling group
                elif schedule_action == 'start':
                    # Resume autoscaling group for startup instances
                    autoscaling.resume_processes(AutoScalingGroupName=autoscaling_name)
                    LOGGER.info("Resume autoscaling group %s", autoscaling_name)
