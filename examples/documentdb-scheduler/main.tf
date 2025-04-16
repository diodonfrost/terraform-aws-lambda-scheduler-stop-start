# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

resource "aws_docdb_cluster" "scheduled" {
  cluster_identifier  = "test-to-stop-${random_pet.suffix.id}"
  engine              = "docdb"
  master_username     = "foo"
  master_password     = "mustbeeightchars"
  skip_final_snapshot = true
  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

resource "aws_docdb_cluster_instance" "scheduled" {
  identifier         = "test-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_docdb_cluster.scheduled.id
  instance_class     = "db.r5.large"
  tags = {
    tostop        = "true"
    terratest_tag = var.random_tag
  }
}

resource "aws_docdb_cluster" "not_scheduled" {
  cluster_identifier  = "test-not-to-stop-${random_pet.suffix.id}"
  engine              = "docdb"
  master_username     = "foo"
  master_password     = "mustbeeightchars"
  skip_final_snapshot = true
  tags = {
    tostop        = "false"
    terratest_tag = var.random_tag
  }
}

resource "aws_docdb_cluster_instance" "not_scheduled" {
  identifier         = "test-not-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_docdb_cluster.not_scheduled.id
  instance_class     = "db.r5.large"
  tags = {
    tostop        = "false"
    terratest_tag = var.random_tag
  }
}


module "documentdb-stop-friday" {
  source                         = "../.."
  name                           = "stop-documentdb-${random_pet.suffix.id}"
  kms_key_arn                    = aws_kms_key.scheduler.arn
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  documentdb_schedule            = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "documentdb-start-monday" {
  source                         = "../.."
  name                           = "start-documentdb-${random_pet.suffix.id}"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  documentdb_schedule            = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
