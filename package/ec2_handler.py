# -*- coding: utf-8 -*-

"""ec2 instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


def ec2_schedule(schedule_action, tag_key, tag_value):
    """Aws ec2 scheduler function.

    Stop or start ec2 instances by using the tag defined.
    """
    ec2 = boto3.client("ec2")

    # Stop ec2 instances with defined tag
    for ec2_instance in ec2_list_instances(tag_key, tag_value):
        if schedule_action == "stop":
            try:
                ec2.stop_instances(InstanceIds=[ec2_instance])
                print("Stop instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "UnsupportedOperation":
                    logging.warning(
                        "%s is a spot instance and can not be stopped"
                        "by scheduler",
                        ec2_instance,
                    )
                else:
                    logging.error("Unexpected error: %s", e)

        # Start ec2 instances with defined tag
        elif schedule_action == "start":
            try:
                ec2.start_instances(InstanceIds=[ec2_instance])
                print("Start instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "UnsupportedOperation":
                    logging.warning(
                        "%s is a spot instance and can not be started"
                        "by scheduler",
                        ec2_instance,
                    )
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
                instance_id = instance["InstanceId"]
                instance_list.insert(0, instance_id)
    return instance_list
