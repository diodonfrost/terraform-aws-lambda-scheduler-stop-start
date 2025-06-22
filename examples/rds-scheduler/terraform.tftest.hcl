run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.rds_stop_friday.scheduler_lambda_name == "stop-rds-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.rds_start_monday.scheduler_lambda_name == "start-rds-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition     = module.test_execution[0].rds_aurora_cluster_to_scheduled == "stopped\n"
    error_message = "Invalid RDS cluster instance state"
  }

  assert {
    condition     = module.test_execution[0].rds_mariadb_instance_to_scheduled == "stopped\n"
    error_message = "Invalid RDS instance state"
  }

  assert {
    condition     = module.test_execution[0].rds_mysql_instance_to_not_scheduled == "available\n"
    error_message = "Invalid RDS instance state"
  }
}

# Add this cleanup step to restore the cluster to 'available' state before destruction
run "cleanup_test_resources" {
  command = apply

  variables {
    rds_aurora_cluster_name  = run.create_test_infrastructure.rds_aurora_cluster_name
    rds_aurora_instance_name = run.create_test_infrastructure.rds_aurora_instance_name
  }

  # This will start the stopped cluster to ensure proper deletion
  module {
    source = "./test-cleanup"
  }
}
