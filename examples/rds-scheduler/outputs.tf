# Terraform ex2-schedule outputs

output "lambda_stop_name" {
  description = "The name of the lambda function to stop the RDS cluster"
  value       = module.rds_stop_friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  description = "The ARN of the lambda function to stop the RDS cluster"
  value       = module.rds_stop_friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  description = "The name of the lambda function to start the RDS cluster"
  value       = module.rds_start_monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  description = "The ARN of the lambda function to start the RDS cluster"
  value       = module.rds_start_monday.scheduler_lambda_arn
}

output "rds_aurora_cluster_name" {
  description = "The name of the scheduled RDS cluster"
  value       = aws_rds_cluster.aurora_scheduled.cluster_identifier
}

output "rds_aurora_instance_name" {
  description = "The name of the scheduled RDS instance"
  value       = aws_rds_cluster_instance.aurora_scheduled.identifier
}
