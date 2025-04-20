# Terraform rds with lambda scheduler
resource "random_pet" "suffix" {}

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
  name       = "aurora-subnet-${random_pet.suffix.id}"
  subnet_ids = [aws_subnet.primary.id, aws_subnet.secondary.id]
}

resource "aws_rds_cluster" "aurora_scheduled" {
  cluster_identifier   = "test-to-stop-aurora-cluster-${random_pet.suffix.id}"
  engine               = "aurora-mysql"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  database_name        = "aurorawithtag"
  master_username      = "foo"
  master_password      = "barbut8chars"
  skip_final_snapshot  = "true"

  tags = {
    tostop = "true"
  }
}

resource "aws_rds_cluster_instance" "aurora_scheduled" {
  identifier           = "test-to-stop-aurora-instance-${random_pet.suffix.id}"
  engine               = aws_rds_cluster.aurora_scheduled.engine
  engine_version       = aws_rds_cluster.aurora_scheduled.engine_version
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  cluster_identifier   = aws_rds_cluster.aurora_scheduled.id
  instance_class       = "db.t3.medium"

  tags = {
    tostop = "true"
  }
}

resource "aws_db_instance" "mariadb_scheduled" {
  identifier           = "test-to-stop-mariadb-instance-${random_pet.suffix.id}"
  db_name              = "mariadbwithtag"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  allocated_storage    = 10
  storage_type         = "gp2"
  engine               = "mariadb"
  engine_version       = "11.4.4"
  instance_class       = "db.t4g.micro"
  username             = "foo"
  password             = "foobarbaz"
  skip_final_snapshot  = "true"

  tags = {
    tostop = "true"
  }
}

resource "aws_db_instance" "mysql_not_scheduled" {
  identifier           = "test-not-to-stop-mysql-instance-${random_pet.suffix.id}"
  db_name              = "mysqlwithouttag"
  db_subnet_group_name = aws_db_subnet_group.aurora.id
  allocated_storage    = 10
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t4g.micro"
  username             = "foo"
  password             = "foobarbaz"
  skip_final_snapshot  = "true"

  tags = {
    tostop = "false"
  }
}


### Terraform modules ###

module "rds-stop-friday" {
  source                         = "../../"
  name                           = "stop-rds-${random_pet.suffix.id}"
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
  name                           = "start-rds-${random_pet.suffix.id}"
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

module "test-execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                         = module.rds-stop-friday.scheduler_lambda_name
  rds_aurora_cluster_to_scheduled_name     = aws_rds_cluster.aurora_scheduled.cluster_identifier
  rds_mariadb_instance_to_scheduled_name   = aws_db_instance.mariadb_scheduled.identifier
  rds_mysql_instance_to_not_scheduled_name = aws_db_instance.mysql_not_scheduled.identifier

  depends_on = [
    aws_rds_cluster_instance.aurora_scheduled
  ]
}
