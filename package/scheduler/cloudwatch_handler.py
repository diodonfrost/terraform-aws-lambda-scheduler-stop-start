# -*- coding: utf-8 -*-

"""Cloudwatch alarm action scheduler."""

import boto3

from botocore.exceptions import ClientError

from .exceptions import cloudwatch_exception
from .filter_resources_by_tags import FilterByTags


class CloudWatchAlarmScheduler(object):
    """Abstract Cloudwatch alarm scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize Cloudwatch alarm scheduler."""
        if region_name:
            self.cloudwatch = boto3.client(
                "cloudwatch", region_name=region_name
            )
        else:
            self.cloudwatch = boto3.client("cloudwatch")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, tag_key: str, tag_value: str) -> None:
        """Aws Cloudwatch alarm disable function.

        Disable Cloudwatch alarm with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        format_tag = [{"Key": tag_key, "Values": [tag_value]}]

        for alarm_arn in self.tag_api.get_resources(
            "cloudwatch:alarm", format_tag
        ):
            alarm_name = alarm_arn.split(":")[-1]
            try:
                self.cloudwatch.disable_alarm_actions(AlarmNames=[alarm_name])
                print("Disable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)

    def start(self, tag_key: str, tag_value: str) -> None:
        """Aws Cloudwatch alarm enable function.

        Enable Cloudwatch alarm with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        format_tag = [{"Key": tag_key, "Values": [tag_value]}]

        for alarm_arn in self.tag_api.get_resources(
            "cloudwatch:alarm", format_tag
        ):
            alarm_name = alarm_arn.split(":")[-1]
            try:
                self.cloudwatch.enable_alarm_actions(AlarmNames=[alarm_name])
                print("Enable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)
