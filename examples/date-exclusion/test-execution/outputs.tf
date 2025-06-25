output "instance_1_scheduled_state" {
  description = "State of instance 1 after scheduler execution"
  value       = data.aws_instance.instance_1_to_scheduled_id.instance_state
}

output "instance_2_scheduled_state" {
  description = "State of instance 2 after scheduler execution"
  value       = data.aws_instance.instance_2_to_scheduled_id.instance_state
}

output "instance_not_scheduled_state" {
  description = "State of instance not scheduled after scheduler execution"
  value       = data.aws_instance.instance_not_to_scheduled_id.instance_state
}
