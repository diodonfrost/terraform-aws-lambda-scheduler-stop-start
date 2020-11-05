# -*- coding: utf-8 -*-

"""Module use by ec2 scheduler unit tests."""

import boto3
import time
from random import randint


def launch_ec2_instances(count, region_name, tag_key, tag_value):
    """Create ec2 instances."""
    client = boto3.client("ec2", region_name=region_name)
    response = client.run_instances(
        ImageId="ami-02df9ea15c1778c9c",
        InstanceType="t2.micro",
        MaxCount=count,
        MinCount=count,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "instance_test"},
                    {"Key": tag_key, "Value": tag_value},
                ],
            }
        ],
    )
    return response


def launch_ec2_spot(count, region_name, tag_key, tag_value):
    """Create ec2 spot instances."""
    client = boto3.client("ec2", region_name=region_name)
    response = client.run_instances(
        ImageId="ami-02df9ea15c1778c9c",
        MaxCount=count,
        MinCount=count,
        InstanceMarketOptions={
            "MarketType": "spot",
            "SpotOptions": {
                "SpotInstanceType": "one-time",
                "InstanceInterruptionBehavior": "terminate",
            },
        },
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "instance_test"},
                    {"Key": tag_key, "Value": tag_value},
                ],
            }
        ],
    )
    return response


def launch_asg(region_name, tag_key, tag_value, launch_conf_name, asg_name):
    """Create autoscaling group with defined aws tags."""
    client = boto3.client("autoscaling", region_name=region_name)
    launch_config = client.create_launch_configuration(
        LaunchConfigurationName=launch_conf_name,
        ImageId="ami-02df9ea15c1778c9c",
        InstanceType="t2.micro",
    )
    asg = client.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        MaxSize=5,
        DesiredCapacity=3,
        MinSize=1,
        LaunchConfigurationName=launch_conf_name,
        AvailabilityZones=[region_name + "a", region_name + "b"],
        Tags=[
            {
                "ResourceId": asg_name,
                "ResourceType": "auto-scaling-group",
                "Key": tag_key,
                "Value": tag_value,
                "PropagateAtLaunch": True,
            }
        ],
    )
    time.sleep(15)
    return launch_config, asg


def launch_rds_instance(region_name, tag_key, tag_value):
    """Create rds instances with defined aws tags."""
    client = boto3.client("rds", region_name=region_name)
    name_prefix = str(randint(0, 1000000000))
    response = client.create_db_instance(
        DBInstanceIdentifier="dbinstance" + name_prefix,
        AllocatedStorage=10,
        BackupRetentionPeriod=0,
        DBName="dbinstance" + name_prefix,
        DBInstanceClass="db.m5.large",
        Engine="mariadb",
        MasterUsername="root",
        MasterUserPassword="IamNotHere",
        Tags=[
            {"Key": "Name", "Value": "dbinstance" + name_prefix},
            {"Key": tag_key, "Value": tag_value},
        ],
    )
    return response


def launch_rds_cluster(region_name, tag_key, tag_value):
    """Create rds cluster with defined aws tags."""
    client = boto3.client("rds", region_name=region_name)
    name_prefix = str(randint(0, 1000000000))
    rds_cluster = client.create_db_cluster(
        DBClusterIdentifier="dbcluster" + name_prefix,
        Engine="aurora-mysql",
        EngineMode="provisioned",
        MasterUsername="root",
        MasterUserPassword="IamNotHere",
        Tags=[
            {"Key": "Name", "Value": "dbinstance"},
            {"Key": tag_key, "Value": tag_value},
        ],
    )

    rds_instance = client.create_db_instance(
        DBInstanceIdentifier="dbinstance" + name_prefix,
        DBClusterIdentifier=rds_cluster["DBCluster"]["DBClusterIdentifier"],
        Engine="aurora-mysql",
        DBInstanceClass="db.r5.large",
        Tags=[
            {"Key": "Name", "Value": "dbinstance"},
            {"Key": tag_key, "Value": tag_value},
        ],
    )
    return rds_cluster, rds_instance


def waiter_db_instance_stopped(region_name, db_instance_ids):
    """Wait rds instance to stopped."""
    client = boto3.client("rds", region_name=region_name)
    i = 0
    while (
        client.describe_db_instances(DBInstanceIdentifier=db_instance_ids)[
            "DBInstances"
        ][0]["DBInstanceStatus"]
        != "stopped"
        or i == 50
    ):
        i += i + 1
        time.sleep(15)


def waitter_db_cluster_available(region_name, db_cluster_id):
    """Wait rds cluster to available."""
    client = boto3.client("rds", region_name=region_name)
    i = 0
    while (
        client.describe_db_clusters(DBClusterIdentifier=db_cluster_id)["DBClusters"][0][
            "Status"
        ]
        != "available"
        or i == 50
    ):
        i += i + 1
        time.sleep(15)


def waitter_db_cluster_stopped(region_name, db_cluster_id):
    """Wait rds cluster to stopped."""
    client = boto3.client("rds", region_name=region_name)
    i = 0
    while (
        client.describe_db_clusters(DBClusterIdentifier=db_cluster_id)["DBClusters"][0][
            "Status"
        ]
        != "stopped"
        or i == 50
    ):
        i += i + 1
        time.sleep(15)


def create_cloudwatch_alarm(region_name, aws_tags):
    """Create cloudwatch alarm with tags."""
    client = boto3.client("cloudwatch", region_name=region_name)
    name_prefix = str(randint(0, 1000000000))
    client.put_metric_alarm(
        AlarmName="alarm" + name_prefix,
        MetricName="StatusCheckFailed_Instance",
        Namespace="AWS/EC2",
        Period=60,
        EvaluationPeriods=2,
        Statistic="Minimum",
        Threshold=0.0,
        ComparisonOperator="GreaterThanThreshold",
        ActionsEnabled=True,
        Tags=[aws_tags],
    )
    return "alarm" + name_prefix
