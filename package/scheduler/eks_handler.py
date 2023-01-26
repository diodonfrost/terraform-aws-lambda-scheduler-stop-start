# -*- coding: utf-8 -*-

"""eks service scheduler."""

import boto3, os

from typing import Dict, List

from botocore.exceptions import ClientError

from scheduler.exceptions import eks_exception
from scheduler.filter_resources_by_tags import FilterByTags

cluster_name=""
min_size=3
max_size=3
desiredSize=3

class EksScheduler(object):
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
            nodegroup_name=service_arn.split("/")[-2]
            cluster_name=service_arn.split("/")[-3]
            print(f"Scaling down {cluster_name}, nodegroup_name {nodegroup_name}")
            minSize, maxSize, desiredSize = map(int, os.getenv("EKS_CONFIG_PAUSED").split(','))
            print(f"minSize={minSize}, maxSize={maxSize}, desiredSize={desiredSize}")
            try:
                # self.eks.update_service(
                #     cluster=cluster_name, service=service_name, desiredCount=0
                # )
                print ("About to try the update")
                self.eks.update_nodegroup_config(
                    clusterName=cluster_name,
                    nodegroupName=nodegroup_name,
                    scalingConfig = {
                        'minSize': minSize,
                        'maxSize': maxSize,
                        'desiredSize': desiredSize,

                    }
                )
                print("Completed the update")
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
            nodegroup_name=service_arn.split("/")[-2]
            cluster_name=service_arn.split("/")[-3]
            minSize, maxSize, desiredSize  = map(int, os.getenv("EKS_CONFIG_RESUME").split(','))
            print(f"Cluster name is {cluster_name}, nodegroup_name is {nodegroup_name}")
            print(f"minSize={minSize}, maxSize={maxSize}, desiredSize={desiredSize}")
            try:
                # self.eks.update_service(
                #     cluster=cluster_name, service=service_name, desiredCount=0
                # )
                print ("About to try the update")
                self.eks.update_nodegroup_config(
                    clusterName = cluster_name,
                    nodegroupName = nodegroup_name,
                    scalingConfig = {
                        'minSize': minSize,
                        'maxSize': maxSize,
                        'desiredSize': desiredSize,

                    }
                )
                print ("Completed the update")
            except ClientError as exc:
                eks_exception("eks Service", service_arn, exc)