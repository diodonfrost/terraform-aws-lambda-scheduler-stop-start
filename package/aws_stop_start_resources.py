"""This script stop and start aws resources"""

import logging
import os
import boto3

# Retrieve variables from Lmanda ENVIRONMENT
schedule_action = os.getenv('SCHEDULE_ACTION', 'stop')
schedule_action = schedule_action.capitalize()

tag_key = os.getenv('TAG_KEY', 'tostop')
tag_key = tag_key.capitalize()

tag_value = os.getenv('TAG_VALUE', 'true')
tag_value = tag_value.capitalize()

ec2_schedule = os.getenv('EC2_SCHEDULE', 'true')
ec2_schedule = ec2_schedule.capitalize()

rds_schedule = os.getenv('RDS_SCHEDULE', 'true')
rds_schedule = rds_schedule.capitalize()

autoscaling_schedule = os.getenv('AUTOSCALING_SCHEDULE', 'true')
autoscaling_schedule = autoscaling_schedule.capitalize()

# Setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the connection
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
autoscaling = boto3.client('autoscaling')

# Initialize instance list
instance_list = []

def lambda_handler(event, context):


    ########################
    #
    # EC2 instance shutdown
    #
    ########################
    reservations = ec2.describe_instances()

    # Retrieve ec2 instances tags
    for reservation in reservations['Reservations']:
        for instance in reservation['Instances']:
            response = ec2.describe_tags()
            taglist = response['Tags']

            # Filter ec2 instances with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value \
                and instance['State']['Name'] == 'running':

                    # Retrieve ec2 instance id and add in list
                    instance_id = instance['InstanceId']
                    instance_list.insert(0, instance_id)

    # Stop instances in list
    ec2.stop_instances(InstanceIds=instance_list)


    ########################
    #
    # autoscaling shutdown
    #
    ########################
    scalinggroup = autoscaling.describe_auto_scaling_groups()

    # Retrieve ec2 autoscalinggroup tags
    for group in scalinggroup['AutoScalingGroups']:
        response = autoscaling.describe_tags()
        taglist = response['Tags']

        # Filter ec2 autoscalinggroup with their tag and state
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value \
            and group['DesiredCapacity'] != '0':

                # Set autoscalinggroup minsize and desired capacity to 0
                autoscaling_name = group['AutoScalingGroupName']
                autoscaling.update_auto_scaling_group(AutoScalingGroupName=autoscaling_name, \
                MinSize=0, DesiredCapacity=0)


    ########################
    #
    # RDS shutdown
    #
    ########################
    clusters = rds.describe_db_clusters()

    # Retrieve rds cluster tags
    for cluster in clusters['DBClusters']:
        response = rds.list_tags_for_resource(ResourceName=cluster['DBClusterArn'])
        taglist = response['TagList']

        # Filter rds cluster with their tag and state
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value and \
            cluster['Status'] == 'available':

                # Retrieve rds cluster id and stop it
                cluster_id = cluster['DBClusterIdentifier']
                rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
