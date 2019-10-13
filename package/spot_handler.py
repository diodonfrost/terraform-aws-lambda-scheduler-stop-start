# -*- coding: utf-8 -*-

"""Spot instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


class SpotScheduler(object):
    """Abstract spot scheduler in a class."""

    def __init__(self):
        """Initialize autoscaling scheduler."""
        #: Initialize aws ec2 resource
        self.ec2 = boto3.client("ec2")

    def terminate(self, tag_key, tag_value):
        """Aws spot instance scheduler function.

        Terminate spot instances by using the defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for spot_instance in self.list_spot(tag_key, tag_value):
            try:
                self.ec2.terminate_instances(InstanceIds=[spot_instance])
                print("Terminate spot instance {0}".format(spot_instance))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

    def list_spot(self, tag_key, tag_value):
        """Aws ec2 spot instance list function.

        List name of all ec2 spot instances with
        specific tag and return it in list.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :yield Iterator[str]:
            The Id of the spot instances
        """
        paginator = self.ec2.get_paginator("describe_instances")
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

        for page in page_iterator:
            for reservation in page["Reservations"]:
                for spot in reservation["Instances"]:
                    yield spot["InstanceId"]
