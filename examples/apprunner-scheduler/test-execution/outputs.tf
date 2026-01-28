output "service_scheduled_status" {
  description = "Status of the App Runner service to be scheduled"
  value       = data.external.service_to_scheduled_status.result.status
}

output "service_not_scheduled_status" {
  description = "Status of the App Runner service not to be scheduled"
  value       = data.external.service_not_to_scheduled_status.result.status
}
