variable "lambda_stop_name" {
  description = "Name of the lambda function to stop DocumentDB clusters"
  type        = string
}

variable "docdb_cluster_to_scheduled_name" {
  description = "Name of the DocumentDB cluster that should be stopped"
  type        = string
}

variable "docdb_cluster_not_scheduled_name" {
  description = "Name of the DocumentDB cluster that should not be stopped"
  type        = string
}
