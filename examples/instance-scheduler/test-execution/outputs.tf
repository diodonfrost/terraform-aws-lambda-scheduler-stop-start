output "instance_1_scheduled_state" {
  description = "State of the first instance to be scheduled"
  value       = data.aws_instance.instance_1_to_scheduled_id.instance_state
}

output "instance_2_scheduled_state" {
  description = "State of the second instance to be scheduled"
  value       = data.aws_instance.instance_2_to_scheduled_id.instance_state
}

output "instance_3_scheduled_state" {
  description = "State of the third instance to be scheduled"
  value       = data.aws_instance.instance_3_to_scheduled_id.instance_state
}

output "instance_1_not_scheduled_state" {
  description = "State of the first instance not to be scheduled"
  value       = data.aws_instance.instance_1_not_to_scheduled_id.instance_state
}

output "instance_2_not_scheduled_state" {
  description = "State of the second instance not to be scheduled"
  value       = data.aws_instance.instance_2_not_to_scheduled_id.instance_state
}
