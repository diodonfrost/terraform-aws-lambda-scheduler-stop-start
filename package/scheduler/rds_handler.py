"""RDS instances scheduler."""

from typing import Dict, List, Literal, Optional

import boto3
from botocore.exceptions import ClientError

from .exceptions import rds_exception
from .filter_resources_by_tags import FilterByTags


class RdsScheduler:
    """RDS resource scheduler for controlling instances and clusters."""

    def __init__(self, region_name: Optional[str] = None) -> None:
        """Initialize RDS scheduler.

        Args:
            region_name: AWS region name. Uses default configuration if not specified.
        """
        self.rds = (
            boto3.client("rds", region_name=region_name)
            if region_name
            else boto3.client("rds")
        )
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop RDS Aurora clusters and RDS DB instances with defined tags.

        Args:
            aws_tags: AWS tags to filter resources.
                Example: [{'Key': 'Environment', 'Values': ['Dev']}]
        """
        self._process_resources(aws_tags, action="stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start RDS Aurora clusters and RDS DB instances with defined tags.

        Args:
            aws_tags: AWS tags to filter resources.
                Example: [{'Key': 'Environment', 'Values': ['Dev']}]
        """
        self._process_resources(aws_tags, action="start")

    def _process_resources(
        self, aws_tags: List[Dict], action: Literal["start", "stop"]
    ) -> None:
        """Process RDS resources with the specified action.

        Args:
            aws_tags: AWS tags to filter resources.
            action: Action to perform ("start" or "stop").
        """
        # Handle clusters
        for cluster_arn in self.tag_api.get_resources("rds:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            self._process_cluster(cluster_id, action)

        # Handle instances
        for db_arn in self.tag_api.get_resources("rds:db", aws_tags):
            db_id = db_arn.split(":")[-1]
            self._process_instance(db_id, action)

    def _process_cluster(
        self, cluster_id: str, action: Literal["start", "stop"]
    ) -> None:
        """Process an RDS cluster with the specified action.

        Args:
            cluster_id: RDS cluster identifier.
            action: Action to perform ("start" or "stop").
        """
        try:
            # Identifier must be cluster id, not resource id
            self.rds.describe_db_clusters(DBClusterIdentifier=cluster_id)

            if action == "start":
                self.rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                print(f"Start RDS cluster {cluster_id}")
            else:
                self.rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                print(f"Stop RDS cluster {cluster_id}")

        except ClientError as exc:
            rds_exception("RDS cluster", cluster_id, exc)

    def _process_instance(self, db_id: str, action: Literal["start", "stop"]) -> None:
        """Process an RDS instance with the specified action.

        Args:
            db_id: RDS instance identifier.
            action: Action to perform ("start" or "stop").
        """
        try:
            if action == "start":
                self.rds.start_db_instance(DBInstanceIdentifier=db_id)
                print(f"Start RDS instance {db_id}")
            else:
                self.rds.stop_db_instance(DBInstanceIdentifier=db_id)
                print(f"Stop RDS instance {db_id}")

        except ClientError as exc:
            rds_exception("RDS instance", db_id, exc)
