provider "aws" {
  region = "eu-west-3"
}

# Create rds aurora cluster
resource "aws_rds_cluster" "aurora_with_tag" {
  cluster_identifier  = "aurora-cluster-with-tag"
  availability_zones  = ["eu-west-3a", "eu-west-3b", "eu-west-3c"]
  database_name       = "aurorawithtag"
  master_username     = "foo"
  master_password     = "barbut8chars"
  skip_final_snapshot = "true"
  tags                = {
    tostop = "true"
  }
}

resource "aws_rds_cluster_instance" "aurora_with_tag" {
  identifier         = "aurora-cluster-with-tag"
  cluster_identifier = "${aws_rds_cluster.aurora_with_tag.id}"
  instance_class     = "db.t2.small"
}

# Create rds mariadb instance with tag
resource "aws_db_instance" "mariadb_with_tag" {
  identifier          = "mariadb-instance-with-tag"
  name                = "mariadbwithtag"
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "mariadb"
  engine_version      = "10.3"
  instance_class      = "db.t2.micro"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = "true"
  tags                = {
    tostop = "true"
  }
}

# Create rds mysql instance with tag
resource "aws_db_instance" "mysql_without_tag" {
  identifier          = "mysql-instance-without-tag"
  name                = "mysqlwithouttag"
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "mysql"
  engine_version      = "5.6"
  instance_class      = "db.t2.micro"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = "true"
}


### Terraform modules ###

module "rds-stop-friday" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "stop-rds"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "false"
  rds_schedule                   = "true"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}

module "rds-start-monday" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "start-rds"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "false"
  rds_schedule                   = "true"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
