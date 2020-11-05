# -*- coding: utf-8 -*-

"""Tests for the cloudwatch alarm scheduler."""

import boto3

from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler

from .fixture import create_cloudwatch_alarm

import pytest


@pytest.mark.parametrize(
    "aws_region, cloudwatch_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "cloudwatch-scheduler-test-5", "Values": ["true"]}],
            [{"Key": "cloudwatch-scheduler-test-5", "Values": ["true"]}],
            False,
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "cloudwatch-scheduler-test-6", "Values": ["true"]}],
            True,
        ),
        (
            "eu-west-2",
            [{"Key": "cloudwatch-scheduler-test-7", "Values": ["true"]}],
            [{"Key": "cloudwatch-scheduler-test-7", "Values": ["true"]}],
            False,
        ),
        (
            "eu-west-2",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "cloudwatch-scheduler-test-8", "Values": ["true"]}],
            True,
        ),
    ],
)
def test_stop_cloudwatch_alarms(
    aws_region, cloudwatch_tag, scheduler_tag, result_count
):
    """Verify cloudwatch stop scheduler class method."""
    client = boto3.client("cloudwatch", region_name=aws_region)
    fake_tag = {"Key": "faketag", "Value": "true"}
    alarm_tag = {
        "Key": cloudwatch_tag[0]["Key"],
        "Value": "".join(cloudwatch_tag[0]["Values"]),
    }
    try:
        alarm1 = create_cloudwatch_alarm(aws_region, fake_tag)
        alarm2 = create_cloudwatch_alarm(aws_region, alarm_tag)
        cloudwatch_scheduler = CloudWatchAlarmScheduler(aws_region)
        cloudwatch_scheduler.stop(scheduler_tag)
        alarm1_status = client.describe_alarms(AlarmNames=[alarm1])
        alarm2_status = client.describe_alarms(AlarmNames=[alarm2])
        assert alarm1_status["MetricAlarms"][0]["ActionsEnabled"] == True
        assert alarm2_status["MetricAlarms"][0]["ActionsEnabled"] == result_count
    finally:
        client.delete_alarms(AlarmNames=[alarm1, alarm2])


@pytest.mark.parametrize(
    "aws_region, cloudwatch_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "cloudwatch-scheduler-test-9", "Values": ["true"]}],
            [{"Key": "cloudwatch-scheduler-test-9", "Values": ["true"]}],
            True,
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "cloudwatch-scheduler-test-10", "Values": ["true"]}],
            False,
        ),
        (
            "eu-west-2",
            [{"Key": "cloudwatch-scheduler-test-11", "Values": ["true"]}],
            [{"Key": "cloudwatch-scheduler-test-11", "Values": ["true"]}],
            True,
        ),
        (
            "eu-west-2",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "cloudwatch-scheduler-test-12", "Values": ["true"]}],
            False,
        ),
    ],
)
def test_start_cloudwatch_alarms(
    aws_region, cloudwatch_tag, scheduler_tag, result_count
):
    """Verify cloudwatch start scheduler class method."""
    client = boto3.client("cloudwatch", region_name=aws_region)
    fake_tag = {"Key": "faketag", "Value": "true"}
    alarm_tag = {
        "Key": cloudwatch_tag[0]["Key"],
        "Value": "".join(cloudwatch_tag[0]["Values"]),
    }
    try:
        alarm1 = create_cloudwatch_alarm(aws_region, fake_tag)
        alarm2 = create_cloudwatch_alarm(aws_region, alarm_tag)
        client.disable_alarm_actions(AlarmNames=[alarm1, alarm2])
        cloudwatch_scheduler = CloudWatchAlarmScheduler(aws_region)
        cloudwatch_scheduler.start(scheduler_tag)
        alarm1_status = client.describe_alarms(AlarmNames=[alarm1])
        alarm2_status = client.describe_alarms(AlarmNames=[alarm2])
        assert alarm1_status["MetricAlarms"][0]["ActionsEnabled"] == False
        assert alarm2_status["MetricAlarms"][0]["ActionsEnabled"] == result_count
    finally:
        client.delete_alarms(AlarmNames=[alarm1, alarm2])
