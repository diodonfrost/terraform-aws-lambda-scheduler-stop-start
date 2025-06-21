"""This script stop and start aws resources."""

import json
import logging
import os
from datetime import datetime

from .autoscaling_handler import AutoscalingScheduler
from .cloudwatch_handler import CloudWatchAlarmScheduler
from .documentdb_handler import DocumentDBScheduler
from .ecs_handler import EcsScheduler
from .instance_handler import InstanceScheduler
from .rds_handler import RdsScheduler
from .redshift_handler import RedshiftScheduler
from .transfer_handler import TransferScheduler


def lambda_handler(event, context):
    """Main function entrypoint for lambda.

    Stop and start AWS resources:
    - rds instances
    - rds aurora clusters
    - instance ec2
    - ecs services
    - redshift clusters
    - transfer servers

    Suspend and resume AWS resources:
    - ec2 autoscaling groups

    Terminate spot instances (spot instance cannot be stopped by a user)
    """
    # Retrieve variables from aws lambda ENVIRONMENT
    schedule_action = os.getenv("SCHEDULE_ACTION")
    aws_regions = os.getenv("AWS_REGIONS").replace(" ", "").split(",")
    format_tags = [{"Key": os.getenv("TAG_KEY"), "Values": [os.getenv("TAG_VALUE")]}]
    autoscaling_terminate_instances = strtobool(
        os.getenv("AUTOSCALING_TERMINATE_INSTANCES")
    )
    excluded_dates = json.loads(os.environ.get("SCHEDULER_EXCLUDED_DATES", "[]"))

    if is_date_excluded(excluded_dates):
        return

    _strategy = {
        AutoscalingScheduler: os.getenv("AUTOSCALING_SCHEDULE"),
        DocumentDBScheduler: os.getenv("DOCUMENTDB_SCHEDULE"),
        InstanceScheduler: os.getenv("EC2_SCHEDULE"),
        EcsScheduler: os.getenv("ECS_SCHEDULE"),
        RdsScheduler: os.getenv("RDS_SCHEDULE"),
        RedshiftScheduler: os.getenv("REDSHIFT_SCHEDULE"),
        CloudWatchAlarmScheduler: os.getenv("CLOUDWATCH_ALARM_SCHEDULE"),
        TransferScheduler: os.getenv("TRANSFER_SCHEDULE"),
    }

    for service, to_schedule in _strategy.items():
        if strtobool(to_schedule):
            for aws_region in aws_regions:
                strategy = service(aws_region)
                if service == AutoscalingScheduler and autoscaling_terminate_instances:
                    getattr(strategy, schedule_action)(
                        aws_tags=format_tags, terminate_instances=True
                    )
                else:
                    getattr(strategy, schedule_action)(aws_tags=format_tags)


def strtobool(value: str) -> bool:
    """Convert string to boolean."""
    return value.lower() in ("yes", "true", "t", "1")


def is_date_excluded(excluded_dates: list[str]) -> bool:
    """Check if the current date should be excluded from scheduling.

    Args:
        excluded_dates: List of dates in MM-DD format to exclude

    Returns:
        True if current date should be excluded, False otherwise
    """
    if not excluded_dates:
        return False

    current_date = datetime.now()
    current_date_str = current_date.strftime("%m-%d")

    if current_date_str in excluded_dates:
        logging.info(
            "Skipping execution - current date (%s) is in excluded dates: %s",
            current_date_str,
            excluded_dates,
        )
        return True

    return False
