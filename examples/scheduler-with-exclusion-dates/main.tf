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

resource "aws_vpc" "test" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_internet_gateway" "test" {
  vpc_id = aws_vpc.test.id

  tags = {
    Name = "scheduler-exclusion-igw-${random_pet.suffix.id}"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.test.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = data.aws_availability_zones.available.names[0]
  map_public_ip_on_launch = true
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.test.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.test.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_instance" "scheduled" {
  count         = 2
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id

  tags = {
    tostop = "true-${random_pet.suffix.id}"
    Name   = "ec2-scheduled-exclusion-example-${random_pet.suffix.id}-${count.index}"
  }
}

resource "aws_instance" "not_scheduled" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id

  tags = {
    tostop = "false"
    Name   = "ec2-not-scheduled-exclusion-example-${random_pet.suffix.id}"
  }
}


module "ec2-stop-with-exclusions" {
  source                    = "../../"
  name                      = "stop-ec2-exclusions-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 22 ? * MON-FRI *)"
  schedule_action           = "stop"
  ec2_schedule              = true
  rds_schedule              = false
  autoscaling_schedule      = false
  cloudwatch_alarm_schedule = false

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}


module "ec2-start-with-exclusions" {
  source                    = "../../"
  name                      = "start-ec2-exclusions-${random_pet.suffix.id}"
  schedule_expression       = "cron(0 7 ? * MON-FRI *)"
  schedule_action           = "start"
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
