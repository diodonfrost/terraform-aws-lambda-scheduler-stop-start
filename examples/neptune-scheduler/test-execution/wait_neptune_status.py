#!/usr/bin/env python3
"""Script to wait for AWS neptune cluster status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_neptune_cluster_status(
    desired_status: str, cluster_identifiers: List[str]
) -> None:
    """Wait for neptune clusters to reach desired status.

    Args:
        cluster_identifiers: List of neptune cluster identifiers
        desired_status: Desired status to wait for (e.g. 'available', 'paused')
    """
    if not cluster_identifiers:
        return

    neptune = boto3.client("neptune")
    start_time = time.time()
    timeout = 1800  # 30 minutes timeout

    while True:
        try:
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds."
                    "Some neptune clusters may not have reached the desired status."
                )
                sys.exit(1)

            all_clusters_in_desired_state = True
            for cluster_id in cluster_identifiers:
                response = neptune.describe_db_clusters(DBClusterIdentifier=cluster_id)
                cluster_status = response["DBClusters"][0]["Status"]
                instance_id = response["DBClusters"][0]["DBClusterMembers"][0][
                    "DBInstanceIdentifier"
                ]
                instance_response = neptune.describe_db_instances(
                    DBInstanceIdentifier=instance_id
                )
                instance_status = instance_response["DBInstances"][0][
                    "DBInstanceStatus"
                ]

                if (
                    cluster_status != desired_status
                    or instance_status != desired_status
                ):
                    all_clusters_in_desired_state = False
                    break

            if all_clusters_in_desired_state:
                print(f"All neptune clusters are now {desired_status}")
                return

            print(f"Waiting for neptune clusters to be {desired_status}...")
            time.sleep(10)  # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error checking neptune status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_neptune_status.py"
            "<desired_status> <cluster_id1> [cluster_id2 ...]"
        )
        sys.exit(1)

    target_status = sys.argv[1]
    target_clusters = sys.argv[2:]

    wait_for_neptune_cluster_status(target_status, target_clusters)
