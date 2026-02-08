"""ecs service scheduler."""

from typing import Dict, Iterator, List

import boto3
from botocore.exceptions import ClientError

from .exceptions import ecs_exception
from .filter_resources_by_tags import FilterByTags


class EcsScheduler:
    """Abstract ECS Service scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ECS service scheduler."""
        if region_name:
            self.ecs = boto3.client("ecs", region_name=region_name)
        else:
            self.ecs = boto3.client("ecs")
        self.tag_api = FilterByTags(region_name=region_name)

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List ECS service ARNs matching the given tags."""
        yield from self.tag_api.get_resources("ecs:service", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop ECS services with defined tags."""
        for service_arn in self.list_resources(aws_tags):
            self._process_service(service_arn, "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start ECS services with defined tags."""
        for service_arn in self.list_resources(aws_tags):
            self._process_service(service_arn, "start")

    def _process_service(self, service_arn: str, action: str) -> None:
        """Process an ECS service with the specified action."""
        cluster_name = service_arn.split("/")[-2]
        service_name = service_arn.split("/")[-1]
        try:
            self.ecs.update_service(
                cluster=cluster_name,
                service=service_name,
                desiredCount=0 if action == "stop" else 1,
            )
            print(
                f"{action.capitalize()} ECS Service {service_name} on Cluster {cluster_name}"
            )
        except ClientError as exc:
            ecs_exception("ECS Service", service_name, exc)
