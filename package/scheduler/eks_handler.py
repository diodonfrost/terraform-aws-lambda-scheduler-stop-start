# -*- coding: utf-8 -*-

"""eks service scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import eks_exception
from scheduler.filter_resources_by_tags import FilterByTags


class eksScheduler(object):
    """Abstract eks Service scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize eks service scheduler."""
        if region_name:
            self.eks = boto3.client("eks", region_name=region_name)
        else:
            self.eks = boto3.client("eks")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        print("Inside the EKS stop")
        """Aws eks instance stop function.

        Stop eks service with defined tags and disable its Cloudwatch
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
        for service_arn in self.tag_api.get_resources("eks:nodegroup", aws_tags):
            print(f"Service ARN is {service_arn}")
            nodegroup_name = service_arn.split("/")[-1]
            cluster_name - service_arn.split("/")[-2]
            print(f"Cluster name is {cluster_name}, nodegroup_name is {nodegroup_name}")
            try:
                # self.eks.update_service(
                #     cluster=cluster_name, service=service_name, desiredCount=0
                # )
                print ("About to try the update")
                self.eks.update_nodegroup_config(
                    clusterName = cluster_name,
                    nodegroupName = nodegroup_name,
                    scalingConfig = {
                        'minSize': min_size,
                        'desiredSize': desired_size,
                        'maxSize': max_size
                    }
                )
                print ("Completed the update")
                print(
                    "Stop eks Service {0} on Cluster {1}".format(
                        service_arn, cluster_name
                    )
                )
            except ClientError as exc:
                eks_exception("eks Service", service_arn, exc)

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
        for service_arn in self.tag_api.get_resources("eks:nodegroup", aws_tags):
            print(f"Service ARN is {service_arn}")
            nodegroup_name = service_arn.split("/")[-1]
            cluster_name - service_arn.split("/")[-2]
            print(f"Cluster name is {cluster_name}, nodegroup_name is {nodegroup_name}")
            try:
                # self.eks.update_service(
                #     cluster=cluster_name, service=service_name, desiredCount=0
                # )
                print ("About to try the update")
                self.eks.update_nodegroup_config(
                    clusterName = cluster_name,
                    nodegroupName = nodegroup_name,
                    scalingConfig = {
                        'minSize': min_size,
                        'desiredSize': desired_size,
                        'maxSize': max_size
                    }
                )
                print ("Completed the update")
                print(
                    "Stop eks Service {0} on Cluster {1}".format(
                        service_arn, cluster_name
                    )
                )
            except ClientError as exc:
                eks_exception("eks Service", service_arn, exc)