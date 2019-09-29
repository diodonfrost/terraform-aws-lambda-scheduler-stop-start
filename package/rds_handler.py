# -*- coding: utf-8 -*-

"""rds instances scheduler."""

import logging

import boto3

from botocore.exceptions import ClientError


class RdsScheduler:
    """Abstract rds scheduler in a class."""

    def __init__(self):
        """Initialize autoscaling scheduler."""
        #: Initialize aws ec2 resource
        self.rds = boto3.client("rds")

    def stop(self, tag_key, tag_value):
        """Aws rds cluster and instance stop function.

        Stop rds aurora clusters and rds db instances with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for cluster_id in self.list_clusters(tag_key, tag_value):
            try:
                self.rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                print("Stop rds cluster {0}".format(cluster_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBClusterStateFault":
                    logging.info("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

        for instance_id in self.list_instances(tag_key, tag_value):
            try:
                self.rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                print("Stop rds instance {0}".format(instance_id))
            except ClientError as e:
                if e.response["Error"]["Code"] == "InvalidDBInstanceState":
                    logging.info("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def start(self, tag_key, tag_value):
        """Aws rds cluster start function.

        Start rds aurora clusters and db instances a with defined tag.

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources
        """
        for cluster_id in self.list_clusters(tag_key, tag_value):
            try:
                self.rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                print("Start rds cluster {0}".format(cluster_id))
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "InvalidDBClusterStateFault":
                    logging.info("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

        for instance_id in self.list_instances(tag_key, tag_value):
            try:
                self.rds.start_db_instance(DBInstanceIdentifier=instance_id)
                print("Start rds instance {0}".format(instance_id))
            except ClientError as e:
                if e.response["Error"]["Code"] == "InvalidDBInstanceState":
                    logging.info("%s", e)
                else:
                    logging.error("Unexpected error: %s", e)

    def list_clusters(self, tag_key, tag_value):
        """Aws rds cluster list function.

        Return the list of all rds clusters

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :return list cluster_list:
            The list Id of filtered rds clusters
        """
        cluster_list = []
        paginator = self.rds.get_paginator("describe_db_clusters")

        for page in paginator.paginate():
            for custer in page["DBClusters"]:
                response_cluster = self.rds.list_tags_for_resource(
                    ResourceName=custer["DBClusterArn"]
                )
                taglist = response_cluster["TagList"]

                # Retrieve rds cluster with specific tag
                for tag in taglist:
                    if tag["Key"] == tag_key and tag["Value"] == tag_value:
                        cluster_list.append(custer["DBClusterIdentifier"])
        return cluster_list

    def list_instances(self, tag_key, tag_value):
        """Aws rds instance list function.

        Return the list of all rds instances

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :return list instance_list:
            The list Id of filtered rds instances
        """
        instance_list = []
        paginator = self.rds.get_paginator("describe_db_instances")

        for page in paginator.paginate():
            for instance in page["DBInstances"]:
                reponse_instance = self.rds.list_tags_for_resource(
                    ResourceName=instance["DBInstanceArn"]
                )
                taglist = reponse_instance["TagList"]

                # Retrieve rds instance with specific tag
                for tag in taglist:
                    if tag["Key"] == tag_key and tag["Value"] == tag_value:
                        instance_list.append(instance["DBInstanceIdentifier"])
        return instance_list
