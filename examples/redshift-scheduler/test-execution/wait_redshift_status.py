#!/usr/bin/env python3
"""Script to wait for AWS Redshift cluster status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_redshift_cluster_status(
    desired_status: str, cluster_identifiers: List[str]
) -> None:
    """Wait for Redshift clusters to reach desired status.

    Args:
        cluster_identifiers: List of Redshift cluster identifiers
        desired_status: Desired status to wait for (e.g. 'available', 'paused')
    """
    if not cluster_identifiers:
        return

    redshift = boto3.client("redshift")
    start_time = time.time()
    timeout = 900  # 15 minutes timeout

    while True:
        try:
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds."
                    "Some Redshift clusters may not have reached the desired status."
                )
                sys.exit(1)

            all_clusters_in_desired_state = True
            for cluster_id in cluster_identifiers:
                response = redshift.describe_clusters(ClusterIdentifier=cluster_id)
                current_availability_status = response["Clusters"][0][
                    "ClusterAvailabilityStatus"
                ]

                if current_availability_status != desired_status:
                    all_clusters_in_desired_state = False
                    break

            if all_clusters_in_desired_state:
                print(f"All Redshift clusters are now {desired_status}")
                return

            print(f"Waiting for Redshift clusters to be {desired_status}...")
            time.sleep(10)  # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error checking Redshift status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_redshift_status.py"
            "<desired_status> <cluster_id1> [cluster_id2 ...]"
        )
        sys.exit(1)

    target_status = sys.argv[1]
    target_clusters = sys.argv[2:]

    wait_for_redshift_cluster_status(target_status, target_clusters)
