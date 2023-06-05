# Deploy two lambda for testing with awspec

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

resource "aws_redshift_cluster" "scheduled" {
  cluster_identifier  = "tf-redshift-cluster-scheduled"
  database_name       = "mydb"
  master_username     = "exampleuser"
  master_password     = "Mustbe8characters"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  skip_final_snapshot = true

  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

resource "aws_redshift_cluster_snapshot" "scheduled" {
  cluster_identifier  = aws_redshift_cluster.scheduled.id
  snapshot_identifier = "snapshot-cluster-scheduled"
}

resource "aws_redshift_cluster" "not_scheduled" {
  cluster_identifier  = "tf-redshift-cluster-not-scheduled"
  database_name       = "mydb"
  master_username     = "exampleuser"
  master_password     = "Mustbe8characters"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  skip_final_snapshot = true

  tags = {
    tostop        = "false"
    terratest_tag = var.random_tag
  }
}

resource "aws_redshift_cluster_snapshot" "not_scheduled" {
  cluster_identifier  = aws_redshift_cluster.not_scheduled.id
  snapshot_identifier = "snapshot-cluster-not-scheduled"
}


module "redshift-stop-friday" {
  source                         = "../.."
  name                           = "stop-redshift"
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
  name                           = "start-redshift"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  redshift_schedule              = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
