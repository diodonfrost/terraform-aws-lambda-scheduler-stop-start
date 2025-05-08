"""Autoscaling instances scheduler."""

import logging
from typing import Dict, Iterator, List, Optional, Union, Set

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

    def stop(self, aws_tags: List[Dict], terminate_instances: bool = False) -> None:
        """Suspend Auto Scaling groups and stop/terminate their instances.

        Args:
            aws_tags: AWS tags to filter resources by. Format:
                [{'Key': 'tag_key', 'Values': ['tag_value']}]
            terminate_instances: If True, terminate instances instead of stopping them
        """
        tag_key, tag_value = self._extract_tag_info(aws_tags)
        asg_name_list = self.list_groups(tag_key, tag_value)
        instance_id_list = list(self.list_instances(asg_name_list))

        # Suspend Auto Scaling groups
        self._suspend_asg_processes(asg_name_list)

        # Stop or terminate instances
        self._manage_instances(instance_id_list, terminate=terminate_instances)

    def start(self, aws_tags: List[Dict]) -> None:
        """Resume Auto Scaling groups and start their instances.

        Args:
            aws_tags: AWS tags to filter resources by. Format:
                [{'Key': 'tag_key', 'Values': ['tag_value']}]
        """
        tag_key, tag_value = self._extract_tag_info(aws_tags)
        asg_name_list = self.list_groups(tag_key, tag_value)
        instance_id_list = list(self.list_instances(asg_name_list))

        # Start instances
        started_instances = self._start_instances(instance_id_list)

        # Wait for instances to be running
        if started_instances:
            self.waiter.instance_running(instance_ids=started_instances)

        # Resume Auto Scaling groups
        self._resume_asg_processes(asg_name_list)

    def _suspend_asg_processes(self, asg_names: List[str]) -> None:
        """Suspend processes for the specified Auto Scaling groups.

        Args:
            asg_names: List of Auto Scaling group names
        """
        for asg_name in asg_names:
            try:
                self.asg.suspend_processes(AutoScalingGroupName=asg_name)
                logger.info(f"Suspended Auto Scaling group: {asg_name}")
            except ClientError as exc:
                ec2_exception("Auto Scaling group", asg_name, exc)

    def _resume_asg_processes(self, asg_names: List[str]) -> None:
        """Resume processes for the specified Auto Scaling groups.

        Args:
            asg_names: List of Auto Scaling group names
        """
        for asg_name in asg_names:
            try:
                self.asg.resume_processes(AutoScalingGroupName=asg_name)
                logger.info(f"Resumed Auto Scaling group: {asg_name}")
            except ClientError as exc:
                ec2_exception("Auto Scaling group", asg_name, exc)

    def _manage_instances(
        self, instance_ids: List[str], terminate: bool = False
    ) -> None:
        """Stop or terminate EC2 instances.

        Args:
            instance_ids: List of EC2 instance IDs
            terminate: If True, terminate instances; otherwise stop them
        """
        if not instance_ids:
            logger.info("No instances to manage")
            return

        for instance_id in instance_ids:
            try:
                if terminate:
                    self.ec2.terminate_instances(InstanceIds=[instance_id])
                    logger.info(f"Terminated instance: {instance_id}")
                else:
                    self.ec2.stop_instances(InstanceIds=[instance_id])
                    logger.info(f"Stopped instance: {instance_id}")
            except ClientError as exc:
                ec2_exception("instance", instance_id, exc)

    def _start_instances(self, instance_ids: List[str]) -> List[str]:
        """Start EC2 instances and return list of successfully started instance IDs.

        Args:
            instance_ids: List of EC2 instance IDs to start

        Returns:
            List of successfully started instance IDs
        """
        started_instances = []

        if not instance_ids:
            logger.info("No instances to start")
            return started_instances

        for instance_id in instance_ids:
            try:
                self.ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f"Started instance: {instance_id}")
                started_instances.append(instance_id)
            except ClientError as exc:
                ec2_exception("instance", instance_id, exc)

        return started_instances

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
