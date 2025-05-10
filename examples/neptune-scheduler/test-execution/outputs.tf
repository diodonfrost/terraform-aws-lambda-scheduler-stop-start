output "neptune_cluster_to_scheduled_status" {
  description = "Status of the Neptune cluster that should be scheduled for stop/start"
  value       = data.local_file.neptune_cluster_to_scheduled.content
}

output "neptune_cluster_not_scheduled_status" {
  description = "Status of the Neptune cluster that should not be scheduled for stop/start"
  value       = data.local_file.neptune_cluster_not_scheduled.content
}
