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
    if schedule_action == "stop":
        rds_stop_clusters(tag_key, tag_value)
        rds_stop_instances(tag_key, tag_value)
    elif schedule_action == "start":
        rds_start_clusters(tag_key, tag_value)
        rds_start_instances(tag_key, tag_value)
    else:
        logging.error("Bad scheduler action")


def rds_stop_clusters(tag_key, tag_value):
    """Rds stop cluster function.

    Shuting donw Aurora clusters with defined tag.
    """
    rds = boto3.client("rds")

    for cluster_id in rds_list_clusters(tag_key, tag_value):
        try:
            rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
            print("Stop rds cluster {0}".format(cluster_id))
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidDBClusterStateFault":
                logging.info("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def rds_stop_instances(tag_key, tag_value):
    """Rds stop instance function.

    Shuting donw rds instances with defined tag.
    """
    rds = boto3.client("rds")

    for instance_id in rds_list_instances(tag_key, tag_value):
        try:
            rds.stop_db_instance(DBInstanceIdentifier=instance_id)
            print("Stop rds instance {0}".format(instance_id))
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidDBInstanceState":
                logging.info("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def rds_start_clusters(tag_key, tag_value):
    """Rds start cluster function.

    Starting up Aurora clusters with defined tag.
    """
    rds = boto3.client("rds")

    for cluster_id in rds_list_clusters(tag_key, tag_value):
        try:
            rds.start_db_cluster(DBClusterIdentifier=cluster_id)
            print("Start rds cluster {0}".format(cluster_id))
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidDBClusterStateFault":
                logging.info("%s", e)
            else:
                logging.error("Unexpected error: %s", e)


def rds_start_instances(tag_key, tag_value):
    """Rds start instance function.

    Shuting donw rds instances with defined tag.
    """
    rds = boto3.client("rds")

    for instance_id in rds_list_instances(tag_key, tag_value):
        try:
            rds.start_db_instance(DBInstanceIdentifier=instance_id)
            print("Start rds instance {0}".format(instance_id))
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidDBInstanceState":
                logging.info("%s", e)
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
                    cluster_list.append(cluster_rds["DBClusterIdentifier"])
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
                    instance_list.append(instance_rds["DBInstanceIdentifier"])
    return instance_list
