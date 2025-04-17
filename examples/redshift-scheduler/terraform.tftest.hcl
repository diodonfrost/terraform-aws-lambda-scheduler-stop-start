run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.redshift-stop-friday.scheduler_lambda_name == "stop-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.redshift-start-monday.scheduler_lambda_name == "start-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
