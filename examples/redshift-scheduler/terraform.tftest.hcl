run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.redshift_stop_friday.scheduler_lambda_name == "stop-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.redshift_start_monday.scheduler_lambda_name == "start-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].redshift_cluster_to_scheduled_state == "paused\n"
    error_message = "Invalid Redshift cluster state"
  }

  assert {
    condition     = module.test_execution[0].redshift_cluster_not_scheduled_state == "available\n"
    error_message = "Invalid Redshift cluster state"
  }
}
