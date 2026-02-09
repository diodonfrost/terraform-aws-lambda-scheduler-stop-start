run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.ec2_stop_friday.scheduler_lambda_name == "stop-ec2-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.ec2_start_monday.scheduler_lambda_name == "start-ec2-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].instance_1_scheduled_state == "running"
    error_message = "Virtual machine 1 to stop is not running"
  }

  assert {
    condition     = module.test_execution[0].instance_2_scheduled_state == "running"
    error_message = "Virtual machine 2 to stop is not running"
  }

  assert {
    condition     = module.test_execution[0].instance_3_scheduled_state == "running"
    error_message = "Virtual machine 3 to stop is not running"
  }

  assert {
    condition     = module.test_execution[0].instance_1_not_scheduled_state == "running"
    error_message = "Virtual machine 1 to stop is not Running"
  }

  assert {
    condition     = module.test_execution[0].instance_2_not_scheduled_state == "running"
    error_message = "Virtual machine 2 to stop is not Running"
  }
}
