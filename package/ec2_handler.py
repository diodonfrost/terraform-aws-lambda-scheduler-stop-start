# -*- coding: utf-8 -*-

"""ec2 instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


def ec2_schedule(schedule_action, tag_key, tag_value):
    """Aws ec2 scheduler function.

    Stop or start ec2 instances by using the tag defined.
    """
    if schedule_action == "stop":
        ec2_stop_instances(tag_key, tag_value)
    elif schedule_action == "start":
        ec2_start_instances(tag_key, tag_value)
    else:
        logging.error("Bad scheduler action")


def ec2_stop_instances(tag_key, tag_value):
    """Aws ec2 stop instance function.

    Shuting donw ec2 instance with defined tag.
    """
    ec2 = boto3.client("ec2")

    for ec2_instance in ec2_list_instances(tag_key, tag_value):
        try:
            ec2.stop_instances(InstanceIds=[ec2_instance])
            print("Stop instances {0}".format(ec2_instance))
        except ClientError as e:
            if e.response["Error"]["Code"] == "UnsupportedOperation":
                logging.warning("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def ec2_start_instances(tag_key, tag_value):
    """Aws ec2 start instance function.

    Starting up ec2 instance with defined tag.
    """
    ec2 = boto3.client("ec2")

    for ec2_instance in ec2_list_instances(tag_key, tag_value):
        try:
            ec2.start_instances(InstanceIds=[ec2_instance])
            print("Start instances {0}".format(ec2_instance))
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "UnsupportedOperation":
                logging.warning("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def ec2_list_instances(tag_key, tag_value):
    """Aws ec2 instance list function.

    List name of all ec2 instances all ec2 instances
    with specific tag and return it in list.
    """
    instance_list = []
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_instances")
    page_iterator = paginator.paginate(
        Filters=[
            {"Name": "tag:" + tag_key, "Values": [tag_value]},
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "stopping", "stopped"],
            },
        ]
    )

    for page in page_iterator:
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instance_list.append(instance["InstanceId"])
    return instance_list
