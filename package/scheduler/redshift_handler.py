"""redshift cluster scheduler."""

from typing import Dict, Iterator, List

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

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List Redshift cluster ARNs matching the given tags."""
        yield from self.tag_api.get_resources("redshift:cluster", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop Redshift clusters with defined tags."""
        for cluster_arn in self.list_resources(aws_tags):
            self._process_cluster(cluster_arn.split(":")[-1], "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start Redshift clusters with defined tags."""
        for cluster_arn in self.list_resources(aws_tags):
            self._process_cluster(cluster_arn.split(":")[-1], "start")

    def _process_cluster(self, cluster_id: str, action: str) -> None:
        """Process a Redshift cluster with the specified action."""
        try:
            if action == "start":
                self.redshift.resume_cluster(ClusterIdentifier=cluster_id)
            else:
                self.redshift.pause_cluster(ClusterIdentifier=cluster_id)
            print(f"{action.capitalize()} redshift cluster {cluster_id}")
        except ClientError as exc:
            redshift_exception("redshift cluster", cluster_id, exc)
