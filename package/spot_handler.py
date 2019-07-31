"""Spot instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


def spot_schedule(schedule_action, tag_key, tag_value):
    """Aws spot instance scheduler function.

    Terminate spot instances by using the defined tag.
    """
    # Define the connection
    ec2 = boto3.client("ec2")

    # Get spot instance list
    spot_instance_list = spot_list_instances(tag_key, tag_value)

    for spot_instance in spot_instance_list:

        # Terminate spot instances in list
        if schedule_action == "stop":
            try:
                ec2.terminate_instances(InstanceIds=[spot_instance])
                print("Terminate spot instance {0}".format(spot_instance))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)


def spot_list_instances(tag_key, tag_value):
    """Aws ec2 spot instance list function.

    List name of all ec2 spot instances with
    specific tag and return it in list.
    """
    # Define the connection
    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_instances")
    page_iterator = paginator.paginate(
        Filters=[
            {"Name": "tag:" + tag_key, "Values": [tag_value]},
            {"Name": "instance-lifecycle", "Values": ["spot"]},
            {
                "Name": "instance-state-name",
                "Values": ["pending", "running", "stopping", "stopped"],
            },
        ]
    )

    # Initialize instance list
    spot_list = []

    # Retrieve spot instances
    for page in page_iterator:
        for reservation in page["Reservations"]:
            for spot in reservation["Instances"]:

                # Retrieve spot instance id and add in list
                spot_id = spot["InstanceId"]
                spot_list.insert(0, spot_id)

    return spot_list
