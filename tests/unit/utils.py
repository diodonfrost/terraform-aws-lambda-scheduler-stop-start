"""Module use by ec2 scheduler unit tests."""

import boto3


def launch_ec2_instances(count, region_name, tag_key, tag_value):
    """Create ec2 instances."""
    client = boto3.client("ec2", region_name=region_name)
    instance = client.run_instances(
        ImageId="ami-02df9ea15c1778c9c",
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
    return instance


def launch_ec2_spot(count, region_name, tag_key, tag_value):
    """Create ec2 spot instances."""
    client = boto3.client("ec2", region_name=region_name)
    spot = client.run_instances(
        ImageId="ami-02df9ea15c1778c9c",
        MaxCount=count,
        MinCount=count,
        InstanceMarketOptions={
            "MarketType": "spot",
            "SpotOptions": {
                "SpotInstanceType": "one-time",
                "InstanceInterruptionBehavior": "terminate"
            }
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
    return spot


def launch_asg(region_name, tag_key, tag_value):
    """Create autoscaling group with aws tags."""
    client = boto3.client("autoscaling", region_name=region_name)
    client.create_launch_configuration(
        LaunchConfigurationName="lc-test",
        ImageId="ami-02df9ea15c1778c9c",
        InstanceType="t2.micro",
    )
    asg = client.create_auto_scaling_group(
        AutoScalingGroupName="asg-test",
        MaxSize=5,
        DesiredCapacity=3,
        MinSize=1,
        LaunchConfigurationName="lc-test",
        AvailabilityZones=[region_name + "a", region_name + "b"],
        Tags=[
            {
                "ResourceId": "asg-test",
                "ResourceType": "auto-scaling-group",
                "Key": tag_key,
                "Value": tag_value,
                "PropagateAtLaunch": True,
            }
        ],
    )
    return client.describe_auto_scaling_groups(AutoScalingGroupNames=["asg-test"])


def launch_rds_instance(region_name, tag_key, tag_value):
    """Create rds instances with aws tags."""
    client = boto3.client("rds", region_name=region_name)
    rds_instance = client.create_db_instance(
        DBInstanceIdentifier="db-instance",
        AllocatedStorage=10,
        DBName="db-instance",
        DBInstanceClass="db.m4.large",
        Engine="mariadb",
        MasterUsername="root",
        MasterUserPassword="IamNotHere",
        Tags=[
            {"Key": "Name", "Value": "db-instance"},
            {"Key": tag_key, "Value": tag_value},
        ],
    )
    return rds_instance

def put_create_alarm(region_name, name, dimensions):
    """Create alarm and associates it."""
    client = boto3.client("cloudwatch", region_name=region_name)
    client.put_metric_alarm(
        AlarmName=name,
        MetricName="StatusCheckFailed_Instance",
        Namespace="AWS/EC2",
        Period=60,
        EvaluationPeriods=2,
        Statistic="Minimum",
        Threshold=0.0,
        ComparisonOperator="GreaterThanThreshold",
        ActionsEnabled=True,
        Dimensions=dimensions,
    )
