variable "lambda_stop_name" {
  description = "Name of the Lambda function used for stopping instances"
  type        = string
}

variable "instance_1_to_scheduled_id" {
  description = "ID of the first instance to be scheduled"
  type        = string
}

variable "instance_2_to_scheduled_id" {
  description = "ID of the second instance to be scheduled"
  type        = string
}

variable "instance_3_to_scheduled_id" {
  description = "ID of the third instance to be scheduled"
  type        = string
}

variable "instance_1_not_to_scheduled_id" {
  description = "ID of the first instance not to be scheduled"
  type        = string
}

variable "instance_2_not_to_scheduled_id" {
  description = "ID of the second instance not to be scheduled"
  type        = string
}
