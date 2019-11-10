"""Tests for the spot list function."""

from moto import mock_ec2

from package.spot_handler import SpotScheduler

from .utils import launch_ec2_spot


@mock_ec2
def test_ec2_scheduler_spot_with_tag():
    """Verify list ec2 instance with defined aws tag."""
    aws_region = "eu-west-1"
    tag_key = "tostop"
    tag_value = "true"

    launch_ec2_spot(3, aws_region)
    spot_list = SpotScheduler(aws_region)
    taglist = spot_list.list_spot(tag_key, tag_value)
    assert len(list(taglist)) == 0
