"""Tests for the autoscaling group scheduler."""

import boto3
import time

from package.autoscaling_handler import AutoscalingScheduler

from .fixture import launch_asg

import pytest


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count",
    [
        ("eu-west-1", "tostop-asg-test-1", "true", 9),
        ("eu-west-1", "badtagkey", "badtagvalue", 0),
    ],
)
def test_stop_asg_scheduler(aws_region, tag_key, tag_value, result_count):
    """Verify stop asg scheduler class method."""
    client = boto3.client("autoscaling", region_name=aws_region)
    launch_conf_name = "lc-test" + str(time.time())[11:]
    asg_name = "asg-test" + str(time.time())[11:]
    launch_asg(aws_region, tag_key, tag_value, launch_conf_name, asg_name)

    try:
        asg_scheduler = AutoscalingScheduler(aws_region)
        asg_scheduler.stop("tostop-asg-test-1", "true")

        suspend_process = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )["AutoScalingGroups"][0]["SuspendedProcesses"]
        assert len([x["ProcessName"] for x in suspend_process]) == result_count
    finally:
        # Clean aws account
        client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name, ForceDelete=True
        )
        client.delete_launch_configuration(
            LaunchConfigurationName=launch_conf_name
        )


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count",
    [
        ("eu-west-1", "tostop-asg-test-2", "true", 0),
        ("eu-west-1", "badtagkey", "badtagvalue", 9),
    ],
)
def test_start_asg_scheduler(aws_region, tag_key, tag_value, result_count):
    """Verify start asg scheduler class method."""
    client = boto3.client("autoscaling", region_name=aws_region)
    launch_conf_name = "lc-test" + str(time.time())[11:]
    asg_name = "asg-test" + str(time.time())[11:]
    launch_asg(aws_region, tag_key, tag_value, launch_conf_name, asg_name)

    try:
        client.suspend_processes(AutoScalingGroupName=asg_name)
        asg_scheduler = AutoscalingScheduler(aws_region)
        asg_scheduler.start("tostop-asg-test-2", "true")

        suspend_process = client.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )["AutoScalingGroups"][0]["SuspendedProcesses"]
        assert len([x["ProcessName"] for x in suspend_process]) == result_count
    finally:
        # Clean aws account
        client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_name, ForceDelete=True
        )
        client.delete_launch_configuration(
            LaunchConfigurationName=launch_conf_name
        )
