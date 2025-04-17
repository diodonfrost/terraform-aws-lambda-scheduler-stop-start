run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.rds-stop-friday.scheduler_lambda_name == "stop-rds-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.rds-start-monday.scheduler_lambda_name == "start-rds-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
