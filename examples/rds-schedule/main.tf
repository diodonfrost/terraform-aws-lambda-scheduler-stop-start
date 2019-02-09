provider "aws" {
  region = "eu-west-3"
}

# Create rds aurora cluster
resource "aws_rds_cluster" "aurora" {
  cluster_identifier  = "aurora-cluster-example"
  availability_zones  = ["eu-west-3a", "eu-west-3b", "eu-west-3c"]
  database_name       = "aurora"
  master_username     = "foo"
  master_password     = "barbut8chars"
  skip_final_snapshot = "true"
  tags                = {
    tostop = "true"
  }
}

resource "aws_rds_cluster_instance" "aurora" {
  count              = 2
  identifier         = "aurora-cluster-example-${count.index}"
  cluster_identifier = "${aws_rds_cluster.aurora.id}"
  instance_class     = "db.t2.small"
}

# Create rds mariadb instance
resource "aws_db_instance" "mariadb" {
  identifier          = "mariadb-instance-example"
  allocated_storage   = 10
  storage_type        = "gp2"
  engine              = "mariadb"
  engine_version      = "10.3"
  instance_class      = "db.t2.small"
  name                = "mariadb"
  username            = "foo"
  password            = "foobarbaz"
  skip_final_snapshot = "true"
  tags                = {
    tostop = "true"
  }
}

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
