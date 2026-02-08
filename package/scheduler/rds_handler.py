"""RDS instances scheduler."""

from typing import Dict, List, Optional

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

    def list_resources(self, aws_tags: List[Dict]) -> dict:
        """List RDS cluster and instance ARNs matching the given tags."""
        return {
            "clusters": list(self.tag_api.get_resources("rds:cluster", aws_tags)),
            "instances": list(self.tag_api.get_resources("rds:db", aws_tags)),
        }

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop RDS Aurora clusters and RDS DB instances with defined tags."""
        resources = self.list_resources(aws_tags)
        cluster_ids = [arn.split(":")[-1] for arn in resources["clusters"]]
        db_ids = [arn.split(":")[-1] for arn in resources["instances"]]
        for cluster_id in cluster_ids:
            self._process_cluster(cluster_id, "stop")
        for db_id in db_ids:
            self._process_instance(db_id, "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start RDS Aurora clusters and RDS DB instances with defined tags."""
        resources = self.list_resources(aws_tags)
        cluster_ids = [arn.split(":")[-1] for arn in resources["clusters"]]
        db_ids = [arn.split(":")[-1] for arn in resources["instances"]]
        for cluster_id in cluster_ids:
            self._process_cluster(cluster_id, "start")
        for db_id in db_ids:
            self._process_instance(db_id, "start")

    def _process_cluster(self, cluster_id: str, action: str) -> None:
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

    def _process_instance(self, db_id: str, action: str) -> None:
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
