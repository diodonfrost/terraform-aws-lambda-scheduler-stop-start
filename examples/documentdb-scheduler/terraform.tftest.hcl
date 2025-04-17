run "create_test_infrastructure" {
  command = apply

  assert {
    condition     = module.documentdb-stop-friday.scheduler_lambda_name == "stop-documentdb-${random_pet.suffix.id}"
    error_message = "Invalid Stop lambda name"
  }

  assert {
    condition     = module.documentdb-start-monday.scheduler_lambda_name == "start-documentdb-${random_pet.suffix.id}"
    error_message = "Invalid Start lambda name"
  }
}
