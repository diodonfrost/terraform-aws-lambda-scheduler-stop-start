# Terraform ex2-schedule outputs

output "lambda_stop_name" {
  value = "${module.spot-terminate-friday.scheduler_lambda_name}"
}

output "lambda_stop_arn" {
  value = "${module.spot-terminate-friday.scheduler_lambda_arn}"
}
