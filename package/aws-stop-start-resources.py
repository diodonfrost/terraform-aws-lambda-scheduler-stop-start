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
autoscaling_schedule = os.getenv('AUTOSCALING_SCHEDULE', 'true')

# Setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the connection
EC2 = boto3.client('ec2')
RDS = boto3.client('rds')
AUTOSCALING = boto3.client('autoscaling')

# Initialize instance list
instance_list = []

def lambda_handler(event, context):

    ############################
    #
    # Autoscaling scheduler
    #
    ############################
    if autoscaling_schedule == 'true':
        scalinggroup = AUTOSCALING.describe_auto_scaling_groups()

        # Retrieve ec2 autoscalinggroup tags
        for group in scalinggroup['AutoScalingGroups']:
            response = AUTOSCALING.describe_tags()
            taglist = response['Tags']

            # Filter ec2 autoscalinggroup with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

      	            # Retrieve autoscaling group name
                    autoscaling_name = group['AutoScalingGroupName']

                    # Retrieve state of autoscaling group
                    autoscaling_state = AUTOSCALING.describe_scaling_process_types()

                    if schedule_action == 'stop' and next((item for item in \
                    autoscaling_state['Processes'] if item["ProcessName"] == "Launch"), False):
                        # Suspend autoscaling group for shutdown instance
                        AUTOSCALING.suspend_processes(AutoScalingGroupName=autoscaling_name)

                    elif schedule_action == 'start' and next((item for item in \
                    autoscaling_state['Processes'] if item["ProcessName"] != "Launch"), False):
                        # Resume autoscaling group for startup instances
                        AUTOSCALING.resume_processes(AutoScalingGroupName=autoscaling_name)


    ############################
    #
    # EC2 instances scheduler
    #
    ############################
    if ec2_schedule == 'true':
        reservations = EC2.describe_instances()

        # Retrieve ec2 instances tags
        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                response = EC2.describe_tags()
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
            EC2.stop_instances(InstanceIds=instance_list)
        elif len(instance_list) > 0 and schedule_action == 'start':
            # Start instances in list
            EC2.start_instances(InstanceIds=instance_list)


    ############################
    #
    # RDS scheduler
    #
    ############################
    if rds_schedule == 'true':

        # RDS clusters
        clusters_rds = RDS.describe_db_clusters()

        # Retrieve rds cluster tags
        for cluster_rds in clusters_rds['DBClusters']:
            response_cluster = RDS.list_tags_for_resource(ResourceName=cluster_rds['DBClusterArn'])
            taglist = response_cluster['TagList']

            # Filter rds cluster with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve rds cluster id
                    cluster_id = cluster_rds['DBClusterIdentifier']

                    if schedule_action == 'stop' and cluster_rds['Status'] == 'available':
                        RDS.stop_db_cluster(DBClusterIdentifier=cluster_id)

                    elif schedule_action == 'start' and cluster_rds['Status'] == 'stopped':
                        RDS.start_db_cluster(DBClusterIdentifier=cluster_id)

        # RDS instances
        instances_rds = RDS.describe_db_instances()

        # Retrieve rds instances tags
        for instance_rds in instances_rds['DBInstances']:
            reponse_instance = RDS.list_tags_for_resource(ResourceName=instance_rds['DBInstanceArn'])
            taglist = reponse_instance['TagList']

            # Filter rds instance with their tag and state
            for tag in taglist:
                if tag['Key'] == tag_key and tag['Value'] == tag_value:

                    # Retrieve rds instance id
                    instance_id = instance_rds['DBInstanceIdentifier']

                    if schedule_action == 'stop' and \
                    instance_rds['DBInstanceStatus'] == 'available':
                        RDS.stop_db_instance(DBInstanceIdentifier=instance_id)

                    elif schedule_action == 'start' and \
                    instance_rds['DBInstanceStatus'] == 'stopped':
                        RDS.start_db_instance(DBInstanceIdentifier=instance_id)
