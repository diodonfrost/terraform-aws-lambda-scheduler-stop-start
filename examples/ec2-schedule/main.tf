provider "aws" {
  region = "eu-west-3"
}

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

resource "aws_instance" "web" {
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.micro"

  tags = {
    tostop = "true"
  }
}

module "lambda_scheduler_stop_start" {
  cloudwatch_schedule_expression = "cron(0 22 ? * MON-FRI *)"
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  schedule_action                = "stop"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    tostop = "true"
  }
}
