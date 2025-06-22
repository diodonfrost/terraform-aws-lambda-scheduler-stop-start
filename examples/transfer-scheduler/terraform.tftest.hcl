run "test_transfer_scheduler" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.transfer_stop_friday.scheduler_lambda_name == "stop-transfer-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.transfer_start_monday.scheduler_lambda_name == "start-transfer-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].transfer_server_to_scheduled_state == "OFFLINE\n"
    error_message = "Invalid Transfer server state"
  }

  assert {
    condition     = module.test_execution[0].transfer_server_not_scheduled_state == "ONLINE\n"
    error_message = "Invalid Transfer server state"
  }
}
