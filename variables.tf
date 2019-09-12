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

variable "schedule_action" {
  description = "Define schedule action to apply on resources, accepted value are 'stop or 'start"
  type        = string
  default     = "stop"
}

variable "resources_tag" {
  description = "Set the tag use for identify resources to stop or start"
  type        = map(string)

  default = {
    key   = "tostop"
    value = "true"
  }
}

variable "autoscaling_schedule" {
  description = "Enable scheduling on autoscaling resources"
  type        = string
  default     = "false"
}

variable "spot_schedule" {
  description = "Enable scheduling on spot instance resources"
  type        = string
  default     = "false"
}

variable "ec2_schedule" {
  description = "Enable scheduling on ec2 resources"
  type        = string
  default     = "false"
}

variable "rds_schedule" {
  description = "Enable scheduling on rds resources"
  type        = string
  default     = "false"
}
