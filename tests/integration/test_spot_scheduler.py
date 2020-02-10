"""Tests for the ec2 scheduler."""

import boto3

from package.scheduler.spot_handler import SpotScheduler

from .fixture import launch_ec2_spot

import pytest


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count",
    [
        (
            "eu-west-1",
            "tostop-spot-test-1",
            "true",
            {"Code": 48, "Name": "terminated"},
        ),
        (
            "eu-west-1",
            "badtagkey",
            "badtagvalue",
            {"Code": 16, "Name": "running"},
        ),
    ],
)
def test_terminate_spot_scheduler(aws_region, tag_key, tag_value, result_count):
    """Verify terminate spot scheduler class method."""
    client = boto3.client("ec2", region_name=aws_region)
    instances = launch_ec2_spot(2, aws_region, tag_key, tag_value)
    instance_ids = [x["InstanceId"] for x in instances["Instances"]]

    try:
        client.get_waiter("instance_running").wait(InstanceIds=instance_ids)
        spot_scheduler = SpotScheduler(aws_region)
        spot_scheduler.terminate("tostop-spot-test-1", "true")
        if tag_key == "tostop-spot-test-1" and tag_value == "true":
            client.get_waiter("instance_terminated").wait(
                InstanceIds=instance_ids
            )

        ec2_describe = client.describe_instances(InstanceIds=instance_ids)
        for ec2 in ec2_describe["Reservations"][0]["Instances"]:
            assert ec2["State"] == result_count
    finally:
        # Clean aws account
        client.terminate_instances(InstanceIds=instance_ids)
