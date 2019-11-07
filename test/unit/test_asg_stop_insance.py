"""Tests for the autoscaling group stop function."""

import boto3

from moto import mock_autoscaling, mock_ec2

from package.autoscaling_handler import AutoscalingScheduler

from .utils import launch_asg


@mock_ec2
@mock_autoscaling
def test_asg_instance_stop_with_tag():
    """Verify autoscaling instances with defined aws tag are stopped."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"
    client = boto3.client("ec2", region_name=aws_region)

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    asg_scheduler.stop(tag_key, tag_value)
    asg_instance = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(asg_instance) == 3
    for i in range(0, 3):
        instance = asg_instance[i]
        assert instance["State"] == {"Code": 80, "Name": "stopped"}


@mock_ec2
@mock_autoscaling
def test_asg_instance_stop_with_bad_tag():
    """Verify autoscaling instances with defined aws tag are not stopped."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"
    client = boto3.client("ec2", region_name=aws_region)

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    asg_scheduler.stop("badtagkey", "badtagvalue")
    asg_instance = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(asg_instance) == 3
    for i in range(0, 3):
        instance = asg_instance[i]
        assert instance["State"] == {"Code": 16, "Name": "running"}
