run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.apprunner_stop_friday.scheduler_lambda_name == "stop-apprunner-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.apprunner_start_monday.scheduler_lambda_name == "start-apprunner-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].service_scheduled_status == "PAUSED" || module.test_execution[0].service_scheduled_status == "OPERATION_IN_PROGRESS"
    error_message = "App Runner service to stop is not paused"
  }

  assert {
    condition     = module.test_execution[0].service_not_scheduled_status == "RUNNING"
    error_message = "App Runner service not to stop is not running"
  }
}
