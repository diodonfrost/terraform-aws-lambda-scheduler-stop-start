# Terraform documentdb-scheduler outputs

output "lambda_stop_name" {
  description = "The name of the lambda function to stop the documentdb cluster"
  value       = module.documentdb_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the documentdb cluster"
  value       = module.documentdb_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the documentdb cluster"
  value       = module.documentdb_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the documentdb cluster"
  value       = module.documentdb_start_monday.scheduler_lambda_arn
}

output "docdb_cluster_scheduled_identifier" {
  description = "The identifier of the scheduled documentdb cluster"
  value       = aws_docdb_cluster.scheduled.cluster_identifier
}

output "docdb_instance_scheduled_identifier" {
  description = "The identifier of the scheduled documentdb instance"
  value       = aws_docdb_cluster_instance.scheduled.identifier
}

output "docdb_cluster_not_scheduled_identifier" {
  description = "The identifier of the not scheduled documentdb cluster"
  value       = aws_docdb_cluster.not_scheduled.cluster_identifier
}

output "docdb_instance_not_scheduled_identifier" {
  description = "The identifier of the not scheduled documentdb instance"
  value       = aws_docdb_cluster_instance.not_scheduled.identifier
}
