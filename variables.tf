# Terraform variables file

# Set cloudwatch events for shutingdown instances
# trigger lambda functuon every night at 22h00 from Monday to Friday
# cf doc : https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
variable "cloudwatch_schedule_expression" {
  description = "Define the aws cloudwatch event rule schedule expression"
  type        = string
  default     = "cron(0 22 ? * MON-FRI *)"
}

variable "name" {
  description = "Define name to use for lambda function, cloudwatch event and iam role"
  type        = string
}

variable "custom_iam_role_arn" {
  description = "Custom IAM role arn for the scheduling lambda"
  type        = string
  default     = null
}

variable "kms_key_arn" {
  description = "The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key."
  type        = string
  default     = null
}

variable "aws_regions" {
  description = "A list of one or more aws regions where the lambda will be apply, default use the current region"
  type        = list(string)
  default     = null
}

variable "schedule_action" {
  description = "Define schedule action to apply on resources, accepted value are 'stop or 'start"
  type        = string
  default     = "stop"
}

variable "resources_tag" {
  # This variable has been renamed to "scheduler_tag"
  description = "DEPRECATED, use scheduler_tag variable instead"
  type        = map(string)
  default     = null
}

variable "scheduler_tag" {
  description = "Set the tag to use for identify aws resources to stop or start"
  type        = map(string)

  default = {
    "key"   = "tostop"
    "value" = "true"
  }
}

variable "autoscaling_schedule" {
  description = "Enable scheduling on autoscaling resources"
  type        = any
  default     = false
}

variable "autoscaling_terminate_instances" {
  description = "Terminate instances when autoscaling group is scheduled to stop"
  type        = bool
  default     = false
}

variable "ec2_schedule" {
  description = "Enable scheduling on ec2 resources"
  type        = any
  default     = false
}

variable "documentdb_schedule" {
  description = "Enable scheduling on documentdb resources"
  type        = bool
  default     = false
}

variable "ecs_schedule" {
  description = "Enable scheduling on ecs services"
  type        = bool
  default     = false
}

variable "ecs_task_desired_count" {
  description = "Define desired task count for ecs service"
  type        = number
  default     = 1
}

variable "rds_schedule" {
  description = "Enable scheduling on rds resources"
  type        = any
  default     = false
}

variable "redshift_schedule" {
  description = "Enable scheduling on redshift resources"
  type        = any
  default     = false
}

variable "cloudwatch_alarm_schedule" {
  description = "Enable scheduleding on cloudwatch alarm resources"
  type        = any
  default     = false
}

variable "tags" {
  description = "Custom tags on aws resources"
  type        = map(any)
  default     = null
}
