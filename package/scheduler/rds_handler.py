# -*- coding: utf-8 -*-

"""rds instances scheduler."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from .exceptions import rds_exception


class RdsScheduler(object):
    """Abstract rds scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize rds scheduler."""
        if region_name:
            self.rds = boto3.client("rds", region_name=region_name)
        else:
            self.rds = boto3.client("rds")

    def stop(self, tag_key: str, tag_value: str) -> None:
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
            except ClientError as exc:
                rds_exception("rds cluster", cluster_id, exc)

        for instance_id in self.list_instances(tag_key, tag_value):
            try:
                self.rds.stop_db_instance(DBInstanceIdentifier=instance_id)
                print("Stop rds instance {0}".format(instance_id))
            except ClientError as exc:
                rds_exception("rds instance", instance_id, exc)

    def start(self, tag_key: str, tag_value: str) -> None:
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
            except ClientError as exc:
                rds_exception("rds cluster", cluster_id, exc)

        for instance_id in self.list_instances(tag_key, tag_value):
            try:
                self.rds.start_db_instance(DBInstanceIdentifier=instance_id)
                print("Start rds instance {0}".format(instance_id))
            except ClientError as exc:
                rds_exception("rds instance", instance_id, exc)

    def list_clusters(self, tag_key: str, tag_value: str) -> Iterator[str]:
        """Aws rds cluster list function.

        Return the list of all rds clusters

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :yield Iterator[str]:
            The list Id of filtered rds clusters
        """
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
                        yield custer["DBClusterIdentifier"]

    def list_instances(self, tag_key: str, tag_value: str) -> Iterator[str]:
        """Aws rds instance list function.

        Return the list of all rds instances

        :param str tag_key:
            Aws tag key to use for filter resources
        :param str tag_value:
            Aws tag value to use for filter resources

        :yield Iterator[str]:
            The list Id of filtered rds instances
        """
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
                        yield instance["DBInstanceIdentifier"]
