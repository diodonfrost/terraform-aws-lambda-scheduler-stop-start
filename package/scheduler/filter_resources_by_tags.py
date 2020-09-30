# -*- coding: utf-8 -*-

"""Filter aws resouces with tags."""

from typing import Iterator

import boto3


class FilterByTags(object):
    """Abstract Filter aws resources by tags in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize resourcegroupstaggingapi client."""
        if region_name:
            self.rgta = boto3.client(
                "resourcegroupstaggingapi", region_name=region_name
            )
        else:
            self.rgta = boto3.client("resourcegroupstaggingapi")

    def get_resources(self, resource_type, aws_tags) -> Iterator[str]:
        """Filter aws resources using resource type and defined tags.

        Returns all the tagged defined resources that are located in
        the specified Region for the AWS account.

        :param str resource_type:
            The constraints on the resources that you want returned.
            The format of each resource type is service[:resourceType] .
            For example, specifying a resource type of ec2 returns all
            Amazon EC2 resources (which includes EC2 instances).
            Specifying a resource type of ec2:instance returns only
            EC2 instances.
        :param list[map] aws_tags:
            A list of TagFilters (keys and values).
            Each TagFilter specified must contain a key with values
            as optional. For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                },
            ]
        :yield Iterator[str]:
            The ids of the resources
        """
        paginator = self.rgta.get_paginator("get_resources")
        page_iterator = paginator.paginate(
            TagFilters=aws_tags, ResourceTypeFilters=[resource_type]
        )
        for page in page_iterator:
            for resource_tag_map in page["ResourceTagMappingList"]:
                yield resource_tag_map["ResourceARN"]
