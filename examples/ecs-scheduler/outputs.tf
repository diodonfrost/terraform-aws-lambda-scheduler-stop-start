# Terraform ex2-schedule outputs

output "lambda_stop_name" {
  value = module.ecs-stop-friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  value = module.ecs-stop-friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  value = module.ecs-start-monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  value = module.ecs-start-monday.scheduler_lambda_arn
}
