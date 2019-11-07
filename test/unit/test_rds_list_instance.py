"""Tests for the rds list function."""

from moto import mock_rds2

from package.rds_handler import RdsScheduler

from .utils import launch_rds_instance


@mock_rds2
def test_rds_scheduler_instance_with_tag():
    """Verify list rds instance with defined aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_rds_instance(aws_region, tag_key, tag_value)
    rds_scheduler = RdsScheduler(aws_region)
    taglist = rds_scheduler.list_instances(tag_key, tag_value)
    assert len(list(taglist)) == 1


@mock_rds2
def test_rds_scheduler_instance_without_tag():
    """Verify list rds instance wih the bad aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_rds_instance(aws_region, tag_key, tag_value)
    rds_scheduler = RdsScheduler(aws_region)
    taglist = rds_scheduler.list_instances("wrongtagkey", "wrongtagvalue")
    assert len(list(taglist)) == 0
