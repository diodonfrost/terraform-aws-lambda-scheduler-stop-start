# Terraform documentdb-scheduler outputs

output "lambda_stop_name" {
  description = "The name of the lambda function to stop the Neptune cluster"
  value       = module.neptune_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the Neptune cluster"
  value       = module.neptune_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the Neptune cluster"
  value       = module.neptune_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the Neptune cluster"
  value       = module.neptune_start_monday.scheduler_lambda_arn
}

output "neptune_cluster_scheduled_identifier" {
  description = "The identifier of the scheduled Neptune cluster"
  value       = aws_neptune_cluster.to_schedule.cluster_identifier
}

output "neptune_instance_scheduled_identifier" {
  description = "The identifier of the scheduled Neptune instance"
  value       = aws_neptune_cluster_instance.to_schedule.identifier
}

output "neptune_cluster_not_scheduled_identifier" {
  description = "The identifier of the not scheduled Neptune cluster"
  value       = aws_neptune_cluster.not_to_scheduled.cluster_identifier
}

output "neptune_instance_not_scheduled_identifier" {
  description = "The identifier of the not scheduled Neptune instance"
  value       = aws_neptune_cluster_instance.not_to_scheduled.identifier
}
