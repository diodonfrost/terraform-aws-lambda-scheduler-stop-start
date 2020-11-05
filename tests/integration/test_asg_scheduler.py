# -*- coding: utf-8 -*-

"""Tests for the autoscaling group scheduler."""

import boto3
import time
from random import randint

from package.scheduler.autoscaling_handler import AutoscalingScheduler
from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler

from .fixture import launch_asg

import pytest


@pytest.mark.parametrize(
    "aws_region, asg_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "tostop-asg-test-1", "Values": ["true"]}],
            [{"Key": "tostop-asg-test-1", "Values": ["true"]}],
            10,
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "tostop-asg-test-2", "Values": ["true"]}],
            0,
        ),
    ],
)
def test_stop_asg_scheduler(aws_region, asg_tag, scheduler_tag, result_count):
    """Verify stop asg scheduler class method."""
    client = boto3.client("autoscaling", region_name=aws_region)
    launch_conf_name = "lc-test" + str(randint(0, 1000000000))
    asg_name = "asg-test" + str(randint(0, 1000000000))
    tag_key = asg_tag[0]["Key"]
    tag_value = "".join(asg_tag[0]["Values"])
    launch_asg(aws_region, tag_key, tag_value, launch_conf_name, asg_name)

    try:
        asg_scheduler = AutoscalingScheduler(aws_region)
        asg_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
        asg_scheduler.stop(scheduler_tag)

        suspend_process = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )["AutoScalingGroups"][0]["SuspendedProcesses"]
        assert len([x["ProcessName"] for x in suspend_process]) == result_count
    finally:
        # Clean aws account
        client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name, ForceDelete=True
        )
        client.delete_launch_configuration(LaunchConfigurationName=launch_conf_name)


@pytest.mark.parametrize(
    "aws_region, asg_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "tostop-asg-test-3", "Values": ["true"]}],
            [{"Key": "tostop-asg-test-3", "Values": ["true"]}],
            0,
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "tostop-asg-test-4", "Values": ["true"]}],
            10,
        ),
    ],
)
def test_start_asg_scheduler(aws_region, asg_tag, scheduler_tag, result_count):
    """Verify start asg scheduler class method."""
    client = boto3.client("autoscaling", region_name=aws_region)
    launch_conf_name = "lc-test" + str(randint(0, 1000000000))
    asg_name = "asg-test" + str(randint(0, 1000000000))
    tag_key = asg_tag[0]["Key"]
    tag_value = "".join(asg_tag[0]["Values"])
    launch_asg(aws_region, tag_key, tag_value, launch_conf_name, asg_name)

    try:
        client.suspend_processes(AutoScalingGroupName=asg_name)
        asg_scheduler = AutoscalingScheduler(aws_region)
        asg_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
        asg_scheduler.start(scheduler_tag)

        suspend_process = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )["AutoScalingGroups"][0]["SuspendedProcesses"]
        assert len([x["ProcessName"] for x in suspend_process]) == result_count
    finally:
        # Clean aws account
        client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name, ForceDelete=True
        )
        client.delete_launch_configuration(LaunchConfigurationName=launch_conf_name)
