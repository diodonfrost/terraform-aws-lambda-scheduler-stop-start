"""Tests for the spot scheduler class."""

import boto3

from moto import mock_cloudwatch, mock_ec2

from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler
from package.scheduler.spot_handler import SpotScheduler

from .utils import launch_ec2_spot

import pytest


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count", [
        ("eu-west-1", "badtagkey", "badtagvalue", 0),
        ("eu-west-2", "badtagkey", "badtagvalue", 0),
    ]
)
@mock_ec2
def test_list_ec2_spot(aws_region, tag_key, tag_value, result_count):
    """Verify list ec2 spot function."""
    launch_ec2_spot(3, aws_region, "tostop", "true")
    spot_list = SpotScheduler(aws_region)
    taglist = spot_list.list_spot(tag_key, tag_value)
    assert len(list(taglist)) == result_count


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count", [
        ("eu-west-2", "badtagkey", "badtagvalue", {"Code": 16, "Name": "running"}),
    ]
)
@mock_ec2
@mock_cloudwatch
def test_terminate_ec2_spot(aws_region, tag_key, tag_value, result_count):
    """Verify terminate ec2 spot instance."""
    client = boto3.client("ec2", region_name=aws_region)

    launch_ec2_spot(3, aws_region, "tostop", "true")
    spot_scheduler = SpotScheduler(aws_region)
    spot_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
    spot_scheduler.terminate(tag_key, tag_value)
    instances = client.describe_instances()["Reservations"][0]["Instances"]
    assert len(instances) == 3
    for instance in instances:
        assert instance["State"] == result_count
