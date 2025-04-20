# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

resource "aws_vpc" "redshift_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "redshift-vpc-${random_pet.suffix.id}"
  }
}

resource "aws_internet_gateway" "redshift_igw" {
  vpc_id = aws_vpc.redshift_vpc.id
  tags = {
    Name = "redshift-igw-${random_pet.suffix.id}"
  }
}

resource "aws_route_table" "redshift_route_table" {
  vpc_id = aws_vpc.redshift_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.redshift_igw.id
  }

  tags = {
    Name = "redshift-rt-${random_pet.suffix.id}"
  }
}

resource "aws_route_table_association" "redshift_rt_assoc_1" {
  subnet_id      = aws_subnet.redshift_subnet_1.id
  route_table_id = aws_route_table.redshift_route_table.id
}

resource "aws_route_table_association" "redshift_rt_assoc_2" {
  subnet_id      = aws_subnet.redshift_subnet_2.id
  route_table_id = aws_route_table.redshift_route_table.id
}

resource "aws_subnet" "redshift_subnet_1" {
  vpc_id                  = aws_vpc.redshift_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "redshift_subnet_2" {
  vpc_id                  = aws_vpc.redshift_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-west-1b"
  map_public_ip_on_launch = true
}

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "redshift-subnet-group-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.redshift_subnet_1.id, aws_subnet.redshift_subnet_2.id]
}

resource "aws_security_group" "redshift_sg" {
  name        = "redshift-sg-${random_pet.suffix.id}"
  description = "Security group for Redshift clusters"
  vpc_id      = aws_vpc.redshift_vpc.id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow Redshift access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_redshift_cluster" "scheduled" {
  cluster_identifier        = "test-to-stop-${random_pet.suffix.id}"
  database_name             = "mydb"
  master_username           = "exampleuser"
  master_password           = "Mustbe8characters"
  node_type                 = "dc2.large"
  cluster_type              = "single-node"
  publicly_accessible       = false
  skip_final_snapshot       = true
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name
  vpc_security_group_ids    = [aws_security_group.redshift_sg.id]

  tags = {
    tostop = "true"
  }
}

resource "aws_redshift_cluster_snapshot" "scheduled" {
  cluster_identifier  = aws_redshift_cluster.scheduled.id
  snapshot_identifier = "test-to-stop-${random_pet.suffix.id}"
}

resource "aws_redshift_cluster" "not_scheduled" {
  cluster_identifier        = "test-not-to-stop-${random_pet.suffix.id}"
  database_name             = "mydb"
  master_username           = "exampleuser"
  master_password           = "Mustbe8characters"
  node_type                 = "dc2.large"
  cluster_type              = "single-node"
  publicly_accessible       = false
  skip_final_snapshot       = true
  cluster_subnet_group_name = aws_redshift_subnet_group.redshift_subnet_group.name
  vpc_security_group_ids    = [aws_security_group.redshift_sg.id]

  tags = {
    tostop = "false"
  }
}

resource "aws_redshift_cluster_snapshot" "not_scheduled" {
  cluster_identifier  = aws_redshift_cluster.not_scheduled.id
  snapshot_identifier = "test-not-to-stop-${random_pet.suffix.id}"
}


module "redshift-stop-friday" {
  source                         = "../.."
  name                           = "stop-redshift-${random_pet.suffix.id}"
  kms_key_arn                    = aws_kms_key.scheduler.arn
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  redshift_schedule              = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "redshift-start-monday" {
  source                         = "../.."
  name                           = "start-redshift-${random_pet.suffix.id}"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  redshift_schedule              = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "test-execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                    = module.redshift-stop-friday.scheduler_lambda_name
  redshift_cluster_to_scheduled_name  = aws_redshift_cluster.scheduled.cluster_identifier
  redshift_cluster_not_scheduled_name = aws_redshift_cluster.not_scheduled.cluster_identifier
}
