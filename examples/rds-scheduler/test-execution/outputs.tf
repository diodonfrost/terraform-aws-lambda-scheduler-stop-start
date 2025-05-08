output "rds_aurora_cluster_to_scheduled" {
  description = "The status of the RDS cluster"
  value       = data.local_file.rds_aurora_cluster_to_scheduled.content
}

output "rds_mariadb_instance_to_scheduled" {
  description = "The status of the RDS instance"
  value       = data.local_file.rds_mariadb_instance_to_scheduled.content
}

output "rds_mysql_instance_to_not_scheduled" {
  description = "The status of the RDS instance"
  value       = data.local_file.rds_mysql_instance_to_not_scheduled.content
}
