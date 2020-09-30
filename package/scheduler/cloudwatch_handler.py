# -*- coding: utf-8 -*-

"""Cloudwatch alarm action scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import cloudwatch_exception
from scheduler.filter_resources_by_tags import FilterByTags


class CloudWatchAlarmScheduler(object):
    """Abstract Cloudwatch alarm scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize Cloudwatch alarm scheduler."""
        if region_name:
            self.cloudwatch = boto3.client("cloudwatch", region_name=region_name)
        else:
            self.cloudwatch = boto3.client("cloudwatch")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws Cloudwatch alarm disable function.

        Disable Cloudwatch alarm with defined tags.

        :param list[map] aws_tags:
            Aws tags to use for filter resources.
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        for alarm_arn in self.tag_api.get_resources("cloudwatch:alarm", aws_tags):
            alarm_name = alarm_arn.split(":")[-1]
            try:
                self.cloudwatch.disable_alarm_actions(AlarmNames=[alarm_name])
                print("Disable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws Cloudwatch alarm enable function.

        Enable Cloudwatch alarm with defined tags.

        :param list[map] aws_tags:
            Aws tags to use for filter resources.
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        for alarm_arn in self.tag_api.get_resources("cloudwatch:alarm", aws_tags):
            alarm_name = alarm_arn.split(":")[-1]
            try:
                self.cloudwatch.enable_alarm_actions(AlarmNames=[alarm_name])
                print("Enable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)
