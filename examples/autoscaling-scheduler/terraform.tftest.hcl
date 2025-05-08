run "create_test_infrastructure" {
  command = apply

  variables {
    test_mode = true
  }

  assert {
    condition     = module.autoscaling-stop-friday.scheduler_lambda_name == "stop-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.autoscaling-start-monday.scheduler_lambda_name == "start-autoscaling-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }

  assert {
    condition = module.test-execution[0].asg_scheduled_suspended_processes == toset([
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
    condition     = length(module.test-execution[0].asg_not_scheduled_suspended_processes) == 0
    error_message = "Autoscaling group instances should not be suspended"
  }

  assert {
    condition     = module.test-execution[0].asg_instance_scheduled_state == "stopped" || module.test-execution[0].asg_instance_scheduled_state == "stopping"
    error_message = "Autoscaling group instance should be stopped"
  }

  assert {
    condition     = module.test-execution[0].asg_instance_not_scheduled_state == "running"
    error_message = "Autoscaling group instance should be running"
  }
}
