"""AWS App Runner service scheduler."""

from typing import Dict, Iterator, List

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

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List AWS App Runner service ARNs matching the given tags."""
        yield from self.tag_api.get_resources("apprunner:service", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Pause AWS App Runner services with defined tags."""
        for service_arn in self.list_resources(aws_tags):
            self._process_apprunner_service(service_arn, "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Resume AWS App Runner services with defined tags."""
        for service_arn in self.list_resources(aws_tags):
            self._process_apprunner_service(service_arn, "start")

    def _process_apprunner_service(self, service_arn: str, action: str) -> None:
        """Process an App Runner service with the specified action."""
        service_name = service_arn.split("/")[-2]
        try:
            if action == "start":
                self.apprunner.resume_service(ServiceArn=service_arn)
                print(f"Resume App Runner Service {service_name}")
            else:
                self.apprunner.pause_service(ServiceArn=service_arn)
                print(f"Pause App Runner Service {service_name}")
        except ClientError as exc:
            apprunner_exception("App Runner Service", service_name, exc)
