"""Tests for the rds scheduler."""

import boto3

from package.rds_handler import RdsScheduler

from .fixture import (
    launch_rds_instance,
    launch_rds_cluster,
    waiter_db_instance_stopped,
    waitter_db_cluster_available,
    waitter_db_cluster_stopped,
)

import pytest


@pytest.mark.parametrize(
    "aws_region, db_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            {"key": "tostop", "value": "true"},
            {"key": "tostop", "value": "true"},
            "stopped",
        ),
        (
            "eu-west-1",
            {"key": "badtagkey", "value": "badtagvalue"},
            {"key": "tostop", "value": "true"},
            "available",
        ),
    ],
)
def test_stop_db_instance(aws_region, db_tag, scheduler_tag, result_count):
    """Verify stop rds db scheduler class method."""
    client = boto3.client("rds", region_name=aws_region)
    db = launch_rds_instance(aws_region, db_tag["key"], db_tag["value"])
    db_id = db["DBInstance"]["DBInstanceIdentifier"]

    try:
        client.get_waiter("db_instance_available").wait(
            DBInstanceIdentifier=db_id
        )
        rds_scheduler = RdsScheduler(aws_region)
        rds_scheduler.stop(scheduler_tag["key"], scheduler_tag["value"])
        if db_tag["key"] == "tostop" and db_tag["value"] == "true":
            waiter_db_instance_stopped(aws_region, db_id)

        db_state = client.describe_db_instances(DBInstanceIdentifier=db_id)
        assert db_state["DBInstances"][0]["DBInstanceStatus"] == result_count
    finally:
        # Clean aws account
        client.delete_db_instance(
            DBInstanceIdentifier=db_id, SkipFinalSnapshot=True
        )


@pytest.mark.parametrize(
    "aws_region, db_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            {"key": "tostart", "value": "true"},
            {"key": "tostart", "value": "true"},
            "available",
        ),
        (
            "eu-west-1",
            {"key": "badtagkey", "value": "badtagvalue"},
            {"key": "tostart", "value": "true"},
            "stopped",
        ),
    ],
)
def test_start_db_instance(aws_region, db_tag, scheduler_tag, result_count):
    """Verify start rds db scheduler class method."""
    client = boto3.client("rds", region_name=aws_region)
    db = launch_rds_instance(aws_region, db_tag["key"], db_tag["value"])
    db_id = db["DBInstance"]["DBInstanceIdentifier"]

    try:
        client.get_waiter("db_instance_available").wait(
            DBInstanceIdentifier=db_id
        )
        client.stop_db_instance(DBInstanceIdentifier=db_id)
        waiter_db_instance_stopped(aws_region, db_id)
        rds_scheduler = RdsScheduler(aws_region)
        rds_scheduler.start(scheduler_tag["key"], scheduler_tag["value"])
        if db_tag["key"] == "tostart" and db_tag["value"] == "true":
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )

        db_state = client.describe_db_instances(DBInstanceIdentifier=db_id)
        assert db_state["DBInstances"][0]["DBInstanceStatus"] == result_count
    finally:
        # Clean aws account
        client.delete_db_instance(
            DBInstanceIdentifier=db_id, SkipFinalSnapshot=True
        )


@pytest.mark.parametrize(
    "aws_region, db_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            {"key": "tostop-cluster", "value": "true"},
            {"key": "tostop-cluster", "value": "true"},
            "stopped",
        ),
        (
            "eu-west-1",
            {"key": "badtagkey", "value": "badtagvalue"},
            {"key": "tostop-cluster", "value": "true"},
            "available",
        ),
    ],
)
def test_stop_db_cluster(aws_region, db_tag, scheduler_tag, result_count):
    """Verify stop rds db scheduler class method."""
    client = boto3.client("rds", region_name=aws_region)
    cluster, db = launch_rds_cluster(
        aws_region, db_tag["key"], db_tag["value"]
    )
    cluster_id = cluster["DBCluster"]["DBClusterIdentifier"]
    db_id = db["DBInstance"]["DBInstanceIdentifier"]

    try:
        client.get_waiter("db_instance_available").wait(
            DBInstanceIdentifier=db_id
        )
        waitter_db_cluster_available(aws_region, cluster_id)
        rds_scheduler = RdsScheduler(aws_region)
        rds_scheduler.stop(scheduler_tag["key"], scheduler_tag["value"])
        if db_tag["key"] == "tostop-cluster" and db_tag["value"] == "true":
            waitter_db_cluster_stopped(aws_region, cluster_id)
            waiter_db_instance_stopped(aws_region, db_id)

        cluster_state = client.describe_db_clusters(
            DBClusterIdentifier=cluster_id
        )["DBClusters"][0]["Status"]
        assert cluster_state == result_count
    finally:
        # Clean aws account
        if cluster_state == "stopped":
            client.start_db_cluster(DBClusterIdentifier=cluster_id)
            waitter_db_cluster_available(aws_region, cluster_id)
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )
        elif cluster_state == "stopping":
            waitter_db_cluster_stopped(aws_region, cluster_id)
            waiter_db_instance_stopped(aws_region, db_id)
            client.start_db_cluster(DBClusterIdentifier=cluster_id)
            waitter_db_cluster_available(aws_region, cluster_id)
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )
        client.delete_db_instance(
            DBInstanceIdentifier=db_id, SkipFinalSnapshot=True
        )
        client.delete_db_cluster(
            DBClusterIdentifier=cluster_id, SkipFinalSnapshot=True
        )


@pytest.mark.parametrize(
    "aws_region, db_tag, scheduler_tag, result_count",
    [
        (
            "eu-west-1",
            {"key": "tostart-cluster", "value": "true"},
            {"key": "tostart-cluster", "value": "true"},
            "available",
        ),
        (
            "eu-west-1",
            {"key": "badtagkey", "value": "badtagvalue"},
            {"key": "tostart-cluster", "value": "true"},
            "stopped",
        ),
    ],
)
def test_start_db_cluster(aws_region, db_tag, scheduler_tag, result_count):
    """Verify syaty rds db scheduler class method."""
    client = boto3.client("rds", region_name=aws_region)
    cluster, db = launch_rds_cluster(
        aws_region, db_tag["key"], db_tag["value"]
    )
    cluster_id = cluster["DBCluster"]["DBClusterIdentifier"]
    db_id = db["DBInstance"]["DBInstanceIdentifier"]

    try:
        client.get_waiter("db_instance_available").wait(
            DBInstanceIdentifier=db_id
        )
        waitter_db_cluster_available(aws_region, cluster_id)
        client.stop_db_cluster(DBClusterIdentifier=cluster_id)
        waitter_db_cluster_stopped(aws_region, cluster_id)
        waiter_db_instance_stopped(aws_region, db_id)

        rds_scheduler = RdsScheduler(aws_region)
        rds_scheduler.start(scheduler_tag["key"], scheduler_tag["value"])
        if db_tag["key"] == "tostart-cluster" and db_tag["value"] == "true":
            waitter_db_cluster_available(aws_region, cluster_id)
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )

        cluster_state = client.describe_db_clusters(
            DBClusterIdentifier=cluster_id
        )["DBClusters"][0]["Status"]
        assert cluster_state == result_count
    finally:
        # Clean aws account
        if cluster_state == "stopped":
            client.start_db_cluster(DBClusterIdentifier=cluster_id)
            waitter_db_cluster_available(aws_region, cluster_id)
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )
        elif cluster_state == "stopping":
            waitter_db_cluster_stopped(aws_region, cluster_id)
            waiter_db_instance_stopped(aws_region, db_id)
            client.start_db_cluster(DBClusterIdentifier=cluster_id)
            waitter_db_cluster_available(aws_region, cluster_id)
            client.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=db_id
            )
        client.delete_db_instance(
            DBInstanceIdentifier=db_id, SkipFinalSnapshot=True
        )
        client.delete_db_cluster(
            DBClusterIdentifier=cluster_id, SkipFinalSnapshot=True
        )
