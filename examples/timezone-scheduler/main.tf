# Deploy two lambda for testing with awspec
resource "random_pet" "suffix" {}

module "aws_stop_friday" {
  source                       = "../.."
  name                         = "stop-aws-${random_pet.suffix.id}"
  schedule_expression          = "cron(0 23 ? * FRI *)"
  schedule_expression_timezone = "Europe/Paris"
  schedule_action              = "stop"
  autoscaling_schedule         = "true"
  ec2_schedule                 = "true"
  rds_schedule                 = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "aws_start_monday" {
  source                       = "../.."
  name                         = "start-aws-${random_pet.suffix.id}"
  schedule_expression          = "cron(0 07 ? * MON *)"
  schedule_expression_timezone = "Europe/Berlin"
  schedule_action              = "start"
  autoscaling_schedule         = "true"
  ec2_schedule                 = "true"
  rds_schedule                 = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}
