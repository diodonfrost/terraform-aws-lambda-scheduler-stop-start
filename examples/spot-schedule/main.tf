# Terraform spot instance with lambda scheduler

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

# Create vpc use by asg
resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
}

# Create subnet use bt asg
resource "aws_subnet" "this" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.1.0/24"
}

# Run spot instances that will be scheduled
resource "aws_launch_template" "scheduled" {
  name_prefix   = "spot-scheduled"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "scheduled" {
  desired_capacity    = 3
  max_size            = 3
  min_size            = 3
  vpc_zone_identifier = [aws_subnet.this.id]

  mixed_instances_policy {
     instances_distribution {
       on_demand_percentage_above_base_capacity = "0"
     }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.scheduled.id
      }

      override {
        instance_type = "t2.micro"
      }

      override {
        instance_type = "t2.nano"
      }
    }
  }

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

# Run spot instances that will be not scheduled
resource "aws_launch_template" "not_scheduled" {
 name_prefix   = "spot-not_scheduled"
 image_id      = data.aws_ami.ubuntu.id
 instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "not_scheduled" {
 desired_capacity    = 2
 max_size            = 2
 min_size            = 2
 vpc_zone_identifier = [aws_subnet.this.id]

 mixed_instances_policy {
    instances_distribution {
      on_demand_percentage_above_base_capacity = "0"
    }

   launch_template {
     launch_template_specification {
       launch_template_id = aws_launch_template.scheduled.id
     }

     override {
       instance_type = "t2.micro"
     }

     override {
       instance_type = "t2.nano"
     }
   }
 }

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


### Terraform module ##

module "spot-terminate-friday" {
  source                         = "../../"
  name                           = "terminate-spot"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  spot_schedule                  = "terminate"
  ec2_schedule                   = "false"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"

  resources_tag = {
    key   = "tostop"
    value = "true"
  }
}
