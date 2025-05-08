run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.documentdb-stop-friday.scheduler_lambda_name == "stop-documentdb-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.documentdb-start-monday.scheduler_lambda_name == "start-documentdb-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test-execution[0].docdb_cluster_to_scheduled_state == "stopping\n"
    error_message = "DocumentDB cluster with tag 'tostop=true' should be stopped"
  }

  assert {
    condition     = module.test-execution[0].docdb_cluster_not_scheduled_state == "available\n"
    error_message = "DocumentDB cluster with tag 'tostop=false' should not be stopped"
  }
}

# Add this cleanup step to restore the cluster to 'available' state before destruction
run "cleanup_test_resources" {
  command = apply

  variables {
    docdb_cluster_name  = run.create_test_infrastructure.docdb_cluster_scheduled_identifier
    docdb_instance_name = run.create_test_infrastructure.docdb_instance_scheduled_identifier
  }

  # This will start the stopped cluster to ensure proper deletion
  module {
    source = "./test-cleanup"
  }
}
