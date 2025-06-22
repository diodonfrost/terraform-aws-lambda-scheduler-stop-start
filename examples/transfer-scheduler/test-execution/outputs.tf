output "transfer_server_to_scheduled_state" {
  description = "State of the Transfer server that should be stopped"
  value       = data.local_file.transfer_server_to_scheduled.content
}

output "transfer_server_not_scheduled_state" {
  description = "State of the Transfer server that should not be stopped"
  value       = data.local_file.transfer_server_not_scheduled.content
}
