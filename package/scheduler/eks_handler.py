# -*- coding: utf-8 -*-

"""eks instances scheduler."""

from typing import Dict, List

import boto3

from botocore.exceptions import ClientError

from scheduler.exceptions import eks_exception
from scheduler.filter_resources_by_tags import FilterByTags

print("EKS function initialised")

class EksScheduler(object):
    """Abstract eks scheduler in a class."""
    print("EKScheduler class initialised")
    def update_nodegroup(cluster_name,nodegroup_name,min_size,max_size,desired_size):
        print("EKScheduler class initialised")
        update = client.update_nodegroup_config(
            clusterName = cluster_name,
            nodegroupName = nodegroup_name,
            scalingConfig = {
                'minSize': min_size,
                'desiredSize': desired_size,
                'maxSize': max_size
            }
        )
        status_code = update['ResponseMetadata']['HTTPStatusCode']

        if status_code == 200:
            status = "OK"
        else: 
            status = "ERROR"

        return nodegroup_name + ": " + str(status_code) + " (" + status + ")"


    def __init__(self, region_name=None) -> None:
        """Initialize eks scheduler."""
        if region_name:
            self.eks = boto3.client("eks", region_name=region_name)
        else:
            self.eks = boto3.client("eks")
        self.tag_api = FilterByTags(region_name=region_name)

    def stop(self, aws_tags: List[Dict]) -> None:
        """Aws eks cluster and instance scale down function.

        Scale down eks clusters with defined tags.

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
        print("EKScheduler stopping")
        for cluster_arn in self.tag_api.get_resources("eks:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            list_nodegroups = []
            try:
                # Identifier must be cluster id, not resource id
                self.eks.describe_eks_clusters(ClusterIdentifier=cluster_id)
                list_nodegroups.append(client.list_nodegroups(clusterName = cluster_id)) 
                for nodegroup in list_nodegroups:
                   self.eks.update_nodegroup(cluster_name=cluster_id,nodegroup_name=nodegroup,min_size=eks_config_paused[0],max_size=eks_config_paused[1],desired_size=eks_config_paused[2])
                   print("Scale up NodeGroup {0}".format(nodegroup))
            except ClientError as exc:
                eks_exception("EKS cluster", cluster_id, exc)

    def start(self, aws_tags: List[Dict]) -> None:
        """Aws eks cluster and instance scale up function.

        Scale up eks clusters with defined tags.

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
        print("EKScheduler starting")
        for cluster_arn in self.tag_api.get_resources("eks:cluster", aws_tags):
            cluster_id = cluster_arn.split(":")[-1]
            list_nodegroups = []
            try:
                # Identifier must be cluster id, not resource id
                self.eks.describe_eks_clusters(ClusterIdentifier=cluster_id)
                list_nodegroups.append(client.list_nodegroups(clusterName = cluster_id)) 
                for nodegroup in list_nodegroups:
                  self.eks.update_nodegroup(nodegroup_name=cluster_id,min_size=eks_config_resume[0],max_size=eks_config_resume[1],desired_size=eks_config_resume[2])
                print("Scale down NodeGroup {0}".format(nodegroup))
            except ClientError as exc:
                eks_exception("eks cluster", cluster_id, exc)
