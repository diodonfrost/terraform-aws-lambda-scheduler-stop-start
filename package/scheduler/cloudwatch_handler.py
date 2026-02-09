"""Cloudwatch alarm action scheduler."""

from typing import Dict, Iterator, List

import boto3
from botocore.exceptions import ClientError

from .decorators import skip_on_dry_run
from .exceptions import cloudwatch_exception
from .filter_resources_by_tags import FilterByTags


class CloudWatchAlarmScheduler:
    """Abstract Cloudwatch alarm scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize Cloudwatch alarm scheduler."""
        if region_name:
            self.cloudwatch = boto3.client("cloudwatch", region_name=region_name)
        else:
            self.cloudwatch = boto3.client("cloudwatch")
        self.tag_api = FilterByTags(region_name=region_name)

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List CloudWatch alarm ARNs matching the given tags."""
        yield from self.tag_api.get_resources("cloudwatch:alarm", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Disable CloudWatch alarms with defined tags."""
        for alarm_arn in self.list_resources(aws_tags):
            self._process_alarm(alarm_arn.split(":")[-1], "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Enable CloudWatch alarms with defined tags."""
        for alarm_arn in self.list_resources(aws_tags):
            self._process_alarm(alarm_arn.split(":")[-1], "start")

    @skip_on_dry_run
    def _process_alarm(self, alarm_name: str, action: str) -> None:
        """Process a CloudWatch alarm with the specified action."""
        try:
            if action == "start":
                self.cloudwatch.enable_alarm_actions(AlarmNames=[alarm_name])
                print(f"Enable Cloudwatch alarm {alarm_name}")
            else:
                self.cloudwatch.disable_alarm_actions(AlarmNames=[alarm_name])
                print(f"Disable Cloudwatch alarm {alarm_name}")
        except ClientError as exc:
            cloudwatch_exception("cloudwatch alarm", alarm_name, exc)
