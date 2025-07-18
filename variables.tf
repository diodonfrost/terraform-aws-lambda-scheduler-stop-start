# Terraform variables file

variable "schedule_expression" {
  description = "Define the aws event rule schedule expression, https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html"
  type        = string
  default     = "cron(0 22 ? * MON-FRI *)"
}

variable "schedule_expression_timezone" {
  description = "Timezone in which the scheduling expression is evaluated. Example : 'America/New_York', 'Europe/Paris'"
  type        = string
  default     = "UTC"
}

variable "scheduler_excluded_dates" {
  description = "List of specific dates to exclude from scheduling in MM-DD format (e.g., ['12-25', '01-01'])"
  type        = list(string)
  default     = []

  validation {
    condition = alltrue([
      for date in var.scheduler_excluded_dates : can(regex("^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", date))
    ])
    error_message = "Excluded dates must be in MM-DD format (e.g., '12-25', '01-01')."
  }
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

variable "runtime" {
  description = "The runtime environment for the Lambda function that you are uploading"
  type        = string
  default     = "python3.13"
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
  type        = bool
  default     = false
}

variable "autoscaling_terminate_instances" {
  description = "Terminate instances when autoscaling group is scheduled to stop"
  type        = bool
  default     = false
}

variable "ec2_schedule" {
  description = "Enable scheduling on ec2 resources"
  type        = bool
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

variable "rds_schedule" {
  description = "Enable scheduling on rds resources"
  type        = bool
  default     = false
}

variable "redshift_schedule" {
  description = "Enable scheduling on redshift resources"
  type        = bool
  default     = false
}

variable "cloudwatch_alarm_schedule" {
  description = "Enable scheduleding on cloudwatch alarm resources"
  type        = bool
  default     = false
}

variable "transfer_schedule" {
  description = "Enable scheduling on AWS Transfer (SFTP) servers"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Custom tags on aws resources"
  type        = map(any)
  default     = null
}
