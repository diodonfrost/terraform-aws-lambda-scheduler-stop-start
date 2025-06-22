# Terraform redshift-scheduler outputs

output "lambda_stop_name" {
  description = "The name of the lambda function to stop the redshift cluster"
  value       = module.redshift_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the redshift cluster"
  value       = module.redshift_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the redshift cluster"
  value       = module.redshift_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the redshift cluster"
  value       = module.redshift_start_monday.scheduler_lambda_arn
}

output "redshift_cluster_scheduled_identifier" {
  description = "The identifier of the scheduled redshift cluster"
  value       = aws_redshift_cluster.scheduled.cluster_identifier
}

output "redshift_cluster_not_scheduled_identifier" {
  description = "The identifier of the not scheduled redshift cluster"
  value       = aws_redshift_cluster.not_scheduled.cluster_identifier
}
