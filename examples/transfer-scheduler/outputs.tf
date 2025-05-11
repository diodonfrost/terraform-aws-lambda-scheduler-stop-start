output "lambda_stop_name" {
  value = module.transfer-stop-friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  value = module.transfer-stop-friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  value = module.transfer-start-monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  value = module.transfer-start-monday.scheduler_lambda_arn
}

output "transfer_server_scheduled_id" {
  description = "ID of the scheduled Transfer server"
  value       = aws_transfer_server.to_scheduled.id
}

output "transfer_server_not_scheduled_id" {
  description = "ID of the non-scheduled Transfer server"
  value       = aws_transfer_server.not_to_scheduled.id
} 