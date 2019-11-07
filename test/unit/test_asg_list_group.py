"""Tests for the autoscaling group list function."""

from moto import mock_autoscaling

from package.autoscaling_handler import AutoscalingScheduler

from .utils import launch_asg


@mock_autoscaling
def test_asg_scheduler_with_tag():
    """Verify list autoscaling group with defined aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_groups(tag_key, tag_value)
    assert len(list(taglist)) == 1


@mock_autoscaling
def test_asg_scheduler_without_tag():
    """Verify list autoscaling group when the the bad aws tag is set."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_groups("wrongtagkey", "wrongtagvalue")
    assert len(list(taglist)) == 0


@mock_autoscaling
def test_asg_instance_list():
    """Verify list instance in aws with one autoscaling group id."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_instances(["asg-test"])
    assert len(list(taglist)) == 3


@mock_autoscaling
def test_empty_asg_instance_list():
    """Verify list instance in asg with empty autoscaling group."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_asg(aws_region, tag_key, tag_value)
    asg_scheduler = AutoscalingScheduler(aws_region)
    taglist = asg_scheduler.list_instances([])
    assert len(list(taglist)) == 0
