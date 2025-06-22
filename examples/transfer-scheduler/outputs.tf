output "lambda_stop_name" {
  description = "The name of the lambda function to stop the transfer server"
  value       = module.transfer_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the transfer server"
  value       = module.transfer_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the transfer server"
  value       = module.transfer_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the transfer server"
  value       = module.transfer_start_monday.scheduler_lambda_arn
}

output "transfer_server_scheduled_id" {
  description = "ID of the scheduled Transfer server"
  value       = aws_transfer_server.to_scheduled.id
}

output "transfer_server_not_scheduled_id" {
  description = "ID of the non-scheduled Transfer server"
  value       = aws_transfer_server.not_to_scheduled.id
}
