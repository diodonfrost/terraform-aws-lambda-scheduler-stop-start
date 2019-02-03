output "scheduler_lambda_arn" {
  value = "${aws_lambda_function.stop_start.arn}"
}
