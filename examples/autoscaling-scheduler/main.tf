# Terraform autoscaling group with lambda scheduler
resource "random_pet" "suffix" {}

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

resource "aws_launch_template" "this" {
  name_prefix   = "web_config"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

# Create autoscaling group with tag
resource "aws_autoscaling_group" "scheduled" {
  count                     = 3
  name                      = "test-to-stop-${count.index}-${random_pet.suffix.id}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  vpc_zone_identifier       = [aws_subnet.this.id]

  launch_template {
    id      = aws_launch_template.this.id
    version = "$Latest"
  }

  tag {
    key                 = "tostop"
    value               = "true"
    propagate_at_launch = true
  }
}

# Create autoscaling group without tag
resource "aws_autoscaling_group" "not_scheduled" {
  count                     = 2
  name                      = "test-not-to-stop-${count.index}-${random_pet.suffix.id}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  vpc_zone_identifier       = [aws_subnet.this.id]

  launch_template {
    id      = aws_launch_template.this.id
    version = "$Latest"
  }

  tag {
    key                 = "tostop"
    value               = "false"
    propagate_at_launch = true
  }
}


### Terraform modules ###

module "autoscaling-stop-friday" {
  source                         = "../../"
  name                           = "stop-autoscaling-${random_pet.suffix.id}"
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
  name                           = "start-autoscaling-${random_pet.suffix.id}"
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

module "test-execution" {
  source = "./test-execution"

  lambda_stop_name       = module.autoscaling-stop-friday.scheduler_lambda_name
  asg_scheduled_name     = aws_autoscaling_group.scheduled[0].name
  asg_not_scheduled_name = aws_autoscaling_group.not_scheduled[0].name
}
