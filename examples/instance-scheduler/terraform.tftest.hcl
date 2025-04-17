run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.ec2-stop-friday.scheduler_lambda_name == "stop-ec2-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.ec2-start-monday.scheduler_lambda_name == "start-ec2-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
