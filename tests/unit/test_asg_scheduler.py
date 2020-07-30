"""Tests for the autoscaling group scheduler class."""

import boto3

from moto import mock_autoscaling, mock_cloudwatch, mock_ec2

from package.scheduler.autoscaling_handler import AutoscalingScheduler
from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler

from .utils import launch_asg

import pytest


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count", [
        ("eu-west-1", "tostop", "true", 1),
        ("eu-west-2", "tostop", "true", 1),
        ("eu-west-2", "badtagkey", "badtagvalue", 0),
    ]
)
@mock_autoscaling
def test_list_autoscaling_group(aws_region, tag_key, tag_value, result_count):
    """Verify list autoscaling group function."""
    launch_asg(aws_region, "tostop", "true")
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_groups(tag_key, tag_value)
    assert len(list(taglist)) == result_count


@pytest.mark.parametrize(
    "aws_region, asg_name, result_count", [
        ("eu-west-1", ["asg-test"], 3),
        ("eu-west-2", ["asg-test"], 3),
        ("eu-west-2", [], 0),
    ]
)
@mock_ec2
@mock_autoscaling
def test_list_autoscaling_instance(aws_region, asg_name, result_count):
    """Verify list autoscaling instance function"""
    launch_asg(aws_region, "tostop", "true")
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_instances(asg_name)
    assert len(list(taglist)) == result_count


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count", [
        ("eu-west-1", "tostop", "true", {"Code": 80, "Name": "stopped"}),
        ("eu-west-2", "tostop", "true", {"Code": 80, "Name": "stopped"}),
        ("eu-west-2", "badtagkey", "badtagvalue", {"Code": 16, "Name": "running"}),
    ]
)
@mock_ec2
@mock_autoscaling
@mock_cloudwatch
def test_asg_instance_stop(aws_region, tag_key, tag_value, result_count):
    """Verify autoscaling instances stop function."""
    client = boto3.client("ec2", region_name=aws_region)

    launch_asg(aws_region, "tostop", "true")
    asg_scheduler = AutoscalingScheduler(aws_region)
    asg_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
    asg_scheduler.stop(tag_key, tag_value)
    asg_instance = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(asg_instance) == 3
    for instance in asg_instance:
        assert instance["State"] == result_count
