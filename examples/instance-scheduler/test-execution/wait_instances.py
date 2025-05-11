#!/usr/bin/env python3
"""Script to wait for AWS instances status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_instances_status(
    instance_ids: List[str], desired_status: str, region: str = None
) -> None:
    """Wait for instances to reach desired status.

    Args:
        instance_ids: List of instance IDs to check
        desired_status: Desired status to wait for (e.g. 'running', 'stopped')
        region: AWS region name
    """
    if not instance_ids:
        return

    ec2 = boto3.client("ec2", region_name=region) if region else boto3.client("ec2")
    start_time = time.time()
    timeout = 600  # 10 minutes timeout

    while True:
        try:
            # Check if timeout has been reached
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds. Some instances may not have reached the desired status."
                )
                sys.exit(1)

            response = ec2.describe_instances(InstanceIds=instance_ids)
            all_instances_in_desired_state = True

            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    current_state = instance["State"]["Name"]
                    if current_state != desired_status:
                        all_instances_in_desired_state = False
                        break

                if not all_instances_in_desired_state:
                    break

            if all_instances_in_desired_state:
                print(f"All instances are now {desired_status}")
                return

            print(f"Waiting for instances to be {desired_status}...")
            time.sleep(10)  # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error checking instance status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_instances.py <desired_status> <instance_id1> [instance_id2 ...]"
        )
        sys.exit(1)

    desired_status = sys.argv[1]
    instance_ids = sys.argv[2:]

    wait_for_instances_status(instance_ids, desired_status)
