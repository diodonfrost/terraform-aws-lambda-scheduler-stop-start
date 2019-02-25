""" rds instances scheduler """

import logging
import boto3

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

        # Filter rds cluster with their tag and state
        for tag in taglist:
            if tag['Key'] == tag_key and tag['Value'] == tag_value:

                # Retrieve rds cluster id
                cluster_id = cluster_rds['DBClusterIdentifier']

                if schedule_action == 'stop' and cluster_rds['Status'] == 'available':
                    rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                    LOGGER.info("Stop rds cluster %s", cluster_id)

                elif schedule_action == 'start' and cluster_rds['Status'] == 'stopped':
                    rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                    LOGGER.info("Start rds cluster %s", cluster_id)

    # List rds instances
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

                if schedule_action == 'stop' and \
                instance_rds['DBInstanceStatus'] == 'available':
                    rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                    LOGGER.info("Stop rds instance %s", instance_id)

                elif schedule_action == 'start' and \
                instance_rds['DBInstanceStatus'] == 'stopped':
                    rds.start_db_instance(DBInstanceIdentifier=instance_id)
                    LOGGER.info("Start rds instance %s", instance_id)
