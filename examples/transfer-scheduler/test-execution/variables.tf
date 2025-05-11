variable "lambda_stop_name" {
  description = "Name of the lambda function"
  type        = string
}

variable "transfer_server_to_scheduled_id" {
  description = "ID of the scheduled Transfer server"
  type        = string
}

variable "transfer_server_not_scheduled_id" {
  description = "ID of the non-scheduled Transfer server"
  type        = string
}
