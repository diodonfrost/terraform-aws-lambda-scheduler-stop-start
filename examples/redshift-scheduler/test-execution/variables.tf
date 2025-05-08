variable "lambda_stop_name" {
  description = "Name of the lambda function to stop Redshift clusters"
  type        = string
}

variable "redshift_cluster_to_scheduled_name" {
  description = "Name of the Redshift cluster that should be stopped"
  type        = string
}

variable "redshift_cluster_not_scheduled_name" {
  description = "Name of the Redshift cluster that should not be stopped"
  type        = string
}
