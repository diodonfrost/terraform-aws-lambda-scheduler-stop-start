"""ecs service scheduler."""

from os import getenv
from typing import Dict, List

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
        self.ecs_task_desired_count = int(getenv("ECS_TASK_DESIRED_COUNT"))

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws ecs instance stop function.

        Stop ecs service with defined tags and disable its Cloudwatch
        alarms.

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
        for service_arn in self.tag_api.get_resources("ecs:service", aws_tags):
            service_name = service_arn.split("/")[-1]
            cluster_name = service_arn.split("/")[-2]
            try:
                self.ecs.update_service(
                    cluster=cluster_name, service=service_name, desiredCount=0
                )
                print(f"Stop ECS Service {service_name} on Cluster {cluster_name}")
            except ClientError as exc:
                ecs_exception("ECS Service", service_name, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws ec2 instance start function.

        Start ec2 instances with defined tags.

        Aws tags to use for filter resources
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
        for service_arn in self.tag_api.get_resources("ecs:service", aws_tags):
            service_name = service_arn.split("/")[-1]
            cluster_name = service_arn.split("/")[-2]
            try:
                self.ecs.update_service(
                    cluster=cluster_name, service=service_name, desiredCount=self.ecs_task_desired_count
                )
                print(f"Start ECS Service {service_name} on Cluster {cluster_name}")
            except ClientError as exc:
                ecs_exception("ECS Service", service_name, exc)
