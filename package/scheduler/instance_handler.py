# -*- coding: utf-8 -*-

"""ec2 instances scheduler."""


import boto3

from botocore.exceptions import ClientError

from .exceptions import ec2_exception
from .filter_resources_by_tags import FilterByTags


class InstanceScheduler(object):
    """Abstract ec2 scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ec2 scheduler."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
            self.asg = boto3.client("autoscaling", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")
            self.asg = boto3.client("autoscaling")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, tag_key: str, tag_value: str) -> None:
        """Aws ec2 instance stop function.

        Stop ec2 instances with defined tag and disable its Cloudwatch
        alarms.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        format_tag = [{"Key": tag_key, "Values": [tag_value]}]

        for instance_arn in self.tag_api.get_resources(
            "ec2:instance", format_tag
        ):
            instance_id = instance_arn.split("/")[-1]
            try:
                if not self.asg.describe_auto_scaling_instances(
                    InstanceIds=[instance_id]
                )["AutoScalingInstances"]:
                    self.ec2.stop_instances(InstanceIds=[instance_id])
                    print("Stop instances {0}".format(instance_id))
            except ClientError as exc:
                ec2_exception("instance", instance_id, exc)

    def start(self, tag_key: str, tag_value: str) -> None:
        """Aws ec2 instance start function.

        Start ec2 instances with defined tag

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        format_tag = [{"Key": tag_key, "Values": [tag_value]}]

        for instance_arn in self.tag_api.get_resources(
            "ec2:instance", format_tag
        ):
            instance_id = instance_arn.split("/")[-1]
            try:
                if not self.asg.describe_auto_scaling_instances(
                    InstanceIds=[instance_id]
                )["AutoScalingInstances"]:
                    self.ec2.start_instances(InstanceIds=[instance_id])
                    print("Start instances {0}".format(instance_id))
            except ClientError as exc:
                ec2_exception("instance", instance_id, exc)
