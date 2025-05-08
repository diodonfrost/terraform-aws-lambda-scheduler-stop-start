#!/usr/bin/env python3
"""Script to wait for AWS RDS instance status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_rds_instance_status(
    instance_identifiers: List[str], desired_status: str
) -> None:
    """Wait for RDS instances to reach desired status.

    Args:
        instance_identifiers: List of RDS instance identifiers
        desired_status: Desired status to wait for (e.g. 'available', 'stopped')
        region: AWS region name
    """
    if not instance_identifiers:
        return

    rds = boto3.client("rds")
    start_time = time.time()
    timeout = 900  # 15 minutes timeout

    while True:
        try:
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds. Some RDS instances may not have reached the desired status."
                )
                sys.exit(1)

            all_instances_in_desired_state = True
            for instance_id in instance_identifiers:
                response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
                current_status = response["DBInstances"][0]["DBInstanceStatus"]

                if current_status != desired_status:
                    all_instances_in_desired_state = False
                    break

            if all_instances_in_desired_state:
                print(f"All RDS instances are now {desired_status}")
                return

            print(f"Waiting for RDS instances to be {desired_status}...")
            time.sleep(10)  # Wait 30 seconds before checking again

        except ClientError as e:
            print(f"Error checking RDS status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_rds_instance.py <desired_status> <instance_id1> [instance_id2 ...]"
        )
        sys.exit(1)

    desired_status = sys.argv[1]
    instance_identifiers = sys.argv[2:]

    wait_for_rds_instance_status(instance_identifiers, desired_status)
