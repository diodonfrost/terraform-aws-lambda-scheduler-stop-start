# Terraform documentdb-scheduler outputs

output "lambda_stop_name" {
  value = module.neptune-stop-friday.scheduler_lambda_name
}

output "lambda_stop_arn" {
  value = module.neptune-stop-friday.scheduler_lambda_arn
}

output "lambda_start_name" {
  value = module.neptune-start-monday.scheduler_lambda_name
}

output "lambda_start_arn" {
  value = module.neptune-start-monday.scheduler_lambda_arn
}

output "neptune_cluster_scheduled_identifier" {
  value = aws_neptune_cluster.to_schedule.cluster_identifier
}

output "neptune_instance_scheduled_identifier" {
  value = aws_neptune_cluster_instance.to_schedule.identifier
}

output "neptune_cluster_not_scheduled_identifier" {
  value = aws_neptune_cluster.not_to_scheduled.cluster_identifier
}

output "neptune_instance_not_scheduled_identifier" {
  value = aws_neptune_cluster_instance.not_to_scheduled.identifier
}
