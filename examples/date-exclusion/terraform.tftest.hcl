run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.ec2_stop_with_exclusions.scheduler_lambda_name == "stop-ec2-exclusions-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.ec2_start_with_exclusions.scheduler_lambda_name == "start-ec2-exclusions-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].instance_1_scheduled_state == "running"
    error_message = "Instance 1 should remain running (current date is excluded)"
  }

  assert {
    condition     = module.test_execution[0].instance_2_scheduled_state == "running"
    error_message = "Instance 2 should remain running (current date is excluded)"
  }

  assert {
    condition     = module.test_execution[0].instance_not_scheduled_state == "running"
    error_message = "Instance not scheduled should remain running"
  }
}
