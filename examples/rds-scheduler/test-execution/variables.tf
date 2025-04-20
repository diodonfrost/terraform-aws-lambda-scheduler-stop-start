variable "lambda_stop_name" {
  description = "Name of the Lambda function used for stopping instances"
  type        = string
}

variable "rds_aurora_cluster_to_scheduled_name" {
  description = "rds cluster name to be scheduled"
  type        = string
}

variable "rds_mariadb_instance_to_scheduled_name" {
  description = "rds instance name to be scheduled"
  type        = string
}

variable "rds_mysql_instance_to_not_scheduled_name" {
  description = "rds instance name to not be scheduled"
  type        = string
}
