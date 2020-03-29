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

    def disable(self, resource_id: str) -> None:
        """Aws Cloudwatch alarm disable function.

        Disable Cloudwatch alarm on defined resource.

        :param str resource_id:
            Specify the exact aws resource ID on which Cloudwatch alarm
            will be disable.
        """
        for alarm_name in self.list_alarm(resource_id):
            try:
                self.cloudwatch.disable_alarm_actions(AlarmNames=[alarm_name])
                print("Disable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)

    def enable(self, resource_id: str) -> None:
        """Aws Cloudwatch alarm enable function.

        Enable Cloudwatch alarm on defined resource.

        :param str resource_id:
            Specify the exact aws resource ID on which Cloudwatch alarm
            will be enable.
        """
        for alarm_name in self.list_alarm(resource_id):
            try:
                self.cloudwatch.enable_alarm_actions(AlarmNames=[alarm_name])
                print("Enable Cloudwatch alarm {0}".format(alarm_name))
            except ClientError as exc:
                cloudwatch_exception("cloudwatch alarm", alarm_name, exc)

    def list_alarm(self, resource_id: str) -> Iterator[str]:
        """Aws Cloudwatch alarm list function.

        List name of all Cloudwatch alarm attached to the defined
        aws resource.

        :yield Iterator[str]:
            The Name of Cloudwatch alarm.
        """
        paginator = self.cloudwatch.get_paginator("describe_alarms")

        for page in paginator.paginate():
            for metric_alarm in page["MetricAlarms"]:
                for dimension in metric_alarm["Dimensions"]:
                    if resource_id == dimension["Value"]:
                        yield metric_alarm["AlarmName"]
