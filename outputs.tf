output "lambda_iam_role_arn" {
  description = "The ARN of the IAM role used by Lambda function"
  value       = var.custom_iam_role_arn == null ? aws_iam_role.this[0].arn : var.custom_iam_role_arn
}

output "lambda_iam_role_name" {
  description = "The name of the IAM role used by Lambda function"
  value       = var.custom_iam_role_arn == null ? aws_iam_role.this[0].name : split("/", var.custom_iam_role_arn)[1]
}

output "scheduler_lambda_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.this.arn
}

output "scheduler_lambda_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.this.function_name
}

output "scheduler_lambda_invoke_arn" {
  description = "The ARN to be used for invoking Lambda function from API Gateway"
  value       = aws_lambda_function.this.invoke_arn
}

output "scheduler_lambda_function_last_modified" {
  description = "The date Lambda function was last modified"
  value       = aws_lambda_function.this.last_modified
}

output "scheduler_lambda_function_version" {
  description = "Latest published version of your Lambda function"
  value       = aws_lambda_function.this.version
}

output "scheduler_log_group_name" {
  description = "The name of the scheduler log group"
  value       = aws_cloudwatch_log_group.this.name
}

output "scheduler_log_group_arn" {
  description = "The Amazon Resource Name (ARN) specifying the log group"
  value       = aws_cloudwatch_log_group.this.arn
}
