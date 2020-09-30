# -*- coding: utf-8 -*-

"""rds instances scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import rds_exception
from scheduler.filter_resources_by_tags import FilterByTags


class RdsScheduler(object):
    """Abstract rds scheduler in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize rds scheduler."""
        if region_name:
            self.rds = boto3.client("rds", region_name=region_name)
        else:
            self.rds = boto3.client("rds")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws rds cluster and instance stop function.

        Stop rds aurora clusters and rds db instances with defined tags.

        :param list[map] aws_tags:
            Aws tags to use for filter resources.
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        for cluster_arn in self.tag_api.get_resources("rds:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                # Identifier must be cluster id, not resource id
                self.rds.describe_db_clusters(DBClusterIdentifier=cluster_id)
                self.rds.stop_db_cluster(DBClusterIdentifier=cluster_id)
                print("Stop rds cluster {0}".format(cluster_id))
            except ClientError as exc:
                rds_exception("rds cluster", cluster_id, exc)

        for db_arn in self.tag_api.get_resources("rds:db", aws_tags):
            db_id = db_arn.split(":")[-1]
            try:
                self.rds.stop_db_instance(DBInstanceIdentifier=db_id)
                print("Stop rds instance {0}".format(db_id))
            except ClientError as exc:
                rds_exception("rds instance", db_id, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws rds cluster start function.

        Start rds aurora clusters and db instances with defined tags.

        :param list[map] aws_tags:
            Aws tags to use for filter resources.
            For example:
            [
                {
                    'Key': 'string',
                    'Values': [
                        'string',
                    ]
                }
            ]
        """
        for cluster_arn in self.tag_api.get_resources("rds:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            try:
                # Identifier must be cluster id, not resource id
                self.rds.describe_db_clusters(DBClusterIdentifier=cluster_id)
                self.rds.start_db_cluster(DBClusterIdentifier=cluster_id)
                print("Start rds cluster {0}".format(cluster_id))
            except ClientError as exc:
                rds_exception("rds cluster", cluster_id, exc)

        for db_arn in self.tag_api.get_resources("rds:db", aws_tags):
            db_id = db_arn.split(":")[-1]
            try:
                self.rds.start_db_instance(DBInstanceIdentifier=db_id)
                print("Start rds instance {0}".format(db_id))
            except ClientError as exc:
                rds_exception("rds instance", db_id, exc)
