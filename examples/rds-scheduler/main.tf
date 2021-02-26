# Terraform rds with lambda scheduler

# Get aws availability zones
data "aws_availability_zones" "available" {}

resource "aws_vpc" "this" {
  cidr_block = "10.103.0.0/16"
}

resource "aws_subnet" "primary" {
  availability_zone = data.aws_availability_zones.available.names[0]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.98.0/24"
}

resource "aws_subnet" "secondary" {
  availability_zone = data.aws_availability_zones.available.names[1]
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.103.99.0/24"
}

resource "aws_db_subnet_group" "aurora" {
  name       = "aurora-subnet"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

# Create rds aurora cluster
resource "aws_rds_cluster" "aurora_scheduled" {
  cluster_identifier   = "aurora-cluster-with-tag"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  database_name        = "aurorawithtag"
  master_username      = "foo"
  master_password      = "barbut8chars"
  skip_final_snapshot  = "true"

  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

resource "aws_rds_cluster_instance" "aurora_scheduled" {
  identifier           = "aurora-cluster-with-tag-writer"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  cluster_identifier   = aws_rds_cluster.aurora_scheduled.id
  instance_class       = "db.t2.small"

  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

# Create rds mariadb instance with tag
resource "aws_db_instance" "mariadb_scheduled" {
  identifier           = "mariadb-instance-with-tag"
  name                 = "mariadbwithtag"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  allocated_storage    = 10
  storage_type         = "gp2"
  engine               = "mariadb"
  engine_version       = "10.3"
  instance_class       = "db.t2.micro"
  username             = "foo"
  password             = "foobarbaz"
  skip_final_snapshot  = "true"

  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

# Create rds mysql instance with tag
resource "aws_db_instance" "mysql_not_scheduled" {
  identifier           = "mysql-instance-without-tag"
  name                 = "mysqlwithouttag"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  allocated_storage    = 10
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.6"
  instance_class       = "db.t2.micro"
  username             = "foo"
  password             = "foobarbaz"
  skip_final_snapshot  = "true"

  tags = {
    tostop        = "false"
    terratest_tag = var.random_tag
  }
}


### Terraform modules ###

module "rds-stop-friday" {
  source                         = "../../"
  name                           = "stop-rds"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "false"
  rds_schedule                   = "true"
  autoscaling_schedule           = "false"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "rds-start-monday" {
  source                         = "../../"
  name                           = "start-rds"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "false"
  rds_schedule                   = "true"
  autoscaling_schedule           = "false"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
