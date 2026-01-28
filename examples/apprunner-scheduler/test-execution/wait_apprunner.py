#!/usr/bin/env python3
"""Script to wait for AWS App Runner services status."""

import sys
import time
from typing import List

import boto3
from botocore.exceptions import ClientError


def wait_for_services_status(
    service_arns: List[str], desired_status: str, region: str = None
) -> None:
    """Wait for App Runner services to reach desired status.

    Args:
        service_arns: List of App Runner service ARNs to check
        desired_status: Desired status to wait for (e.g. 'RUNNING', 'PAUSED')
        region: AWS region name
    """
    if not service_arns:
        return

    apprunner = (
        boto3.client("apprunner", region_name=region)
        if region
        else boto3.client("apprunner")
    )
    start_time = time.time()
    timeout = 600  # 10 minutes timeout

    while True:
        try:
            # Check if timeout has been reached
            if time.time() - start_time > timeout:
                print(
                    f"Timeout reached after {timeout} seconds. "
                    "Some services may not have reached the desired status."
                )
                sys.exit(1)

            all_services_in_desired_state = True

            for service_arn in service_arns:
                response = apprunner.describe_service(ServiceArn=service_arn)
                current_status = response["Service"]["Status"]

                if current_status != desired_status:
                    all_services_in_desired_state = False
                    print(
                        f"Service {service_arn} is {current_status}, "
                        f"waiting for {desired_status}..."
                    )
                    break

            if all_services_in_desired_state:
                print(f"All services are now {desired_status}")
                return

            time.sleep(10)  # Wait 10 seconds before checking again

        except ClientError as e:
            print(f"Error checking service status: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python wait_apprunner.py <desired_status> "
            "<service_arn1> [service_arn2 ...]"
        )
        sys.exit(1)

    desired_status = sys.argv[1]
    service_arns = sys.argv[2:]

    wait_for_services_status(service_arns, desired_status)
