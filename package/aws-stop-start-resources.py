"""This script stop and start aws resources"""

import logging
import os
import boto3

# Retrieve variables from Lmanda ENVIRONMENT
schedule_action = os.getenv('SCHEDULE_ACTION', 'stop')
tag_key = os.getenv('TAG_KEY', 'tostop')
tag_value = os.getenv('TAG_VALUE', 'true')
ec2_schedule = os.getenv('EC2_SCHEDULE', 'true')
rds_schedule = os.getenv('RDS_SCHEDULE', 'true')

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
    if ec2_schedule == 'true':
        reservations = ec2.describe_instances()

        # Retrieve ec2 instances tags
        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                response = ec2.describe_tags()
                taglist = response['Tags']

                # Filter ec2 instances with their tag and state
                for tag in taglist:
                    if tag['Key'] == tag_key and tag['Value'] == tag_value:

                      if schedule_action == 'stop' and \
                      instance['State']['Name'] == 'running':

                          # Retrieve ec2 instance id and add in list
                          instance_id = instance['InstanceId']
                          instance_list.insert(0, instance_id)

                      if schedule_action == 'start' and \
                      instance['State']['Name'] == 'stopped':

                          # Retrieve ec2 instance id and add in list
                          instance_id = instance['InstanceId']
                          instance_list.insert(0, instance_id)

        if len(instance_list) > 0 and schedule_action == 'stop':
            # Stop instances in list
            ec2.stop_instances(InstanceIds=instance_list)
        elif len(instance_list) > 0 and schedule_action == 'start':
            # Start instances in list
            ec2.start_instances(InstanceIds=instance_list)


    ########################
    #
    # RDS shutdown
    #
    ########################
    if rds_schedule == 'true':

        # RDS clusters
        clusters_rds = rds.describe_db_clusters()

        # Retrieve rds cluster tags
        for cluster_rds in clusters_rds['DBClusters']:
            response_cluster = rds.list_tags_for_resource(ResourceName=cluster_rds['DBClusterArn'])
            taglist = response_cluster['TagList']

            # Filter rds cluster with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve rds cluster id
                    cluster_id = cluster_rds['DBClusterIdentifier']

                    if schedule_action == 'stop' and cluster_rds['Status'] == 'available':
                        rds.stop_db_cluster(DBClusterIdentifier=cluster_id)

                    elif schedule_action == 'start' and cluster_rds['Status'] == 'stopped':
                        rds.start_db_cluster(DBClusterIdentifier=cluster_id)

        # RDS instances
        instances_rds = rds.describe_db_instances()

        # Retrieve rds instances tags
        for instance_rds in instances_rds['DBInstances']:
            reponse_instance = rds.list_tags_for_resource(ResourceName=instance_rds['DBInstanceArn'])
            taglist = reponse_instance['TagList']

            # Filter rds instance with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve rds instance id
                    instance_id = instance_rds['DBInstanceIdentifier']

                    if schedule_action == 'stop' and instance_rds['DBInstanceStatus'] == 'available':
                        rds.stop_db_instance(DBInstanceIdentifier=instance_id)

                    elif schedule_action == 'start' and instance_rds['DBInstanceStatus'] == 'stopped':
                        rds.start_db_instance(DBInstanceIdentifier=instance_id)
