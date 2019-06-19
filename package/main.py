"""This script stop and start aws resources"""

import os

import autoscaling_handler
import ec2_handler
import rds_handler


def lambda_handler(event, context):
    """ Main function entrypoint for lambda """

    # Retrieve variables from aws lambda ENVIRONMENT
    schedule_action = os.getenv('SCHEDULE_ACTION', 'stop')
    tag_key = os.getenv('TAG_KEY', 'tostop')
    tag_value = os.getenv('TAG_VALUE', 'true')
    ec2_schedule = os.getenv('EC2_SCHEDULE', 'true')
    rds_schedule = os.getenv('RDS_SCHEDULE', 'true')
    autoscaling_schedule = os.getenv('AUTOSCALING_SCHEDULE', 'true')

    if autoscaling_schedule == 'true':
        autoscaling_handler.autoscaling_schedule(
            schedule_action, tag_key, tag_value)

    if ec2_schedule == 'true':
        ec2_handler.ec2_schedule(
            schedule_action, tag_key, tag_value)

    if rds_schedule == 'true':
        rds_handler.rds_schedule(
            schedule_action, tag_key, tag_value)
