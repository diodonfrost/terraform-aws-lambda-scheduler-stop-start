output "redshift_cluster_to_scheduled_state" {
  description = "State of the Redshift cluster that should be stopped"
  value       = data.local_file.redshift_cluster_to_scheduled.content
}

output "redshift_cluster_not_scheduled_state" {
  description = "State of the Redshift cluster that should not be stopped"
  value       = data.local_file.redshift_cluster_not_scheduled.content
}
