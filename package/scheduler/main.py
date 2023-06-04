# -*- coding: utf-8 -*-

"""This script stop and start aws resources."""
import os
from distutils.util import strtobool

from scheduler.autoscaling_handler import AutoscalingScheduler
from scheduler.cloudwatch_handler import CloudWatchAlarmScheduler
from scheduler.ecs_handler import EcsScheduler
from scheduler.instance_handler import InstanceScheduler
from scheduler.rds_handler import RdsScheduler


def lambda_handler(event, context):
    """Main function entrypoint for lambda.

    Stop and start AWS resources:
    - rds instances
    - rds aurora clusters
    - instance ec2
    - ecs services

    Suspend and resume AWS resources:
    - ec2 autoscaling groups

    Terminate spot instances (spot instance cannot be stopped by a user)
    """
    # Retrieve variables from aws lambda ENVIRONMENT
    schedule_action = os.getenv("SCHEDULE_ACTION")
    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")
    format_tags = [{"Key": os.getenv("TAG_KEY"), "Values": [os.getenv("TAG_VALUE")]}]

    _strategy = {}
    _strategy[AutoscalingScheduler] = os.getenv("AUTOSCALING_SCHEDULE")
    _strategy[InstanceScheduler] = os.getenv("EC2_SCHEDULE")
    _strategy[EcsScheduler] = os.getenv("ECS_SCHEDULE")
    _strategy[RdsScheduler] = os.getenv("RDS_SCHEDULE")
    _strategy[CloudWatchAlarmScheduler] = os.getenv("CLOUDWATCH_ALARM_SCHEDULE")

    for service, to_schedule in _strategy.items():
        if strtobool(to_schedule):
            for aws_region in aws_regions:
                strategy = service(aws_region)
                getattr(strategy, schedule_action)(aws_tags=format_tags)
