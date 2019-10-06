# -*- coding: utf-8 -*-

"""Autoscaling instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


class AutoscalingScheduler:
    """Abstract autoscaling scheduler in a class."""

    def __init__(self):
        """Initialize autoscaling scheduler."""
        #: Initialize aws autoscaling resource
        self.asg = boto3.client("autoscaling")
        #: Initialize aws ec2 resource
        self.ec2 = boto3.client("ec2")

    def stop(self, tag_key, tag_value):
        """Aws autoscaling suspend function.

        Suspend autoscaling group and stop its instances
        with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        asg_list = self.list_groups(tag_key, tag_value)
        instance_list = self.list_instances(asg_list)

        for asg_name in asg_list:
            try:
                self.asg.suspend_processes(AutoScalingGroupName=asg_name)
                print("Suspend autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        # Stop autoscaling instance
        for ec2_instance in instance_list:
            try:
                self.ec2.stop_instances(InstanceIds=[ec2_instance])
                print("Stop autoscaling instances {0}".format(ec2_instance))
            except ClientError as e:
                if e.response["Error"]["Code"] == "UnsupportedOperation":
                    logging.warning("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def start(self, tag_key, tag_value):
        """Aws autoscaling resume function.

        Resume autoscaling group and start its instances
        with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        asg_list = self.list_groups(tag_key, tag_value)
        instance_list = self.list_instances(asg_list)

        for asg_name in asg_list:
            try:
                self.asg.resume_processes(AutoScalingGroupName=asg_name)
                print("Resume autoscaling group {0}".format(asg_name))
            except ClientError as e:
                logging.error("Unexpected error: %s", e)

        # Start autoscaling instance
        for ec2_instance in instance_list:
            try:
                self.ec2.start_instances(InstanceIds=[ec2_instance])
                print("Start autoscaling instances {0}".format(ec2_instance))
            except ClientError as e:
                if e.response["Error"]["Code"] == "IncorrectInstanceState":
                    logging.warning("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def list_groups(self, tag_key, tag_value):
        """Aws autoscaling list function.

        List name of all autoscaling groups with
        specific tag and return it in list.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :return list asg_list:
            The names of the Auto Scaling groups
        """
        asg_list = []
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate():
            for group in page["AutoScalingGroups"]:
                for tag in group["Tags"]:
                    if tag["Key"] == tag_key and tag["Value"] == tag_value:
                        asg_list.append(group["AutoScalingGroupName"])
        return asg_list

    def list_instances(self, asg_list):
        """Aws autoscaling instance list function.

        List name of all instances in the autoscaling groups
        and return it in list.

        :param list asg_list:
            The names of the Auto Scaling groups.

        :yield Iterator[str]:
            The names of the instances in Auto Scaling groups.
        """
        if not asg_list:
            yield from []
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate(AutoScalingGroupNames=asg_list):
            for scalinggroup in page["AutoScalingGroups"]:
                for instance in scalinggroup["Instances"]:
                    yield instance["InstanceId"]
