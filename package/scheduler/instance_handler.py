"""EC2 instances scheduler.

This module provides functionality to start and stop EC2 instances based on tags.
"""

import logging
from typing import Dict, Iterator, List, Optional

import boto3
from botocore.exceptions import ClientError

from .exceptions import ec2_exception
from .filter_resources_by_tags import FilterByTags

# Set up logger
logger = logging.getLogger(__name__)


class InstanceScheduler:
    """EC2 instance scheduler to start and stop instances based on tags."""

    def __init__(self, region_name: Optional[str] = None) -> None:
        """Initialize EC2 scheduler with AWS clients.

        Args:
            region_name: AWS region name. If None, default region is used.
        """
        self.region_name = region_name
        self.ec2 = (
            boto3.client("ec2", region_name=region_name)
            if region_name
            else boto3.client("ec2")
        )
        self.asg = (
            boto3.client("autoscaling", region_name=region_name)
            if region_name
            else boto3.client("autoscaling")
        )
        self.tag_api = FilterByTags(region_name=region_name)

    def list_resources(self, aws_tags: List[Dict]) -> Iterator[str]:
        """List EC2 instance ARNs matching the given tags."""
        yield from self.tag_api.get_resources("ec2:instance", aws_tags)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Stop EC2 instances with defined tags."""
        for instance_arn in self.list_resources(aws_tags):
            self._process_instance(instance_arn.split("/")[-1], "stop")

    def start(self, aws_tags: List[Dict]) -> None:
        """Start EC2 instances with defined tags."""
        for instance_arn in self.list_resources(aws_tags):
            self._process_instance(instance_arn.split("/")[-1], "start")

    def _process_instance(self, instance_id: str, action: str) -> None:
        """Process an EC2 instance with the specified action."""
        try:
            if self.asg.describe_auto_scaling_instances(InstanceIds=[instance_id])[
                "AutoScalingInstances"
            ]:
                logger.info(
                    f"Skipping {instance_id} as it belongs to an Auto Scaling Group"
                )
                return

            if action == "start":
                self.ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f"Started instance {instance_id}")
            elif action == "stop":
                self.ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f"Stopped instance {instance_id}")

        except ClientError as exc:
            ec2_exception("instance", instance_id, exc)
            logger.error(f"Failed to {action} instance {instance_id}: {str(exc)}")
