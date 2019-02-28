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

resource "aws_instance" "instance_with_tag" {
  count         = "3"
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.micro"
  tags          = {
    tostop = "true"
  }
}

resource "aws_instance" "instance_without_tag" {
  count         = "2"
  ami           = "${data.aws_ami.ubuntu.id}"
  instance_type = "t2.micro"
}


### Terraform modules ###

module "ec2-stop-friday" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "stop-ec2"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}

module "ec2-start-monday" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "start-ec2"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
