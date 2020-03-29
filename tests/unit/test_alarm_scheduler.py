"""Tests for the cloudwatch alarm scheduler class."""

import boto3

from moto import mock_autoscaling, mock_cloudwatch, mock_ec2, mock_rds2

from package.scheduler.cloudwatch_handler import CloudWatchAlarmScheduler

from .utils import launch_asg, put_create_alarm, launch_ec2_instances, launch_rds_instance

import pytest

@pytest.mark.parametrize(
    "aws_region, associate_alarm, result_count", [
        ("eu-west-1", True, 1),
        ("eu-west-1", False, 0),
        ("eu-west-2", True, 1),
        ("eu-west-2", False, 0),
    ]
)
@mock_cloudwatch
@mock_ec2
def test_list_instance_alarm(aws_region, associate_alarm, result_count):
    """Verify list cloudwatch alarm function on instance."""
    instance = launch_ec2_instances(1, aws_region, "tostop", "true")
    instance_id = instance["Instances"][0]["InstanceId"]
    if associate_alarm:
        dimensions = [{"Name": "InstanceId", "Value": instance_id}]
    else:
        dimensions = []
    put_create_alarm(aws_region, "alarm-1", dimensions)
    put_create_alarm(aws_region, "alarm-2", dimensions=[])
    cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
    list_alarms = cloudwatch_alarm.list_alarm(instance_id)
    assert len(list(list_alarms)) == result_count


@pytest.mark.parametrize(
    "aws_region, associate_alarm, result_count", [
        ("eu-west-1", True, 1),
        ("eu-west-1", False, 0),
        ("eu-west-2", True, 1),
        ("eu-west-2", False, 0),
    ]
)
@mock_cloudwatch
@mock_autoscaling
def test_list_asg_alarm(aws_region, associate_alarm, result_count):
    """Verify list cloudwatch alarm function on autoscaling group."""
    asg = launch_asg(aws_region, "tostop", "true")
    asg_name = asg["AutoScalingGroups"][0]["AutoScalingGroupName"]
    if associate_alarm:
        dimensions = [{"Name": "AutoScalingGroupName", "Value": asg_name}]
    else:
        dimensions = []
    put_create_alarm(aws_region, "alarm-1", dimensions)
    put_create_alarm(aws_region, "alarm-2", dimensions=[])
    cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
    list_alarms = cloudwatch_alarm.list_alarm(asg_name)
    assert len(list(list_alarms)) == result_count


@pytest.mark.parametrize(
    "aws_region, associate_alarm, result_count", [
        ("eu-west-1", True, 1),
        ("eu-west-1", False, 0),
        ("eu-west-2", True, 1),
        ("eu-west-2", False, 0),
    ]
)
@mock_cloudwatch
@mock_rds2
def test_list_rds_instance_alarm(aws_region, associate_alarm, result_count):
    """Verify list cloudwatch alarm function on rds instance."""
    rds_instance = launch_rds_instance(aws_region, "tostop", "true")
    rds_instance_id = rds_instance["DBInstance"]["DBInstanceIdentifier"]
    if associate_alarm:
        dimensions = [{"Name": "DBInstanceIdentifier", "Value": rds_instance_id}]
    else:
        dimensions = []
    put_create_alarm(aws_region, "alarm-1", dimensions)
    put_create_alarm(aws_region, "alarm-2", dimensions=[])
    cloudwatch_alarm = CloudWatchAlarmScheduler(aws_region)
    list_alarms = cloudwatch_alarm.list_alarm(rds_instance_id)
    assert len(list(list_alarms)) == result_count
