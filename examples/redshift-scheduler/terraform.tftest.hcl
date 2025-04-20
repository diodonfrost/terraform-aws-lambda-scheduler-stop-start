run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.redshift-stop-friday.scheduler_lambda_name == "stop-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.redshift-start-monday.scheduler_lambda_name == "start-redshift-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test-execution[0].redshift_cluster_to_scheduled_state == "pausing\n"
    error_message = "Invalid Redshift cluster state"
  }

  assert {
    condition     = module.test-execution[0].redshift_cluster_not_scheduled_state == "available\n"
    error_message = "Invalid Redshift cluster state"
  }
}

# Add this cleanup step to restore the cluster to 'available' state before destruction
run "cleanup_test_resources" {
  command = apply

  variables {
    redshift_cluster_name = run.create_test_infrastructure.redshift_cluster_scheduled_identifier
  }

  # This will start the stopped cluster to ensure proper deletion
  module {
    source = "./test-cleanup"
  }
}
