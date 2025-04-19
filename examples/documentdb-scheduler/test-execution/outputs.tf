output "docdb_cluster_to_scheduled_state" {
  description = "State of the DocumentDB cluster that should be stopped"
  value       = data.local_file.docdb_cluster_to_scheduled.content
}

output "docdb_cluster_not_scheduled_state" {
  description = "State of the DocumentDB cluster that should not be stopped"
  value       = data.local_file.docdb_cluster_not_scheduled.content
} 