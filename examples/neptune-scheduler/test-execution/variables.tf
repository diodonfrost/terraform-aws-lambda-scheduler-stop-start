variable "neptune_cluster_to_scheduled_name" {
  description = "Name of the Neptune cluster that should be scheduled for stop/start"
  type        = string
}

variable "neptune_cluster_not_scheduled_name" {
  description = "Name of the Neptune cluster that should not be scheduled for stop/start"
  type        = string
}

variable "lambda_stop_name" {
  description = "Name of the Lambda function that stops the Neptune cluster"
  type        = string
} 