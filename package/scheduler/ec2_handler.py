# -*- coding: utf-8 -*-

"""ec2 instances scheduler."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from .exceptions import ec2_exception


class Ec2Scheduler(object):
    """Abstract ec2 scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize autoscaling scheduler."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def stop(self, tag_key: str, tag_value: str) -> None:
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
            except ClientError as exc:
                ec2_exception("instance", ec2_instance, exc)

    def start(self, tag_key: str, tag_value: str) -> None:
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
            except ClientError as exc:
                ec2_exception("instance", ec2_instance, exc)

    def list_instances(self, tag_key: str, tag_value: str) -> Iterator[str]:
        """Aws ec2 instance list function.

        List name of all ec2 instances all ec2 instances
        with specific tag and return it in list.

        :yield Iterator[str]:
            The Id of ec2 instances
        """
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
                    yield instance["InstanceId"]
