# Terraform ec2 instance with lambda scheduler
resource "random_pet" "suffix" {}

data "aws_region" "current" {}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "scheduled" {
  count         = "3"
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  tags = {
    tostop = "true-${random_pet.suffix.id}"
    Name   = "ec2-to-scheduled-${random_pet.suffix.id}-${count.index}"
  }
}

resource "aws_instance" "not_scheduled" {
  count         = "2"
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  tags = {
    tostop = "false"
    Name   = "ec2-not-to-scheduled-${random_pet.suffix.id}-${count.index}"
  }
}


### Terraform modules ###

module "ec2-stop-friday" {
  source                    = "../../"
  name                      = "stop-ec2-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 23 ? * FRI *)"
  schedule_action           = "stop"
  ec2_schedule              = "true"
  rds_schedule              = "false"
  autoscaling_schedule      = "false"
  cloudwatch_alarm_schedule = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "ec2-start-monday" {
  source                    = "../../"
  name                      = "start-ec2-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 07 ? * MON *)"
  schedule_action           = "start"
  ec2_schedule              = "true"
  rds_schedule              = "false"
  autoscaling_schedule      = "false"
  cloudwatch_alarm_schedule = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test-execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name               = module.ec2-stop-friday.scheduler_lambda_name
  instance_1_to_scheduled_id     = aws_instance.scheduled[0].id
  instance_2_to_scheduled_id     = aws_instance.scheduled[1].id
  instance_3_to_scheduled_id     = aws_instance.scheduled[2].id
  instance_1_not_to_scheduled_id = aws_instance.not_scheduled[0].id
  instance_2_not_to_scheduled_id = aws_instance.not_scheduled[1].id
}
