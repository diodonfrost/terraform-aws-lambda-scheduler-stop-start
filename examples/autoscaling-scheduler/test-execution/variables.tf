variable "lambda_stop_name" {
  description = "Name of the Lambda function used for stopping instances"
  type        = string
}

variable "asg_scheduled_name" {
  description = "Name of the scheduled autoscaling group"
  type        = string
}

variable "asg_not_scheduled_name" {
  description = "Name of the not scheduled autoscaling group"
  type        = string
}
