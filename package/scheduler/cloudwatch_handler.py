# -*- coding: utf-8 -*-

"""Cloudwatch alarm action scheduler."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from .exceptions import cloudwatch_exception


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

    def stop(self, tag_key: str, tag_value: str) -> None:
        """Aws Cloudwatch alarm disable function.

        Disable Cloudwatch alarm with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for alarm_name in self.filter_alarms(tag_key, tag_value):
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
        for alarm_name in self.filter_alarms(tag_key, tag_value):
            try:
                self.cloudwatch.enable_alarm_actions(AlarmNames=[alarm_name])
                print("Enable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)

    def filter_alarms(self, tag_key: str, tag_value: str) -> Iterator[str]:
        """Aws Cloudwatch alarm filter function.

        List name of all Cloudwatch alarm with the defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :yield Iterator[str]:
            The Name of Cloudwatch alarm.
        """
        paginator = self.cloudwatch.get_paginator("describe_alarms")
        alarm_arn_and_name_list = []
        cloudwatch_tag_to_filter = {"Key": tag_key, "Value": tag_value}

        for page in paginator.paginate():
            for metric_alarm in page["MetricAlarms"]:
                alarm_arn_and_name_list.append(
                    {
                        "arn": metric_alarm["AlarmArn"],
                        "name": metric_alarm["AlarmName"],
                    }
                )

        for alarm_arn_and_name in alarm_arn_and_name_list:
            for alarm_tag in self.cloudwatch.list_tags_for_resource(
                ResourceARN=alarm_arn_and_name["arn"]
            )["Tags"]:
                if cloudwatch_tag_to_filter == alarm_tag:
                    yield alarm_arn_and_name["name"]
