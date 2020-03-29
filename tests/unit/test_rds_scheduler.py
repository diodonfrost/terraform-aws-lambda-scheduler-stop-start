"""Tests for the rds scheduler class."""

from moto import mock_rds2

from package.scheduler.rds_handler import RdsScheduler

from .utils import launch_rds_instance

import pytest


@pytest.mark.parametrize(
    "aws_region, tag_key, tag_value, result_count", [
        ("eu-west-1", "tostop", "true", 1),
        ("eu-west-2", "tostop", "true", 1),
        ("eu-west-2", "badtagkey", "badtagvalue", 0),
    ]
)
@mock_rds2
def test_list_rds(aws_region, tag_key, tag_value, result_count):
    """Verify list rds instance function."""
    launch_rds_instance(aws_region, "tostop", "true")
    rds_scheduler = RdsScheduler(aws_region)
    taglist = rds_scheduler.list_instances(tag_key, tag_value)
    assert len(list(taglist)) == result_count
