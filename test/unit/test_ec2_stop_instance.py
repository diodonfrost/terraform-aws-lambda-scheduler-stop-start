"""Tests for the ec2 stop function."""

import boto3

from moto import mock_ec2

from package.ec2_handler import Ec2Scheduler

from .utils import launch_ec2_instances


@mock_ec2
def test_ec2_stop_instance_with_tag():
    """Verify ec2 instances with defined aws tag are stopped."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"
    client = boto3.client("ec2", region_name=aws_region)

    launch_ec2_instances(3, aws_region, tag_key, tag_value)
    ec2_scheduler = Ec2Scheduler(aws_region)
    ec2_scheduler.stop(tag_key, tag_value)
    instances = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(instances) == 3
    for instance in instances:
        assert instance["State"] == {"Code": 80, "Name": "stopped"}


@mock_ec2
def test_ec2_stop_instance_with_bad_tag():
    """Verify ec2 instances with bad aws tag are not stopped."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"
    client = boto3.client("ec2", region_name=aws_region)

    launch_ec2_instances(3, aws_region, tag_key, tag_value)
    ec2_scheduler = Ec2Scheduler(aws_region)
    ec2_scheduler.stop("badtagkey", "badtagvalue")
    instances = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(instances) == 3
    for instance in instances:
        assert instance["State"] == {"Code": 16, "Name": "running"}
