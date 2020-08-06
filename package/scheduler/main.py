# -*- coding: utf-8 -*-

"""This script stop and start aws resources."""
import os

from scheduler.autoscaling_handler import AutoscalingScheduler
from scheduler.cloudwatch_handler import CloudWatchAlarmScheduler
from scheduler.instance_handler import InstanceScheduler
from scheduler.rds_handler import RdsScheduler
from scheduler.spot_handler import SpotScheduler


def lambda_handler(event, context):
    """Main function entrypoint for lambda.

    Stop and start AWS resources:
    - rds instances
    - rds aurora clusters
    - instance ec2

    Suspend and resume AWS resources:
    - ec2 autoscaling groups

    Terminate spot instances (spot instance cannot be stopped by a user)
    """
    _strategy = {}
    # Retrieve variables from aws lambda ENVIRONMENT
    schedule_action = os.getenv("SCHEDULE_ACTION")
    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")
    tag_key = os.getenv("TAG_KEY")
    tag_value = os.getenv("TAG_VALUE")
    _strategy[AutoscalingScheduler] = os.getenv("AUTOSCALING_SCHEDULE")
    _strategy[SpotScheduler] = os.getenv("SPOT_SCHEDULE")
    _strategy[InstanceScheduler] = os.getenv("EC2_SCHEDULE")
    _strategy[RdsScheduler] = os.getenv("RDS_SCHEDULE")
    _strategy[CloudWatchAlarmScheduler] = os.getenv(
        "CLOUDWATCH_ALARM_SCHEDULE"
    )
    for service, to_schedule in _strategy.items():
        if to_schedule in ("true", "terminate"):
            for aws_region in aws_regions:
                strategy = service(aws_region)
                if to_schedule == "terminate":
                    action = to_schedule
                else:
                    action = schedule_action
                getattr(strategy, action)(tag_key, tag_value)
