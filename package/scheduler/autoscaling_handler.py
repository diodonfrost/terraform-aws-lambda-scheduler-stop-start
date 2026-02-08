"""Autoscaling instances scheduler."""

import logging
from typing import Dict, Iterator, List, Optional

import boto3
from botocore.exceptions import ClientError

from .exceptions import ec2_exception
from .waiters import AwsWaiters

logger = logging.getLogger(__name__)


class AutoscalingScheduler:
    """Manages AWS Auto Scaling groups scheduling operations."""

    def __init__(self, region_name: Optional[str] = None) -> None:
        """Initialize AWS clients for EC2 and Auto Scaling.

        Args:
            region_name: AWS region name. If None, default region will be used.
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
        self.waiter = AwsWaiters(region_name=region_name)

    def _extract_tag_info(self, aws_tags: List[Dict]) -> tuple:
        """Extract tag key and value from aws_tags.

        Args:
            aws_tags: List of AWS tag dictionaries

        Returns:
            Tuple containing (tag_key, tag_value)
        """
        tag_key = aws_tags[0]["Key"]
        tag_value = "".join(aws_tags[0]["Values"])
        return tag_key, tag_value

    def list_resources(self, aws_tags: List[Dict]) -> dict:
        """List Auto Scaling group names and instance IDs matching the given tags."""
        tag_key, tag_value = self._extract_tag_info(aws_tags)
        asg_names = self.list_groups(tag_key, tag_value)
        instance_ids = list(self.list_instances(asg_names))
        return {"groups": asg_names, "instances": instance_ids}

    def stop(self, aws_tags: List[Dict], terminate_instances: bool = False) -> None:
        """Suspend Auto Scaling groups and stop/terminate their instances."""
        resources = self.list_resources(aws_tags)

        for asg_name in resources["groups"]:
            self._process_group(asg_name, "suspend")
        for instance_id in resources["instances"]:
            action = "terminate" if terminate_instances else "stop"
            self._process_instance(instance_id, action)

    def start(self, aws_tags: List[Dict]) -> None:
        """Resume Auto Scaling groups and start their instances."""
        resources = self.list_resources(aws_tags)

        started_instances = []
        for instance_id in resources["instances"]:
            if self._process_instance(instance_id, "start"):
                started_instances.append(instance_id)

        if started_instances:
            self.waiter.instance_running(instance_ids=started_instances)

        for asg_name in resources["groups"]:
            self._process_group(asg_name, "resume")

    def _process_group(self, asg_name: str, action: str) -> None:
        """Process an Auto Scaling group with the specified action."""
        try:
            if action == "resume":
                self.asg.resume_processes(AutoScalingGroupName=asg_name)
            else:
                self.asg.suspend_processes(AutoScalingGroupName=asg_name)
            logger.info(f"{action.capitalize()} Auto Scaling group: {asg_name}")
        except ClientError as exc:
            ec2_exception("Auto Scaling group", asg_name, exc)

    def _process_instance(self, instance_id: str, action: str) -> Optional[str]:
        """Process an EC2 instance with the specified action."""
        try:
            if action == "start":
                self.ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f"Started instance: {instance_id}")
                return instance_id
            elif action == "terminate":
                self.ec2.terminate_instances(InstanceIds=[instance_id])
                logger.info(f"Terminated instance: {instance_id}")
            else:
                self.ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f"Stopped instance: {instance_id}")
        except ClientError as exc:
            ec2_exception("instance", instance_id, exc)
        return None

    def list_groups(self, tag_key: str, tag_value: str) -> List[str]:
        """List Auto Scaling groups with the specified tag.

        Args:
            tag_key: AWS tag key to filter by
            tag_value: AWS tag value to filter by

        Returns:
            List of Auto Scaling group names
        """
        asg_name_list = []
        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate():
            for group in page["AutoScalingGroups"]:
                for tag in group["Tags"]:
                    if tag["Key"] == tag_key and tag["Value"] == tag_value:
                        asg_name_list.append(group["AutoScalingGroupName"])

        logger.info(
            f"Found {len(asg_name_list)} Auto Scaling groups with tag {tag_key}={tag_value}"
        )
        return asg_name_list

    def list_instances(self, asg_name_list: List[str]) -> Iterator[str]:
        """List instances in the specified Auto Scaling groups.

        Args:
            asg_name_list: List of Auto Scaling group names

        Returns:
            Iterator yielding instance IDs
        """
        if not asg_name_list:
            logger.info("No Auto Scaling groups to list instances for")
            return iter([])

        paginator = self.asg.get_paginator("describe_auto_scaling_groups")

        for page in paginator.paginate(AutoScalingGroupNames=asg_name_list):
            for scalinggroup in page["AutoScalingGroups"]:
                for instance in scalinggroup["Instances"]:
                    yield instance["InstanceId"]
