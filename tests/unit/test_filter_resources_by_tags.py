# -*- coding: utf-8 -*-

"""Tests for the class FilterByTags class."""

import boto3

from moto import (
    mock_ec2,
    mock_resourcegroupstaggingapi,
)

from package.scheduler.filter_resources_by_tags import FilterByTags
from package.scheduler.instance_handler import InstanceScheduler

from .utils import launch_ec2_instances

import pytest


@pytest.mark.parametrize(
    "aws_region, instance_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            2,
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            [{"Key": "tostop-ec2-test-1", "Values": ["true"]}],
            0,
        ),
    ],
)
@mock_ec2
@mock_resourcegroupstaggingapi
def test_filter_instances(aws_region, instance_tag, scheduler_tag, result_count):
    """Filter instances class method."""
    tag_key = instance_tag[0]["Key"]
    tag_value = "".join(instance_tag[0]["Values"])
    instances_correct_tags = launch_ec2_instances(2, aws_region, tag_key, tag_value)
    instances_bad_tags = launch_ec2_instances(3, aws_region, "wrongkey", "wrongvalue")

    tag_api = FilterByTags(region_name=aws_region)
    instance_arns = tag_api.get_resources("ec2:instance", scheduler_tag)

    assert len(list(instance_arns)) == result_count
