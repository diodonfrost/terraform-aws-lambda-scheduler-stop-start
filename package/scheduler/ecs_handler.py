# -*- coding: utf-8 -*-

"""ecs service scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import ecs_exception
from scheduler.filter_resources_by_tags import FilterByTags


class EcsScheduler(object):
    """Abstract ECS Service scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ECS service scheduler."""
        if region_name:
            self.ecs = boto3.client("ecs", region_name=region_name)
        else:
            self.ecs = boto3.client("ecs")
        self.tag_api = FilterByTags(region_name=region_name)

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
                print(
                    "Stop ECS Service {0} on Cluster {1}".format(
                        service_name, cluster_name
                    )
                )
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
                    cluster=cluster_name, service=service_name, desiredCount=1
                )
                print(
                    "Start ECS Service {0} on Cluster {1}".format(
                        service_name, cluster_name
                    )
                )
            except ClientError as exc:
                ecs_exception("ECS Service", service_name, exc)
