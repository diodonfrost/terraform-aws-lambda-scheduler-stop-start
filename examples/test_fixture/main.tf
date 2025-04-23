# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

resource "aws_kms_key" "scheduler" {
  description             = "test kms option on scheduler module"
  deletion_window_in_days = 7
}

module "aws-stop-friday" {
  source                         = "../.."
  name                           = "stop-aws-${random_pet.suffix.id}"
  kms_key_arn                    = aws_kms_key.scheduler.arn
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  autoscaling_schedule           = "true"
  ec2_schedule                   = "true"
  rds_schedule                   = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "aws-start-monday" {
  source                         = "../.."
  name                           = "start-aws-${random_pet.suffix.id}"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  autoscaling_schedule           = "true"
  ec2_schedule                   = "true"
  rds_schedule                   = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}
