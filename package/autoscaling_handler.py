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

                # Retrieve state of autoscaling group
                autoscaling_state = autoscaling.describe_scaling_process_types()

                if schedule_action == 'stop' and next((item for item in \
                autoscaling_state['Processes'] if item["ProcessName"] == "Launch"), False):
                    # Suspend autoscaling group for shutdown instance
                    autoscaling.suspend_processes(AutoScalingGroupName=autoscaling_name)
                    LOGGER.info("Suspend autoscaling group %s", autoscaling_name)

                    # Terminate all instances in autoscaling group
                    for instance in autoscaling_instances['AutoScalingInstances']:
                        autoscaling.terminate_instance_in_auto_scaling_group(\
                        InstanceId=instance['InstanceId'], ShouldDecrementDesiredCapacity=False)
                        LOGGER.info("Terminate autoscaling instance %s", instance['InstanceId'])

                elif schedule_action == 'start' and next((item for item in \
                autoscaling_state['Processes'] if item["ProcessName"] != "Launch"), False):
                    # Resume autoscaling group for startup instances
                    autoscaling.resume_processes(AutoScalingGroupName=autoscaling_name)
                    LOGGER.info("Resume autoscaling group %s", autoscaling_name)
