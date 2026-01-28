resource "random_pet" "suffix" {}

data "aws_region" "current" {}

module "apprunner_stop_friday" {
  source              = "../../"
  name                = "stop-apprunner-${random_pet.suffix.id}"
  schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action     = "stop"
  apprunner_schedule  = true

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "apprunner_start_monday" {
  source              = "../../"
  name                = "start-apprunner-${random_pet.suffix.id}"
  schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action     = "start"
  apprunner_schedule  = true

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test_execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name             = module.apprunner_stop_friday.scheduler_lambda_name
  service_to_scheduled_arn     = aws_apprunner_service.to_scheduled.arn
  service_not_to_scheduled_arn = aws_apprunner_service.not_to_scheduled.arn
}
