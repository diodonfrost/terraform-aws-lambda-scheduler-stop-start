"""documentdb instances scheduler."""

from typing import Dict, Iterator, List

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

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List DocumentDB cluster ARNs matching the given tags."""
        yield from self.tag_api.get_resources("rds:cluster", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop DocumentDB clusters with defined tags."""
        for cluster_arn in self.list_resources(aws_tags):
            self._process_cluster(cluster_arn.split(":")[-1], "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start DocumentDB clusters with defined tags."""
        for cluster_arn in self.list_resources(aws_tags):
            self._process_cluster(cluster_arn.split(":")[-1], "start")

    def _process_cluster(self, cluster_id: str, action: str) -> None:
        """Process a DocumentDB cluster with the specified action."""
        try:
            if action == "start":
                self.documentdb.start_db_cluster(DBClusterIdentifier=cluster_id)
            else:
                self.documentdb.stop_db_cluster(DBClusterIdentifier=cluster_id)
            print(f"{action.capitalize()} documentdb cluster {cluster_id}")
        except ClientError as exc:
            documentdb_exception("documentdb cluster", cluster_id, exc)
