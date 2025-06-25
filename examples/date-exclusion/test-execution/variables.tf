variable "lambda_stop_name" {
  description = "Name of the lambda function to stop EC2"
  type        = string
}

variable "instance_1_to_scheduled_id" {
  description = "Instance 1 ID to test scheduled action"
  type        = string
}

variable "instance_2_to_scheduled_id" {
  description = "Instance 2 ID to test scheduled action"
  type        = string
}

variable "instance_not_to_scheduled_id" {
  description = "Instance ID not to be scheduled"
  type        = string
}
