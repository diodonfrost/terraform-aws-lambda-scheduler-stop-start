# -*- coding: utf-8 -*-

"""This script stop and start aws resources."""
import os

from autoscaling_handler import AutoscalingScheduler

from ec2_handler import Ec2Scheduler

from rds_handler import RdsScheduler

from spot_handler import SpotScheduler


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
    tag_key = os.getenv("TAG_KEY")
    tag_value = os.getenv("TAG_VALUE")
    _strategy[AutoscalingScheduler] = os.getenv("AUTOSCALING_SCHEDULE")
    _strategy[SpotScheduler] = os.getenv("SPOT_SCHEDULE")
    _strategy[Ec2Scheduler] = os.getenv("EC2_SCHEDULE")
    _strategy[RdsScheduler] = os.getenv("RDS_SCHEDULE")

    for key, value in _strategy.items():
        if value == "true":
            strategy = key()
            if schedule_action == "stop":
                strategy.stop(tag_key, tag_value)
            elif schedule_action == "start":
                strategy.start(tag_key, tag_value)
        elif value == "terminate" and schedule_action == "stop":
            strategy = key()
            strategy.terminate(tag_key, tag_value)
