# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

resource "aws_redshift_cluster" "scheduled" {
  cluster_identifier        = "test-to-stop-${random_pet.suffix.id}"
  database_name             = "mydb"
  master_username           = "exampleuser"
  master_password           = "Mustbe8characters"
  node_type                 = "ra3.large"
  cluster_type              = "single-node"
  publicly_accessible       = false
  skip_final_snapshot       = true
  cluster_subnet_group_name = aws_redshift_subnet_group.redshif.name

  tags = {
    tostop = "true-${random_pet.suffix.id}"
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
  node_type                 = "ra3.large"
  cluster_type              = "single-node"
  publicly_accessible       = false
  skip_final_snapshot       = true
  cluster_subnet_group_name = aws_redshift_subnet_group.redshif.name

  tags = {
    tostop = "false"
  }
}

resource "aws_redshift_cluster_snapshot" "not_scheduled" {
  cluster_identifier  = aws_redshift_cluster.not_scheduled.id
  snapshot_identifier = "test-not-to-stop-${random_pet.suffix.id}"
}


module "redshift-stop-friday" {
  source              = "../.."
  name                = "stop-redshift-${random_pet.suffix.id}"
  kms_key_arn         = aws_kms_key.scheduler.arn
  schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action     = "stop"
  redshift_schedule   = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "redshift-start-monday" {
  source              = "../.."
  name                = "start-redshift-${random_pet.suffix.id}"
  schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action     = "start"
  redshift_schedule   = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test-execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                    = module.redshift-stop-friday.scheduler_lambda_name
  redshift_cluster_to_scheduled_name  = aws_redshift_cluster.scheduled.cluster_identifier
  redshift_cluster_not_scheduled_name = aws_redshift_cluster.not_scheduled.cluster_identifier
}
