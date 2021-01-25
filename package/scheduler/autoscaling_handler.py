# -*- coding: utf-8 -*-

"""Autoscaling instances scheduler."""

from typing import Dict, Iterator, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import ec2_exception
from scheduler.waiters import AwsWaiters


class AutoscalingScheduler(object):
    """Abstract autoscaling scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize autoscaling scheduler."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
            self.asg = boto3.client("autoscaling", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")
            self.asg = boto3.client("autoscaling")
        self.waiter = AwsWaiters(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws autoscaling suspend function.

        Suspend autoscaling group and stop its instances
        with defined tag.

        :param list[map] aws_tags:
            Aws tags to use for filter resources.
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        tag_key = aws_tags[0]["Key"]
        tag_value = "".join(aws_tags[0]["Values"])
        asg_name_list = self.list_groups(tag_key, tag_value)
        instance_id_list = self.list_instances(asg_name_list)

        for asg_name in asg_name_list:
            try:
                self.asg.suspend_processes(AutoScalingGroupName=asg_name)
                print("Suspend autoscaling group {0}".format(asg_name))
            except ClientError as exc:
                ec2_exception("instance", asg_name, exc)

        # Stop autoscaling instance
        for instance_id in instance_id_list:
            try:
                self.ec2.stop_instances(InstanceIds=[instance_id])
                print("Stop autoscaling instances {0}".format(instance_id))
            except ClientError as exc:
                ec2_exception("autoscaling group", instance_id, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws autoscaling resume function.

        Resume autoscaling group and start its instances
        with defined tag.

        :param list[map] aws_tags:
            Aws tags to use for filter resources
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        tag_key = aws_tags[0]["Key"]
        tag_value = "".join(aws_tags[0]["Values"])
        asg_name_list = self.list_groups(tag_key, tag_value)
        instance_id_list = self.list_instances(asg_name_list)
        instance_running_ids = []

        # Start autoscaling instance
        for instance_id in instance_id_list:
            try:
                self.ec2.start_instances(InstanceIds=[instance_id])
                print("Start autoscaling instances {0}".format(instance_id))
            except ClientError as exc:
                ec2_exception("instance", instance_id, exc)
            else:
                instance_running_ids.append(instance_id)

        self.waiter.instance_running(instance_ids=instance_running_ids)

        for asg_name in asg_name_list:
            try:
                self.asg.resume_processes(AutoScalingGroupName=asg_name)
                print("Resume autoscaling group {0}".format(asg_name))
            except ClientError as exc:
                ec2_exception("autoscaling group", asg_name, exc)

    def list_groups(self, tag_key: str, tag_value: str) -> List[str]:
        """Aws autoscaling list function.

        List name of all autoscaling groups with
        specific tag and return it in list.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :return list asg_name_list:
            The names of the Auto Scaling groups
        """
        asg_name_list = []
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate():
            for group in page["AutoScalingGroups"]:
                for tag in group["Tags"]:
                    if tag["Key"] == tag_key and tag["Value"] == tag_value:
                        asg_name_list.append(group["AutoScalingGroupName"])
        return asg_name_list

    def list_instances(self, asg_name_list: List[str]) -> Iterator[str]:
        """Aws autoscaling instance list function.

        List name of all instances in the autoscaling groups
        and return it in list.

        :param list asg_name_list:
            The names of the Auto Scaling groups.

        :yield Iterator[str]:
            The names of the instances in Auto Scaling groups.
        """
        if not asg_name_list:
            return iter([])
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate(AutoScalingGroupNames=asg_name_list):
            for scalinggroup in page["AutoScalingGroups"]:
                for instance in scalinggroup["Instances"]:
                    yield instance["InstanceId"]
