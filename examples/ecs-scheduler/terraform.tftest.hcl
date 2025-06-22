run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.ecs_stop_friday.scheduler_lambda_name == "stop-ecs-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.ecs_start_monday.scheduler_lambda_name == "start-ecs-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
