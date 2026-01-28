"""AWS App Runner service scheduler."""

from typing import Dict, List

import boto3
from botocore.exceptions import ClientError

from .exceptions import apprunner_exception
from .filter_resources_by_tags import FilterByTags


class AppRunnerScheduler:
    """Abstract AWS App Runner Service scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize App Runner service scheduler."""
        if region_name:
            self.apprunner = boto3.client("apprunner", region_name=region_name)
        else:
            self.apprunner = boto3.client("apprunner")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Pause AWS App Runner services with defined tags.

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
        for service_arn in self.tag_api.get_resources("apprunner:service", aws_tags):
            service_name = service_arn.split("/")[-2]
            try:
                self.apprunner.pause_service(ServiceArn=service_arn)
                print(f"Pause App Runner Service {service_name}")
            except ClientError as exc:
                apprunner_exception("App Runner Service", service_name, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Resume AWS App Runner services with defined tags.

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
        for service_arn in self.tag_api.get_resources("apprunner:service", aws_tags):
            service_name = service_arn.split("/")[-2]
            try:
                self.apprunner.resume_service(ServiceArn=service_arn)
                print(f"Resume App Runner Service {service_name}")
            except ClientError as exc:
                apprunner_exception("App Runner Service", service_name, exc)
