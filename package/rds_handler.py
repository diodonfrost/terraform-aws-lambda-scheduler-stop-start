""" rds instances scheduler """

import logging
import boto3
from botocore.exceptions import ClientError

# Setup simple logging for INFO
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def rds_handler(schedule_action, tag_key, tag_value):
    """
       Aws rds scheduler function, stop or
       start cluster and  rds instances by using
       the tag defined.
    """

    # Define the connection
    rds = boto3.client('rds')

    # List rds clusters
    clusters_rds = rds.describe_db_clusters()

    # Retrieve rds cluster tags
    for cluster_rds in clusters_rds['DBClusters']:
        response_cluster = rds.list_tags_for_resource(ResourceName=cluster_rds['DBClusterArn'])
        taglist = response_cluster['TagList']

        # Check if the right tag is present
        rds_tag = False
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value:
                rds_tag = True

        # Retrieve rds cluster id
        cluster_id = cluster_rds['DBClusterIdentifier']

        # Stop rds cluster
        if schedule_action == 'stop' and rds_tag:
            try:
                rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                LOGGER.info("Stop rds cluster %s", cluster_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidDBClusterStateFault':
                    LOGGER.info("rds cluster %s is not started", cluster_id)
                else:
                    print("Unexpected error: %s" % e)

        # Stop rds cluster
        elif schedule_action == 'start' and rds_tag:
            try:
                rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                LOGGER.info("Start rds cluster %s", cluster_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidDBClusterStateFault':
                    LOGGER.info("rds cluster %s is not stopped", cluster_id)
                else:
                    print("Unexpected error: %s" % e)

    # List rds instances
    instances_rds = rds.describe_db_instances()

    # Retrieve rds instances tags
    for instance_rds in instances_rds['DBInstances']:
        reponse_instance = rds.list_tags_for_resource(ResourceName=instance_rds['DBInstanceArn'])
        taglist = reponse_instance['TagList']

        # Check if the right tag is present
        rds_tag = False
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value:
                rds_tag = True

        # Retrieve rds instance id
        instance_id = instance_rds['DBInstanceIdentifier']

        # Stop rds instance
        if schedule_action == 'stop' and rds_tag:
            try:
                rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                LOGGER.info("Stop rds instance %s", instance_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidDBInstanceState':
                    LOGGER.info("rds instance %s is not started", instance_id)
                else:
                    print("Unexpected error: %s" % e)

        # Start rds instance
        elif schedule_action == 'start' and rds_tag:
            try:
                rds.start_db_instance(DBInstanceIdentifier=instance_id)
                LOGGER.info("Start rds instance %s", instance_id)
            except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidDBInstanceState':
                    LOGGER.info("rds instance %s is not stopped", instance_id)
                else:
                    print("Unexpected error: %s" % e)
