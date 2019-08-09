# -*- coding: utf-8 -*-

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
    asg_list = autoscaling_list_groups(tag_key, tag_value)
    instance_list = autoscaling_list_instances(asg_list)

    # Suspend autoscaling group and stop all its instances
    if schedule_action == "stop":
        for asg_name in asg_list:
            try:
                autoscaling.suspend_processes(AutoScalingGroupName=asg_name)
                print("Suspend autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for ec2_instance in instance_list:
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
        for asg_name in asg_list:
            try:
                autoscaling.resume_processes(AutoScalingGroupName=asg_name)
                print("Resume autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        for ec2_instance in instance_list:
            try:
                ec2.start_instances(InstanceIds=[ec2_instance])
                print("Start autoscaling instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "IncorrectInstanceState":
                    logging.info(
                        "The instance %s is not in a state from which"
                        "it can be started", ec2_instance
                    )
                else:
                    logging.error("Unexpected error: %s", e)


def autoscaling_list_groups(tag_key, tag_value):
    """Aws autoscaling list function.

    List name of all autoscaling groups with
    specific tag and return it in list.
    """
    asg_list = []
    autoscaling = boto3.client("autoscaling")
    paginator = autoscaling.get_paginator("describe_auto_scaling_groups")

    for page in paginator.paginate():
        for group in page["AutoScalingGroups"]:
            for tag in group["Tags"]:
                if tag["Key"] == tag_key and tag["Value"] == tag_value:
                    autoscaling_group = group["AutoScalingGroupName"]
                    asg_list.insert(0, autoscaling_group)
    return asg_list


def autoscaling_list_instances(asg_list):
    """Aws autoscaling instance list function.

    List name of all instances in the autoscaling groups
    and return it in list.
    """
    if not asg_list:
        return []
    asg_instance_list = []
    autoscaling = boto3.client("autoscaling")
    paginator = autoscaling.get_paginator("describe_auto_scaling_groups")

    for page in paginator.paginate(AutoScalingGroupNames=asg_list):
        for scalinggroup in page["AutoScalingGroups"]:
            for instance in scalinggroup["Instances"]:
                asg_instance = instance["InstanceId"]
                asg_instance_list.insert(0, asg_instance)
    return asg_instance_list
