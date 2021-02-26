# Terraform autoscaling group with lambda scheduler

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "this" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.1.0/24"
}

resource "aws_launch_configuration" "this" {
  name          = "web_config"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

# Create autoscaling group with tag
resource "aws_autoscaling_group" "scheduled" {
  count                     = 3
  name                      = "bar-with-tag-${count.index}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  launch_configuration      = aws_launch_configuration.this.name
  vpc_zone_identifier       = [aws_subnet.this.id]

  tags = [
    {
      key                 = "tostop"
      value               = "true"
      propagate_at_launch = true
    },
    {
      key                 = "terratest_tag"
      value               = var.random_tag
      propagate_at_launch = true
    },
  ]
}

# Create autoscaling group without tag
resource "aws_autoscaling_group" "not_scheduled" {
  count                     = 2
  name                      = "foo-without-tag-${count.index}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  launch_configuration      = aws_launch_configuration.this.name
  vpc_zone_identifier       = [aws_subnet.this.id]

  tags = [
    {
      key                 = "tostop"
      value               = "false"
      propagate_at_launch = true
    },
    {
      key                 = "terratest_tag"
      value               = var.random_tag
      propagate_at_launch = true
    },
  ]
}


### Terraform modules ###

module "autoscaling-stop-friday" {
  source                         = "../../"
  name                           = "stop-autoscaling"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "false"
  rds_schedule                   = "false"
  autoscaling_schedule           = "true"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "autoscaling-start-monday" {
  source                         = "../../"
  name                           = "start-autoscaling"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "false"
  rds_schedule                   = "false"
  autoscaling_schedule           = "true"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
