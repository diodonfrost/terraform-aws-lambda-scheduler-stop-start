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
  name                      = "test-to-stop-${random_pet.suffix.id}-${count.index}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  vpc_zone_identifier       = [aws_subnet.this.id]
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 25
      spot_allocation_strategy                 = "capacity-optimized"
    }
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.this.id
      }
    }
  }

  tag {
    key                 = "tostop"
    value               = "true-${random_pet.suffix.id}"
    propagate_at_launch = true
  }
}

# Create autoscaling group without tag
resource "aws_autoscaling_group" "not_scheduled" {
  count                     = 2
  name                      = "test-not-to-stop-${random_pet.suffix.id}-${count.index}"
  max_size                  = 5
  min_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"
  desired_capacity          = 1
  force_delete              = true
  vpc_zone_identifier       = [aws_subnet.this.id]
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 0
      on_demand_percentage_above_base_capacity = 25
      spot_allocation_strategy                 = "capacity-optimized"
    }
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.this.id
      }
    }
  }

  tag {
    key                 = "tostop"
    value               = "false"
    propagate_at_launch = true
  }
}


### Terraform modules ###

module "autoscaling-stop-friday" {
  source                          = "../../"
  name                            = "stop-autoscaling-${random_pet.suffix.id}"
  schedule_expression             = "cron(0 23 ? * FRI *)"
  schedule_action                 = "stop"
  ec2_schedule                    = "false"
  rds_schedule                    = "false"
  autoscaling_schedule            = "true"
  autoscaling_terminate_instances = "true"
  cloudwatch_alarm_schedule       = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "autoscaling-start-monday" {
  source                    = "../../"
  name                      = "start-autoscaling-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 07 ? * MON *)"
  schedule_action           = "start"
  ec2_schedule              = "false"
  rds_schedule              = "false"
  autoscaling_schedule      = "true"
  cloudwatch_alarm_schedule = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}
