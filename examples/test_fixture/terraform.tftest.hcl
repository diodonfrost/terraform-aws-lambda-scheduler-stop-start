run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.aws-stop-friday.scheduler_lambda_name == "stop-aws-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.aws-start-monday.scheduler_lambda_name == "start-aws-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
