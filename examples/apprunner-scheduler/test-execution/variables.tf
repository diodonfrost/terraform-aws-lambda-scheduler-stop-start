variable "lambda_stop_name" {
  description = "Name of the Lambda function used for stopping App Runner services"
  type        = string
}

variable "service_to_scheduled_arn" {
  description = "ARN of the App Runner service to be scheduled"
  type        = string
}

variable "service_not_to_scheduled_arn" {
  description = "ARN of the App Runner service not to be scheduled"
  type        = string
}
