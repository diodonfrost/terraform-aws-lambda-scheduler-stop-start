#!/usr/bin/env python3
"""Script to wait for AWS Transfer server status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_transfer_server_status(desired_status: str, server_ids: List[str]) -> None:
    """Wait for AWS Transfer servers to reach desired status.

    Args:
        server_ids: List of AWS Transfer server IDs
        desired_status: Desired status to wait for (e.g. 'ONLINE', 'OFFLINE', 'STARTING', 'STOPPING')
    """
    if not server_ids:
        return

    transfer = boto3.client("transfer")
    start_time = time.time()
    timeout = 900  # 15 minutes timeout

    while True:
        try:
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds. "
                    "Some Transfer servers may not have reached the desired status."
                )
                sys.exit(1)

            all_servers_in_desired_state = True
            for server_id in server_ids:
                response = transfer.describe_server(ServerId=server_id)
                current_status = response["Server"]["State"]

                if current_status != desired_status:
                    all_servers_in_desired_state = False
                    break

            if all_servers_in_desired_state:
                print(f"All Transfer servers are now {desired_status}")
                return

            print(f"Waiting for Transfer servers to be {desired_status}...")
            time.sleep(10)  # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error checking Transfer server status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_transfer_status.py "
            "<desired_status> <server_id1> [server_id2 ...]"
        )
        sys.exit(1)

    target_status = sys.argv[1]
    target_servers = sys.argv[2:]

    wait_for_transfer_server_status(target_status, target_servers)
