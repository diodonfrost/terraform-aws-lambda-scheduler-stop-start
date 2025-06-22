import boto3
import pytest
from moto import mock_aws

from package.scheduler.rds_handler import RdsScheduler


@pytest.mark.parametrize(
    "aws_region",
    [
        "us-east-1",
        "us-west-2",
        "eu-west-1",
    ],
)
@mock_aws
def test_rds_scheduler_initialization(aws_region):
    """Test that RdsScheduler initializes correctly with and without region."""
    scheduler = RdsScheduler(region_name=aws_region)
    assert scheduler.rds is not None
    assert scheduler.tag_api is not None

    scheduler = RdsScheduler(region_name=aws_region)
    assert scheduler.rds is not None
    assert scheduler.tag_api is not None


@pytest.mark.parametrize(
    "aws_region, aws_tags, result_count",
    [
        (
            "us-east-1",
            [{"Key": "tostop", "Values": ["true"]}],
            "stopped",
        ),
        (
            "us-west-2",
            [{"Key": "tostop", "Values": ["true"]}],
            "stopped",
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            "available",
        ),
    ],
)
@mock_aws
def test_stop_rds_instance(aws_region, aws_tags, result_count):
    """Test stopping RDS instances."""
    rds = boto3.client("rds", region_name=aws_region)

    instance_id = f"test-db-instance-{aws_region}"
    rds.create_db_instance(
        DBInstanceIdentifier=instance_id,
        DBInstanceClass="db.t2.micro",
        Engine="mysql",
        MasterUsername="test",
        MasterUserPassword="test1234",
        AllocatedStorage=20,
    )

    rds.add_tags_to_resource(
        ResourceName=f"arn:aws:rds:{aws_region}:123456789012:db:{instance_id}",
        Tags=[{"Key": "tostop", "Value": "true"}],
    )

    scheduler = RdsScheduler(region_name=aws_region)
    scheduler.stop(aws_tags)

    response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
    assert response["DBInstances"][0]["DBInstanceStatus"] == result_count


@pytest.mark.parametrize(
    "aws_region, aws_tags, result_count",
    [
        (
            "us-east-1",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "us-west-2",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            "stopped",
        ),
    ],
)
@mock_aws
def test_start_rds_instance(aws_region, aws_tags, result_count):
    """Test starting RDS instances."""
    rds = boto3.client("rds", region_name=aws_region)

    instance_id = f"test-db-instance-{aws_region}"
    rds.create_db_instance(
        DBInstanceIdentifier=instance_id,
        DBInstanceClass="db.t2.micro",
        Engine="mysql",
        MasterUsername="test",
        MasterUserPassword="test1234",
        AllocatedStorage=20,
    )

    rds.add_tags_to_resource(
        ResourceName=f"arn:aws:rds:{aws_region}:123456789012:db:{instance_id}",
        Tags=[{"Key": "tostop", "Value": "true"}],
    )

    rds.stop_db_instance(DBInstanceIdentifier=instance_id)

    scheduler = RdsScheduler(region_name=aws_region)
    scheduler.start(aws_tags)

    response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
    assert response["DBInstances"][0]["DBInstanceStatus"] == result_count


@pytest.mark.parametrize(
    "aws_region, aws_tags, result_count",
    [
        (
            "us-east-1",
            [{"Key": "tostop", "Values": ["true"]}],
            "stopped",
        ),
        (
            "us-west-2",
            [{"Key": "tostop", "Values": ["true"]}],
            "stopped",
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            "available",
        ),
    ],
)
@mock_aws
def test_stop_rds_cluster(aws_region, aws_tags, result_count):
    """Test stopping RDS Aurora clusters."""
    rds = boto3.client("rds", region_name=aws_region)

    cluster_id = f"test-cluster-{aws_region}"
    rds.create_db_cluster(
        DBClusterIdentifier=cluster_id,
        Engine="aurora-mysql",
        MasterUsername="test",
        MasterUserPassword="test1234",
    )

    rds.add_tags_to_resource(
        ResourceName=f"arn:aws:rds:{aws_region}:123456789012:cluster:{cluster_id}",
        Tags=[{"Key": "tostop", "Value": "true"}],
    )

    scheduler = RdsScheduler(region_name=aws_region)
    scheduler.stop(aws_tags)

    response = rds.describe_db_clusters(DBClusterIdentifier=cluster_id)
    assert response["DBClusters"][0]["Status"] == result_count


@pytest.mark.parametrize(
    "aws_region, aws_tags, result_count",
    [
        (
            "us-east-1",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "us-west-2",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            "stopped",
        ),
    ],
)
@mock_aws
def test_start_rds_cluster(aws_region, aws_tags, result_count):
    """Test starting RDS Aurora clusters."""
    rds = boto3.client("rds", region_name=aws_region)

    cluster_id = f"test-cluster-{aws_region}"
    rds.create_db_cluster(
        DBClusterIdentifier=cluster_id,
        Engine="aurora-mysql",
        MasterUsername="test",
        MasterUserPassword="test1234",
    )

    rds.add_tags_to_resource(
        ResourceName=f"arn:aws:rds:{aws_region}:123456789012:cluster:{cluster_id}",
        Tags=[{"Key": "tostop", "Value": "true"}],
    )

    rds.stop_db_cluster(DBClusterIdentifier=cluster_id)

    scheduler = RdsScheduler(region_name=aws_region)
    scheduler.start(aws_tags)

    response = rds.describe_db_clusters(DBClusterIdentifier=cluster_id)
    assert response["DBClusters"][0]["Status"] == result_count


@pytest.mark.parametrize(
    "aws_region, aws_tags, result_count",
    [
        (
            "us-east-1",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "us-west-2",
            [{"Key": "tostop", "Values": ["true"]}],
            "available",
        ),
        (
            "eu-west-1",
            [{"Key": "badtagkey", "Values": ["badtagvalue"]}],
            "stopped",
        ),
    ],
)
@mock_aws
def test_handle_nonexistent_resources(aws_region, aws_tags, result_count):
    """Test handling of nonexistent RDS resources."""
    scheduler = RdsScheduler(region_name=aws_region)
    scheduler.stop(aws_tags)
    scheduler.start(aws_tags)
