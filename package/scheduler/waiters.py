# -*- coding: utf-8 -*-

"""Autoscaling instances scheduler."""

from typing import List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import ec2_exception


class AwsWaiters(object):
    """Abstract aws waiter in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize aws waiter."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def instance_running(self, instance_ids: List[str]) -> None:
        """Aws waiter for instance running.

        Wait ec2 instances are in running state.

        :param list instance_ids:
            The instance IDs to wait.
        """
        if instance_ids:
            try:
                instance_waiter = self.ec2.get_waiter("instance_running")
                instance_waiter.wait(
                    InstanceIds=instance_ids,
                    WaiterConfig={"Delay": 15, "MaxAttempts": 15},
                )
            except ClientError as exc:
                ec2_exception("waiter", instance_waiter, exc)
