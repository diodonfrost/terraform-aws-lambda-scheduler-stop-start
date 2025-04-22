run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.autoscaling-stop-friday.scheduler_lambda_name == "stop-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.autoscaling-start-monday.scheduler_lambda_name == "start-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
