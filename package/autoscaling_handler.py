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
    if schedule_action == "stop":
        asg_stop_groups(tag_key, tag_value)
    elif schedule_action == "start":
        asg_start_groups(tag_key, tag_value)
    else:
        logging.error("Bad scheduler action")


def asg_stop_groups(tag_key, tag_value):
    """Aws autoscaling suspend function.

    Suspend autoscaling group and stop its instances
    with defined tag.
    """
    autoscaling = boto3.client("autoscaling")
    ec2 = boto3.client("ec2")
    asg_list = asg_list_groups(tag_key, tag_value)
    instance_list = asg_list_instances(asg_list)

    for asg_name in asg_list:
        try:
            autoscaling.suspend_processes(AutoScalingGroupName=asg_name)
            print("Suspend autoscaling group {0}".format(asg_name))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # Stop autoscaling instance
    for ec2_instance in instance_list:
        try:
            ec2.stop_instances(InstanceIds=[ec2_instance])
            print("Stop autoscaling instances {0}".format(ec2_instance))
        except ClientError as e:
            if e.response["Error"]["Code"] == "UnsupportedOperation":
                logging.warning("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def asg_start_groups(tag_key, tag_value):
    """Aws autoscaling resume function.

    Resume autoscaling group and start its instances
    with defined tag.
    """
    autoscaling = boto3.client("autoscaling")
    ec2 = boto3.client("ec2")
    asg_list = asg_list_groups(tag_key, tag_value)
    instance_list = asg_list_instances(asg_list)

    for asg_name in asg_list:
        try:
            autoscaling.resume_processes(AutoScalingGroupName=asg_name)
            print("Resume autoscaling group {0}".format(asg_name))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)

    # Start autoscaling instance
    for ec2_instance in instance_list:
        try:
            ec2.start_instances(InstanceIds=[ec2_instance])
            print("Start autoscaling instances {0}".format(ec2_instance))
        except ClientError as e:
            if e.response["Error"]["Code"] == "IncorrectInstanceState":
                logging.warning("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def asg_list_groups(tag_key, tag_value):
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


def asg_list_instances(asg_list):
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
