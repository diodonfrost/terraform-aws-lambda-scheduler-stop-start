# Terraform redshift-scheduler outputs

output "lambda_stop_name" {
  value = module.redshift-stop-friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  value = module.redshift-stop-friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  value = module.redshift-start-monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  value = module.redshift-start-monday.scheduler_lambda_arn
}

output "redshift_cluster_scheduled_identifier" {
  value = aws_redshift_cluster.scheduled.cluster_identifier
}

output "redshift_cluster_not_scheduled_identifier" {
  value = aws_redshift_cluster.not_scheduled.cluster_identifier
}
