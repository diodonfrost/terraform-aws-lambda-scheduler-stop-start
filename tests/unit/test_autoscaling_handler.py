import boto3
from moto import mock_aws
import pytest
from package.scheduler.autoscaling_handler import AutoscalingScheduler


@mock_aws
def test_autoscaling_scheduler_initialization():
    """Test that AutoscalingScheduler initializes correctly with and without region."""
    scheduler = AutoscalingScheduler()
    assert scheduler.region_name is None
    assert scheduler.ec2 is not None
    assert scheduler.asg is not None
    assert scheduler.waiter is not None

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    assert scheduler.region_name == "us-east-1"
    assert scheduler.ec2 is not None
    assert scheduler.asg is not None
    assert scheduler.waiter is not None


@mock_aws
def test_stop_autoscaling_group():
    """Test stopping Auto Scaling groups and their instances."""
    ec2 = boto3.client("ec2", region_name="us-east-1")
    asg = boto3.client("autoscaling", region_name="us-east-1")

    asg.create_launch_configuration(
        LaunchConfigurationName="test-launch-config",
        ImageId="ami-123456",
        InstanceType="t2.micro",
    )

    asg_name = "test-asg"
    asg.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName="test-launch-config",
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
        Tags=[
            {"Key": "Environment", "Value": "Development", "PropagateAtLaunch": True}
        ],
    )

    response = ec2.describe_instances()
    instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    aws_tags = [{"Key": "Environment", "Values": ["Development"]}]
    scheduler.stop(aws_tags)

    response = asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    assert response["AutoScalingGroups"][0]["SuspendedProcesses"] != []

    response = ec2.describe_instances(InstanceIds=[instance_id])
    assert response["Reservations"][0]["Instances"][0]["State"]["Name"] == "stopped"


@mock_aws
def test_start_autoscaling_group():
    """Test starting Auto Scaling groups and their instances."""
    ec2 = boto3.client("ec2", region_name="us-east-1")
    asg = boto3.client("autoscaling", region_name="us-east-1")

    asg.create_launch_configuration(
        LaunchConfigurationName="test-launch-config",
        ImageId="ami-123456",
        InstanceType="t2.micro",
    )

    asg_name = "test-asg"
    asg.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName="test-launch-config",
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
        Tags=[
            {"Key": "Environment", "Value": "Development", "PropagateAtLaunch": True}
        ],
    )

    response = ec2.describe_instances()
    instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

    ec2.stop_instances(InstanceIds=[instance_id])
    asg.suspend_processes(AutoScalingGroupName=asg_name)

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    aws_tags = [{"Key": "Environment", "Values": ["Development"]}]
    scheduler.start(aws_tags)

    response = asg.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    assert response["AutoScalingGroups"][0]["SuspendedProcesses"] == []

    response = ec2.describe_instances(InstanceIds=[instance_id])
    assert response["Reservations"][0]["Instances"][0]["State"]["Name"] == "running"


@mock_aws
def test_terminate_instances():
    """Test terminating instances in Auto Scaling groups."""
    ec2 = boto3.client("ec2", region_name="us-east-1")
    asg = boto3.client("autoscaling", region_name="us-east-1")

    asg.create_launch_configuration(
        LaunchConfigurationName="test-launch-config",
        ImageId="ami-123456",
        InstanceType="t2.micro",
    )

    asg_name = "test-asg"
    asg.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName="test-launch-config",
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
        Tags=[
            {"Key": "Environment", "Value": "Development", "PropagateAtLaunch": True}
        ],
    )

    response = ec2.describe_instances()
    instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    aws_tags = [{"Key": "Environment", "Values": ["Development"]}]
    scheduler.stop(aws_tags, terminate_instances=True)

    response = ec2.describe_instances(InstanceIds=[instance_id])
    assert response["Reservations"][0]["Instances"][0]["State"]["Name"] == "terminated"


@mock_aws
def test_list_groups():
    """Test listing Auto Scaling groups by tag."""
    asg = boto3.client("autoscaling", region_name="us-east-1")

    asg.create_launch_configuration(
        LaunchConfigurationName="test-launch-config",
        ImageId="ami-123456",
        InstanceType="t2.micro",
    )

    asg_name = "test-asg"
    asg.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName="test-launch-config",
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
        Tags=[
            {"Key": "Environment", "Value": "Development", "PropagateAtLaunch": True}
        ],
    )

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    groups = scheduler.list_groups("Environment", "Development")

    assert len(groups) == 1
    assert groups[0] == asg_name


@mock_aws
def test_list_instances():
    """Test listing instances in Auto Scaling groups."""
    ec2 = boto3.client("ec2", region_name="us-east-1")
    asg = boto3.client("autoscaling", region_name="us-east-1")

    asg.create_launch_configuration(
        LaunchConfigurationName="test-launch-config",
        ImageId="ami-123456",
        InstanceType="t2.micro",
    )

    asg_name = "test-asg"
    asg.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName="test-launch-config",
        MinSize=1,
        MaxSize=1,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
        Tags=[
            {"Key": "Environment", "Value": "Development", "PropagateAtLaunch": True}
        ],
    )

    response = ec2.describe_instances()
    instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

    scheduler = AutoscalingScheduler(region_name="us-east-1")
    instances = list(scheduler.list_instances([asg_name]))

    assert len(instances) == 1
    assert instances[0] == instance_id


@mock_aws
def test_handle_nonexistent_resources():
    """Test handling of nonexistent Auto Scaling resources."""
    scheduler = AutoscalingScheduler(region_name="us-east-1")
    aws_tags = [{"Key": "Environment", "Values": ["Development"]}]

    scheduler.stop(aws_tags)
    scheduler.start(aws_tags)
