# -*- coding: utf-8 -*-

"""Tests for the ec2 scheduler."""

import boto3

from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler
from package.scheduler.instance_handler import InstanceScheduler

from .fixture import launch_ec2_instances

import pytest


@pytest.mark.parametrize(
    "aws_region, instance_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            {"Code": 80, "Name": "stopped"},
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            {"Code": 16, "Name": "running"},
        ),
    ],
)
def test_stop_ec2_scheduler(aws_region, instance_tag, scheduler_tag, result_count):
    """Verify stop ec2 scheduler class method."""
    client = boto3.client("ec2", region_name=aws_region)
    tag_key = instance_tag[0]["Key"]
    tag_value = "".join(instance_tag[0]["Values"])
    instances = launch_ec2_instances(2, aws_region, tag_key, tag_value)
    instance_ids = [x["InstanceId"] for x in instances["Instances"]]

    try:
        client.get_waiter("instance_running").wait(InstanceIds=instance_ids)
        ec2_scheduler = InstanceScheduler(aws_region)
        ec2_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
        ec2_scheduler.stop(scheduler_tag)
        if scheduler_tag == instance_tag:
            client.get_waiter("instance_stopped").wait(InstanceIds=instance_ids)

        ec2_describe = client.describe_instances(InstanceIds=instance_ids)
        for ec2 in ec2_describe["Reservations"][0]["Instances"]:
            assert ec2["State"] == result_count
    finally:
        # Clean aws account
        client.terminate_instances(InstanceIds=instance_ids)


@pytest.mark.parametrize(
    "aws_region, instance_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "tostop-ec2-test-2", "Values": ["true"]}],
            [{"Key": "tostop-ec2-test-2", "Values": ["true"]}],
            {"Code": 16, "Name": "running"},
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "tostop-ec2-test-2", "Values": ["true"]}],
            {"Code": 80, "Name": "stopped"},
        ),
    ],
)
def test_start_ec2_scheduler(aws_region, instance_tag, scheduler_tag, result_count):
    """Verify start ec2 scheduler class method."""
    client = boto3.client("ec2", region_name=aws_region)
    tag_key = instance_tag[0]["Key"]
    tag_value = "".join(instance_tag[0]["Values"])
    instances = launch_ec2_instances(2, aws_region, tag_key, tag_value)
    instance_ids = [x["InstanceId"] for x in instances["Instances"]]

    try:
        client.get_waiter("instance_running").wait(InstanceIds=instance_ids)
        client.stop_instances(InstanceIds=instance_ids)
        client.get_waiter("instance_stopped").wait(InstanceIds=instance_ids)
        ec2_scheduler = InstanceScheduler(aws_region)
        ec2_scheduler.cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
        ec2_scheduler.start(scheduler_tag)
        if scheduler_tag == instance_tag:
            client.get_waiter("instance_running").wait(InstanceIds=instance_ids)

        ec2_describe = client.describe_instances(InstanceIds=instance_ids)
        for ec2 in ec2_describe["Reservations"][0]["Instances"]:
            assert ec2["State"] == result_count
    finally:
        # Clean aws account
        client.terminate_instances(InstanceIds=instance_ids)
