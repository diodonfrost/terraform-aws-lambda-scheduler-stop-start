# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

resource "aws_docdb_cluster" "scheduled" {
  cluster_identifier   = "test-to-stop-${random_pet.suffix.id}"
  engine               = "docdb"
  master_username      = "foo"
  master_password      = "mustbeeightchars"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_docdb_subnet_group.documentdb.name
  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_docdb_cluster_instance" "scheduled" {
  identifier         = "test-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_docdb_cluster.scheduled.id
  instance_class     = "db.r5.large"
  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_docdb_cluster" "not_scheduled" {
  cluster_identifier   = "test-not-to-stop-${random_pet.suffix.id}"
  engine               = "docdb"
  master_username      = "foo"
  master_password      = "mustbeeightchars"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_docdb_subnet_group.documentdb.name
  tags = {
    tostop = "false"
  }
}

resource "aws_docdb_cluster_instance" "not_scheduled" {
  identifier         = "test-not-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_docdb_cluster.not_scheduled.id
  instance_class     = "db.r5.large"
  tags = {
    tostop = "false"
  }
}


module "documentdb_stop_friday" {
  source              = "../.."
  name                = "stop-documentdb-${random_pet.suffix.id}"
  kms_key_arn         = aws_kms_key.scheduler.arn
  schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action     = "stop"
  documentdb_schedule = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "documentdb_start_monday" {
  source              = "../.."
  name                = "start-documentdb-${random_pet.suffix.id}"
  schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action     = "start"
  documentdb_schedule = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test_execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                 = module.documentdb_stop_friday.scheduler_lambda_name
  docdb_cluster_to_scheduled_name  = aws_docdb_cluster.scheduled.cluster_identifier
  docdb_cluster_not_scheduled_name = aws_docdb_cluster.not_scheduled.cluster_identifier

  depends_on = [
    aws_docdb_cluster_instance.scheduled,
    aws_docdb_cluster_instance.not_scheduled
  ]
}
