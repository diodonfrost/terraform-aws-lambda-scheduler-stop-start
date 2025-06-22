# Terraform ex2-schedule outputs

output "lambda_stop_name" {
  description = "The name of the lambda function to stop the ECS cluster"
  value       = module.ecs_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the ECS cluster"
  value       = module.ecs_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the ECS cluster"
  value       = module.ecs_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the ECS cluster"
  value       = module.ecs_start_monday.scheduler_lambda_arn
}
