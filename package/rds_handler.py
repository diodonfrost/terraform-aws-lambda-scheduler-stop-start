# -*- coding: utf-8 -*-

"""rds instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


def rds_schedule(schedule_action, tag_key, tag_value):
    """Aws rds scheduler function.

    Stop or start Aurora cluster and rds instances
    by using the defined tag.
    """
    rds = boto3.client("rds")

    for cluster_id in rds_list_clusters(tag_key, tag_value):
        # Stop Aurora cluster
        if schedule_action == "stop":
            try:
                rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                print("Stop rds cluster {0}".format(cluster_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBClusterStateFault":
                    logging.info("rds cluster %s is not started", cluster_id)
                else:
                    logging.error("Unexpected error: %s", e)

        # Start Aurora cluster
        elif schedule_action == "start":
            try:
                rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                print("Start rds cluster {0}".format(cluster_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBClusterStateFault":
                    logging.info("rds cluster %s is not stopped", cluster_id)
                else:
                    logging.error("Unexpected error: %s", e)

    for instance_id in rds_list_instances(tag_key, tag_value):
        if schedule_action == "stop":
            try:
                rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                print("Stop rds instance {0}".format(instance_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBInstanceState":
                    logging.info(
                        "rds instance %s is not started", instance_id
                    )
                else:
                    logging.error("Unexpected error: %s", e)

        elif schedule_action == "start":
            try:
                rds.start_db_instance(DBInstanceIdentifier=instance_id)
                print("Start rds instance {0}".format(instance_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBInstanceState":
                    logging.info(
                        "rds instance %s is not stopped", instance_id
                    )
                else:
                    logging.error("Unexpected error: %s", e)


def rds_list_clusters(tag_key, tag_value):
    """Aws rds list cluster function.

    List all rds clusters name with specific tag.
    """
    cluster_list = []
    rds = boto3.client("rds")
    paginator = rds.get_paginator("describe_db_clusters")

    for page in paginator.paginate():
        for cluster_rds in page["DBClusters"]:
            response_cluster = rds.list_tags_for_resource(
                ResourceName=cluster_rds["DBClusterArn"]
            )
            taglist = response_cluster["TagList"]

            # Retrieve rds cluster with specific tag
            for tag in taglist:
                if tag["Key"] == tag_key and tag["Value"] == tag_value:
                    cluster_id = cluster_rds["DBClusterIdentifier"]
                    cluster_list.insert(0, cluster_id)
    return cluster_list


def rds_list_instances(tag_key, tag_value):
    """Aws rds list instance function.

    List all rds instances name with specific tag.
    """
    instance_list = []
    rds = boto3.client("rds")
    paginator = rds.get_paginator("describe_db_instances")

    for page in paginator.paginate():
        for instance_rds in page["DBInstances"]:
            reponse_instance = rds.list_tags_for_resource(
                ResourceName=instance_rds["DBInstanceArn"]
            )
            taglist = reponse_instance["TagList"]

            # Retrieve rds instance with specific tag
            for tag in taglist:
                if tag["Key"] == tag_key and tag["Value"] == tag_value:
                    instance_id = instance_rds["DBInstanceIdentifier"]
                    instance_list.insert(0, instance_id)
    return instance_list
