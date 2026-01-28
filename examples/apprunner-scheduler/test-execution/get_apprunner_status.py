#!/usr/bin/env python3
"""Script to get AWS App Runner service status for Terraform external data source."""

import json
import sys

import boto3


def get_service_status(service_arn: str) -> str:
    """Get the status of an App Runner service.

    Args:
        service_arn: The ARN of the App Runner service

    Returns:
        The status of the service
    """
    apprunner = boto3.client("apprunner")
    response = apprunner.describe_service(ServiceArn=service_arn)
    return response["Service"]["Status"]


if __name__ == "__main__":
    # Read input from stdin (Terraform external data source format)
    input_data = json.load(sys.stdin)
    service_arn = input_data["service_arn"]

    status = get_service_status(service_arn)

    # Output JSON to stdout (Terraform external data source format)
    output = {"status": status}
    print(json.dumps(output))
