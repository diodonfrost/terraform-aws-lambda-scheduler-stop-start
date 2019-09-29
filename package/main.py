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
    # Retrieve variables from aws lambda ENVIRONMENT
    schedule_action = os.getenv("SCHEDULE_ACTION", "stop")
    tag_key = os.getenv("TAG_KEY", "tostop")
    tag_value = os.getenv("TAG_VALUE", "true")
    autoscaling_schedule = os.getenv("AUTOSCALING_SCHEDULE", "true")
    spot_schedule = os.getenv("SPOT_SCHEDULE", "false")
    ec2_schedule = os.getenv("EC2_SCHEDULE", "true")
    rds_schedule = os.getenv("RDS_SCHEDULE", "true")

    asg_scheduler = AutoscalingScheduler()
    spot_scheduler = SpotScheduler()
    ec2_scheduler = Ec2Scheduler()
    rds_scheduler = RdsScheduler()

    if autoscaling_schedule == "true" and schedule_action == "stop":
        asg_scheduler.stop(tag_key, tag_value)
    elif autoscaling_schedule == "true" and schedule_action == "start":
        asg_scheduler.start(tag_key, tag_value)

    if spot_schedule == "terminate" and schedule_action == "stop":
        spot_scheduler.terminate(tag_key, tag_value)

    if ec2_schedule == "true" and schedule_action == "stop":
        ec2_scheduler.stop(tag_key, tag_value)
    elif ec2_schedule == "true" and schedule_action == "start":
        ec2_scheduler.start(tag_key, tag_value)

    if rds_schedule == "true" and schedule_action == "stop":
        rds_scheduler.stop(tag_key, tag_value)
    elif rds_schedule == "true" and schedule_action == "start":
        rds_scheduler.start(tag_key, tag_value)
