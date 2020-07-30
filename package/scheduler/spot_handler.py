# -*- coding: utf-8 -*-

"""Spot instances scheduler."""

from typing import Set

import boto3

from botocore.exceptions import ClientError

from .exceptions import ec2_exception


class SpotScheduler(object):
    """Abstract spot scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize autoscaling scheduler."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def terminate(self, tag_key: str, tag_value: str) -> None:
        """Aws spot instance scheduler function.

        Terminate spot instances by using the defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for spot_instance in self.list_spot(tag_key, tag_value):
            try:
                self.ec2.terminate_instances(InstanceIds=[spot_instance])
                print("Terminate spot instance {0}".format(spot_instance))
            except ClientError as exc:
                ec2_exception("spot instance", spot_instance, exc)

    def list_spot(self, tag_key: str, tag_value: str) -> Set[str]:
        """Aws ec2 spot instance list function.

        List name of one-time ec2 spot instances with
        specific tag and return it in list.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :return Set[str]:
            The Id of the one-time spot instances
        """
        spot_ot_list = []
        spot_list = []
        paginator = self.ec2.get_paginator("describe_instances")
        page_iterator = paginator.paginate(
            Filters=[
                {"Name": "tag:" + tag_key, "Values": [tag_value]},
                {"Name": "instance-lifecycle", "Values": ["spot"]},
                {
                    "Name": "instance-state-name",
                    "Values": ["pending", "running", "stopping", "stopped"],
                },
            ]
        )

        for page in page_iterator:
            for reservation in page["Reservations"]:
                for spot in reservation["Instances"]:
                    spot_list.append(spot["InstanceId"])

        # Retrieve all one-time SPOT instance
        paginator_ot = self.ec2.get_paginator(
            "describe_spot_instance_requests"
        )
        page_ot_iterator = paginator_ot.paginate(
            Filters=[{"Name": "type", "Values": ["one-time"]}]
        )

        for page_ot in page_ot_iterator:
            for spot_instance_requests in page_ot["SpotInstanceRequests"]:
                spot_ot_list.append(spot_instance_requests["InstanceId"])

        # Return all one-time SPOT instance which have the correct
        # matching tag + instance-state
        return set(spot_ot_list).intersection(spot_list)
