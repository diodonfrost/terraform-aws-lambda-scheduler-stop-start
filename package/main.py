# -*- coding: utf-8 -*-

"""This script stop and start aws resources."""
import os

from autoscaling_handler import AutoscalingScheduler

import ec2_handler

import rds_handler

import spot_handler


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

    if autoscaling_schedule == "true":
        scheduler = AutoscalingScheduler()
        if schedule_action == "stop":
            scheduler.stop_groups(tag_key, tag_value)
        elif schedule_action == "start":
            scheduler.start_groups(tag_key, tag_value)

    if spot_schedule == "terminate":
        spot_handler.spot_schedule(schedule_action, tag_key, tag_value)

    if ec2_schedule == "true":
        ec2_handler.ec2_schedule(schedule_action, tag_key, tag_value)

    if rds_schedule == "true":
        rds_handler.rds_schedule(schedule_action, tag_key, tag_value)
