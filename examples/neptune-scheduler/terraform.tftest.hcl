run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.neptune-stop-friday.scheduler_lambda_name == "stop-neptune-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.neptune-start-monday.scheduler_lambda_name == "start-neptune-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test-execution[0].neptune_cluster_to_scheduled_status == "stopped\n"
    error_message = "neptune cluster with tag 'tostop=true' should be stopped"
  }

  assert {
    condition     = module.test-execution[0].neptune_cluster_not_scheduled_status == "available\n"
    error_message = "neptune cluster with tag 'tostop=false' should not be stopped"
  }
}

# Add this cleanup step to restore the cluster to 'available' state before destruction
run "cleanup_test_resources" {
  command = apply

  variables {
    neptune_cluster_name = run.create_test_infrastructure.neptune_cluster_scheduled_identifier
  }

  # This will start the stopped cluster to ensure proper deletion
  module {
    source = "./test-cleanup"
  }
}
