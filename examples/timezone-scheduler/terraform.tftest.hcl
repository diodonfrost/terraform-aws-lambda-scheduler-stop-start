run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.aws_stop_friday.scheduler_lambda_name == "stop-aws-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.aws_start_monday.scheduler_lambda_name == "start-aws-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.aws_stop_friday.scheduler_expression == "cron(0 23 ? * FRI *)"
    error_message = "Invalid scheduler expression"
  }

  assert {
    condition     = module.aws_start_monday.scheduler_expression == "cron(0 07 ? * MON *)"
    error_message = "Invalid scheduler expression"
  }

  assert {
    condition     = module.aws_stop_friday.scheduler_timezone == "Europe/Paris"
    error_message = "Invalid scheduler timezone"
  }

  assert {
    condition     = module.aws_start_monday.scheduler_timezone == "Europe/Berlin"
    error_message = "Invalid scheduler timezone"
  }
}
