"""Autoscaling instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


def autoscaling_schedule(schedule_action, tag_key, tag_value):
    """Aws autoscaling scheduler function.

    Suspend or resume all autoscaling scaling groups
    by using the defined tag.
    """
    # Define the connection
    autoscaling = boto3.client("autoscaling")
    ec2 = boto3.client("ec2")

    autoscaling_group_list = autoscaling_list_groups(tag_key, tag_value)

    # Retrieve instances ID in autoscaling group
    instance_list = autoscaling_list_instances(autoscaling_group_list)

    # Suspend autoscaling group and terminate all its instances
    if schedule_action == "stop":
        for asg_name in autoscaling_group_list:

            # Suspend autoscaling group
            try:
                autoscaling.suspend_processes(AutoScalingGroupName=asg_name)
                print("Suspend autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for ec2_instance in instance_list:
            # Stop all instances in autoscaling group
            try:
                ec2.stop_instances(InstanceIds=[ec2_instance])
                print("Stop autoscaling instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "UnsupportedOperation":
                    logging.warning(
                        "%s is a spot instance and cannot be stopped by user",
                        ec2_instance,
                    )
                else:
                    logging.error("Unexpected error: %s", e)

    # Resume autoscaling group
    elif schedule_action == "start":
        for asg_name in autoscaling_group_list:

            # Resume autoscaling group
            try:
                autoscaling.resume_processes(AutoScalingGroupName=asg_name)
                print("Resume autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for ec2_instance in instance_list:
            # Start all instances in autoscaling group
            try:
                ec2.start_instances(InstanceIds=[ec2_instance])
                print("Start autoscaling instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "IncorrectInstanceState":
                    logging.info(
                        "The instance %s is not in a state from which"
                        "it can be started",
                        ec2_instance,
                    )
                else:
                    logging.error("Unexpected error: %s", e)


def autoscaling_list_groups(tag_key, tag_value):
    """Aws autoscaling list function.

    List name of all autoscaling groups
    and return it in list.
    """
    # Define the connection
    autoscaling = boto3.client("autoscaling")

    # List autoscaling groups and autoscaling instances
    paginator = autoscaling.get_paginator("describe_auto_scaling_groups")
    page_iterator = paginator.paginate()

    # Initialize autoscaling group list
    autoscaling_group_list = []

    # Retrieve ec2 autoscalinggroup tags
    for page in page_iterator:
        for group in page["AutoScalingGroups"]:

            # Check if the right tag is present
            for tag in group["Tags"]:
                if tag["Key"] == tag_key and tag["Value"] == tag_value:

                    # Retrieve and add in list autoscaling name
                    autoscaling_group = group["AutoScalingGroupName"]
                    autoscaling_group_list.insert(0, autoscaling_group)

    return autoscaling_group_list


def autoscaling_list_instances(autoscaling_group_list):
    """Aws autoscaling instance list function.

    List name of all instances in the autoscaling groups
    and return it in list.
    """
    if not autoscaling_group_list:
        return []

    # Define the connection
    autoscaling = boto3.client("autoscaling")

    # List autoscaling groups and autoscaling instances
    paginator = autoscaling.get_paginator("describe_auto_scaling_groups")
    page_iterator = paginator.paginate(
        AutoScalingGroupNames=autoscaling_group_list
    )

    # Initialize autoscaling instance list
    autoscaling_instance_list = []

    # Retrieve instance in specific autoscaling group
    for page in page_iterator:
        for scalinggroup in page["AutoScalingGroups"]:
            for instance in scalinggroup["Instances"]:

                autoscaling_instance = instance["InstanceId"]
                autoscaling_instance_list.insert(0, autoscaling_instance)

    return autoscaling_instance_list
