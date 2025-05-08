#!/usr/bin/env python3
"""Script to wait for AWS RDS cluster status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_rds_cluster_status(
    cluster_identifiers: List[str], desired_status: str
) -> None:
    """Wait for RDS clusters to reach desired status.

    Args:
        cluster_identifiers: List of RDS cluster identifiers
        desired_status: Desired status to wait for (e.g. 'available', 'stopped')
    """
    if not cluster_identifiers:
        return

    rds = boto3.client("rds")
    start_time = time.time()
    timeout = 900  # 15 minutes timeout

    while True:
        try:
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds. Some RDS clusters may not have reached the desired status."
                )
                sys.exit(1)

            all_clusters_in_desired_state = True
            for cluster_id in cluster_identifiers:
                response = rds.describe_db_clusters(DBClusterIdentifier=cluster_id)
                current_status = response["DBClusters"][0]["Status"]

                if current_status != desired_status:
                    all_clusters_in_desired_state = False
                    break

            if all_clusters_in_desired_state:
                print(f"All RDS clusters are now {desired_status}")
                return

            print(f"Waiting for RDS clusters to be {desired_status}...")
            time.sleep(10)  # Wait 30 seconds before checking again

        except ClientError as e:
            print(f"Error checking RDS cluster status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_rds_cluster.py <desired_status> <cluster_id1> [cluster_id2 ...]"
        )
        sys.exit(1)

    desired_status = sys.argv[1]
    cluster_identifiers = sys.argv[2:]

    wait_for_rds_cluster_status(cluster_identifiers, desired_status)
