# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_neptune_cluster" "to_schedule" {
  cluster_identifier                  = "test-to-stop-${random_pet.suffix.id}"
  engine                              = "neptune"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
  apply_immediately                   = true
  neptune_subnet_group_name           = aws_neptune_subnet_group.test.name

  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_neptune_cluster_instance" "to_schedule" {
  identifier         = "test-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_neptune_cluster.to_schedule.id
  engine             = "neptune"
  instance_class     = "db.t3.medium"
  apply_immediately  = true

  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_neptune_cluster" "not_to_scheduled" {
  cluster_identifier                  = "test-not-to-stop-${random_pet.suffix.id}"
  engine                              = "neptune"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
  apply_immediately                   = true
  neptune_subnet_group_name           = aws_neptune_subnet_group.test.name

  tags = {
    tostop = "false"
  }
}

resource "aws_neptune_cluster_instance" "not_to_scheduled" {
  identifier         = "test-not-to-stop-${random_pet.suffix.id}"
  cluster_identifier = aws_neptune_cluster.not_to_scheduled.id
  engine             = "neptune"
  instance_class     = "db.t3.medium"
  apply_immediately  = true

  tags = {
    tostop = "false"
  }
}


module "neptune-stop-friday" {
  source              = "../.."
  name                = "stop-neptune-${random_pet.suffix.id}"
  schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action     = "stop"
  rds_schedule        = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "neptune-start-monday" {
  source              = "../.."
  name                = "start-neptune-${random_pet.suffix.id}"
  schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action     = "start"
  rds_schedule        = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test-execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                   = module.neptune-stop-friday.scheduler_lambda_name
  neptune_cluster_to_scheduled_name  = aws_neptune_cluster.to_schedule.cluster_identifier
  neptune_cluster_not_scheduled_name = aws_neptune_cluster.not_to_scheduled.cluster_identifier

  depends_on = [
    aws_neptune_cluster_instance.to_schedule,
    aws_neptune_cluster_instance.not_to_scheduled
  ]
}
