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
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Define the connection
EC2 = boto3.client('ec2')
RDS = boto3.client('rds')
AUTOSCALING = boto3.client('autoscaling')


############################
#
# Autoscaling scheduler
#
############################

def autoscaling_handler():
    """
       Aws autoscaling scheduler function, suspend or
       resume all scaling processes by using the tag defined.
    """
    scalinggroup = AUTOSCALING.describe_auto_scaling_groups()
    autoscaling_instances = AUTOSCALING.describe_auto_scaling_instances()

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
                    LOGGER.info("Suspend autoscaling group %s", autoscaling_name)

                    # Terminate all instances in autoscaling group
                    for instance in autoscaling_instances['AutoScalingInstances']:
                        AUTOSCALING.terminate_instance_in_auto_scaling_group(\
                        InstanceId=instance['InstanceId'], ShouldDecrementDesiredCapacity=False)
                        LOGGER.info("Terminate autoscaling instance %s", instance['InstanceId'])

                elif schedule_action == 'start' and next((item for item in \
                autoscaling_state['Processes'] if item["ProcessName"] != "Launch"), False):
                    # Resume autoscaling group for startup instances
                    AUTOSCALING.resume_processes(AutoScalingGroupName=autoscaling_name)
                    LOGGER.info("Resume autoscaling group %s", autoscaling_name)


############################
#
# EC2 instances scheduler
#
############################

def ec2_handler():
    """
       Aws ec2 scheduler function, stop or
       start ec2 instances by using the tag defined.
    """
    # Initialize instance list
    instance_list = []
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

                    elif schedule_action == 'start' and \
                    instance['State']['Name'] == 'stopped':

                        # Retrieve ec2 instance id and add in list
                        instance_id = instance['InstanceId']
                        instance_list.insert(0, instance_id)

    if instance_list and schedule_action == 'stop':
        # Stop instances in list
        EC2.stop_instances(InstanceIds=instance_list)
        LOGGER.info("Stop instance %s", instance_list)

    elif instance_list and schedule_action == 'start':
        # Start instances in list
        EC2.start_instances(InstanceIds=instance_list)
        LOGGER.info("Start instance %s", instance_list)


############################
#
# RDS scheduler
#
############################
def rds_handler():
    """
       Aws rds scheduler function, stop or
       start cluster and  rds instances by using
       the tag defined.
    """
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
                    LOGGER.info("Stop rds cluster %s", cluster_id)

                elif schedule_action == 'start' and cluster_rds['Status'] == 'stopped':
                    RDS.start_db_cluster(DBClusterIdentifier=cluster_id)
                    LOGGER.info("Start rds cluster %s", cluster_id)

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
                    LOGGER.info("Stop rds instance %s", instance_id)

                elif schedule_action == 'start' and \
                instance_rds['DBInstanceStatus'] == 'stopped':
                    RDS.start_db_instance(DBInstanceIdentifier=instance_id)
                    LOGGER.info("Start rds instance %s", instance_id)

def lambda_handler(event, context):
    """ Main function entrypoint for lambda """

    if autoscaling_schedule == 'true':
        autoscaling_handler()

    if ec2_schedule == 'true':
        ec2_handler()

    if rds_schedule == 'true':
        rds_handler()
