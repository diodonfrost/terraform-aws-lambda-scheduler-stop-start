"""redshift cluster scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from .exceptions import redshift_exception
from .filter_resources_by_tags import FilterByTags


class RedshiftScheduler:
    """Abstract redshift scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize redshift scheduler."""
        if region_name:
            self.redshift = boto3.client("redshift", region_name=region_name)
        else:
            self.redshift = boto3.client("redshift")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws redshift cluster stop function.

        Stop redshift clusters with defined tags.

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
        for cluster_arn in self.tag_api.get_resources("redshift:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                self.redshift.pause_cluster(ClusterIdentifier=cluster_id)
                print(f"Stop redshift cluster {cluster_id}")
            except ClientError as exc:
                redshift_exception("redshift cluster", cluster_id, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws redshift cluster start function.

        Start redshift clusters with defined tags.

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
        for cluster_arn in self.tag_api.get_resources("redshift:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                self.redshift.resume_cluster(ClusterIdentifier=cluster_id)
                print(f"Start redshift cluster {cluster_id}")
            except ClientError as exc:
                redshift_exception("redshift cluster", cluster_id, exc)
