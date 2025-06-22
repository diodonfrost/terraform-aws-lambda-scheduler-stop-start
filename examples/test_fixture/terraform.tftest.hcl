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
}
