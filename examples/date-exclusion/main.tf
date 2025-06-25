resource "random_pet" "suffix" {}

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
  count         = 2
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.test.id

  tags = {
    tostop = "true-${random_pet.suffix.id}"
    Name   = "ec2-scheduled-exclusion-example-${random_pet.suffix.id}-${count.index}"
  }
}

resource "aws_instance" "not_scheduled" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.test.id

  tags = {
    tostop = "false"
    Name   = "ec2-not-scheduled-exclusion-example-${random_pet.suffix.id}"
  }
}


module "ec2_stop_with_exclusions" {
  source                    = "../../"
  name                      = "stop-ec2-exclusions-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 22 ? * MON-FRI *)"
  schedule_action           = "stop"
  ec2_schedule              = true
  rds_schedule              = false
  autoscaling_schedule      = false
  cloudwatch_alarm_schedule = false
  scheduler_excluded_dates = [
    "01-01",                         # New Year's Day
    "12-25",                         # Christmas Day
    "12-24",                         # Christmas Eve
    "07-04",                         # Independence Day (US)
    "11-24",                         # Thanksgiving (example date)
    "05-01",                         # Labor Day
    "12-31",                         # New Year's Eve
    formatdate("MM-DD", timestamp()) # Current date (for tests purposes)
  ]

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}


module "ec2_start_with_exclusions" {
  source                    = "../../"
  name                      = "start-ec2-exclusions-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 7 ? * MON-FRI *)"
  schedule_action           = "start"
  ec2_schedule              = true
  rds_schedule              = false
  autoscaling_schedule      = false
  cloudwatch_alarm_schedule = false

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test_execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name             = module.ec2_stop_with_exclusions.scheduler_lambda_name
  instance_1_to_scheduled_id   = aws_instance.scheduled[0].id
  instance_2_to_scheduled_id   = aws_instance.scheduled[1].id
  instance_not_to_scheduled_id = aws_instance.not_scheduled.id
}
