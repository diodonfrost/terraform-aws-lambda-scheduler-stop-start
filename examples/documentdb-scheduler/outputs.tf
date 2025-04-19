# Terraform documentdb-scheduler outputs

output "lambda_stop_name" {
  value = module.documentdb-stop-friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  value = module.documentdb-stop-friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  value = module.documentdb-start-monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  value = module.documentdb-start-monday.scheduler_lambda_arn
}

output "docdb_cluster_scheduled_identifier" {
  value = aws_docdb_cluster.scheduled.cluster_identifier
}

output "docdb_instance_scheduled_identifier" {
  value = aws_docdb_cluster_instance.scheduled.identifier
}

output "docdb_cluster_not_scheduled_identifier" {
  value = aws_docdb_cluster.not_scheduled.cluster_identifier
}

output "docdb_instance_not_scheduled_identifier" {
  value = aws_docdb_cluster_instance.not_scheduled.identifier
}
