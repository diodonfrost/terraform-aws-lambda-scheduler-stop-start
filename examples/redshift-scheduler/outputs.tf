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
