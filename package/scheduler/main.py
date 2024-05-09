"""This script stop and start aws resources."""
import os
import holidays
from datetime import datetime

from .autoscaling_handler import AutoscalingScheduler
from .cloudwatch_handler import CloudWatchAlarmScheduler
from .documentdb_handler import DocumentDBScheduler
from .ecs_handler import EcsScheduler
from .instance_handler import InstanceScheduler
from .rds_handler import RdsScheduler
from .redshift_handler import RedshiftScheduler


def lambda_handler(event, context):
    """Main function entrypoint for lambda.

    Stop and start AWS resources:
    - rds instances
    - rds aurora clusters
    - instance ec2
    - ecs services
    - redshift clusters

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

    # Optionally quit here on holidays
    schedule_disable_holidays = strtobool(os.getenv("SCHEDULE_DISABLE_HOLIDAYS"))
    schedule_holidays_country = os.getenv("SCHEDULE_HOLIDAYS_COUNTRY")
    if schedule_disable_holidays and schedule_holidays_country != "":
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        country_holidays = holidays.country_holidays(country=schedule_holidays_country, years=int(now.strftime("%Y")))
        if today in country_holidays:
            msg = "Stopping gracefully now because today ({}) is a holiday in {}: {}".format(today, 
                                                                                             schedule_holidays_country, 
                                                                                             country_holidays.get(today))
            print(msg)
            return {'result': msg}
        else:
            print("Today ({}) is no holiday - proceeding...".format(today))

    _strategy = {
        AutoscalingScheduler: os.getenv("AUTOSCALING_SCHEDULE"),
        DocumentDBScheduler: os.getenv("DOCUMENTDB_SCHEDULE"),
        InstanceScheduler: os.getenv("EC2_SCHEDULE"),
        EcsScheduler: os.getenv("ECS_SCHEDULE"),
        RdsScheduler: os.getenv("RDS_SCHEDULE"),
        RedshiftScheduler: os.getenv("REDSHIFT_SCHEDULE"),
        CloudWatchAlarmScheduler: os.getenv("CLOUDWATCH_ALARM_SCHEDULE"),
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
