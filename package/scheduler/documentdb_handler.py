"""documentdb instances scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from .exceptions import documentdb_exception
from .filter_resources_by_tags import FilterByTags


class DocumentDBScheduler:
    """documentdb scheduler."""

    def __init__(self, region_name=None) -> None:
        """Initialize documentdb scheduler."""
        if region_name:
            self.documentdb = boto3.client("docdb", region_name=region_name)
        else:
            self.documentdb = boto3.client("docdb")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws documentdb cluster stop function.

        Stop documentdb clusters with defined tags.

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
        for cluster_arn in self.tag_api.get_resources("rds:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                self.documentdb.stop_db_cluster(DBClusterIdentifier=cluster_id)
                print(f"Stop documentdb cluster {cluster_id}")
            except ClientError as exc:
                documentdb_exception("documentdb cluster", cluster_id, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws documentdb cluster start function.

        Start documentdb clusters with defined tags.

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
        for cluster_arn in self.tag_api.get_resources("rds:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                self.documentdb.start_db_cluster(DBClusterIdentifier=cluster_id)
                print(f"Start documentdb cluster {cluster_id}")
            except ClientError as exc:
                documentdb_exception("documentdb cluster", cluster_id, exc)
