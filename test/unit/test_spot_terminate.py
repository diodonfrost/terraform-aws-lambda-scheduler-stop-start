"""Tests for the spot terminate function."""

import boto3

from moto import mock_ec2

from package.spot_handler import SpotScheduler

from .utils import launch_ec2_spot


@mock_ec2
def test_ec2_terminate_spot_with_no_tag():
    """Verify ec2 spot instances with no aws tag are not terminated."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"
    client = boto3.client("ec2", region_name=aws_region)

    launch_ec2_spot(1, aws_region)
    dpot_scheduler = SpotScheduler(aws_region)
    dpot_scheduler.terminate(tag_key, tag_value)
    instances = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(instances) == 1
    assert instances[0]["State"] == {"Code": 16, "Name": "running"}
