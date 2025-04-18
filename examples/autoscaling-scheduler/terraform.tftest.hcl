run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.autoscaling-stop-friday.scheduler_lambda_name == "stop-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.autoscaling-start-monday.scheduler_lambda_name == "start-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition = module.test-execution.asg_scheduled_suspended_processes == toset([
      "AZRebalance",
      "AddToLoadBalancer",
      "AlarmNotification",
      "HealthCheck",
      "InstanceRefresh",
      "Launch",
      "RemoveFromLoadBalancerLowPriority",
      "ReplaceUnhealthy",
      "ScheduledActions",
      "Terminate",
    ])
    error_message = "Autoscaling group instances should be suspended"
  }

  assert {
    condition     = length(module.test-execution.asg_not_scheduled_suspended_processes) == 0
    error_message = "Autoscaling group instances should not be suspended"
  }

  assert {
    condition     = module.test-execution.asg_instance_scheduled_state == "stopped"
    error_message = "Autoscaling group instance should be stopped"
  }

  assert {
    condition     = module.test-execution.asg_instance_not_scheduled_state == "running"
    error_message = "Autoscaling group instance should be running"
  }
}
