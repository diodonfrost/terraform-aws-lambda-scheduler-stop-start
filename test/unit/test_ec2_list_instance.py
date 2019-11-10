"""Tests for the ec2 list function."""

from moto import mock_ec2

from package.ec2_handler import Ec2Scheduler

from .utils import launch_ec2_instances


@mock_ec2
def test_ec2_scheduler_instance_with_tag():
    """Verify list ec2 instances with defined aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_ec2_instances(3, aws_region, tag_key, tag_value)
    ec2_scheduler = Ec2Scheduler(aws_region)
    taglist = ec2_scheduler.list_instances(tag_key, tag_value)
    assert len(list(taglist)) == 3


@mock_ec2
def test_ec2_scheduler_instance_without_tag():
    """Verify list ec2 instances wih the bad aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_ec2_instances(3, aws_region, tag_key, tag_value)
    ec2_scheduler = Ec2Scheduler(aws_region)
    taglist = ec2_scheduler.list_instances("wrongtagkey", "wrongtagvalue")
    assert len(list(taglist)) == 0
