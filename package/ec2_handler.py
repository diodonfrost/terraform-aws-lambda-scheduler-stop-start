# -*- coding: utf-8 -*-

"""ec2 instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


class Ec2Scheduler:
    """Abstract ec2 scheduler in a class."""

    def __init__(self):
        """Initialize autoscaling scheduler."""
        #: Initialize aws ec2 resource
        self.ec2 = boto3.client("ec2")

    def stop_instances(self, tag_key, tag_value):
        """Aws ec2 instance stop function.

        Stop ec2 instances with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for ec2_instance in self.list_instances(tag_key, tag_value):
            try:
                self.ec2.stop_instances(InstanceIds=[ec2_instance])
                print("Stop instances {0}".format(ec2_instance))
            except ClientError as e:
                if e.response["Error"]["Code"] == "UnsupportedOperation":
                    logging.warning("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def start_instances(self, tag_key, tag_value):
        """Aws ec2 instance start function.

        Start ec2 instances with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for ec2_instance in self.list_instances(tag_key, tag_value):
            try:
                self.ec2.start_instances(InstanceIds=[ec2_instance])
                print("Start instances {0}".format(ec2_instance))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "UnsupportedOperation":
                    logging.warning("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def list_instances(self, tag_key, tag_value):
        """Aws ec2 instance list function.

        List name of all ec2 instances all ec2 instances
        with specific tag and return it in list.
        """
        instance_list = []
        paginator = self.ec2.get_paginator("describe_instances")
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
