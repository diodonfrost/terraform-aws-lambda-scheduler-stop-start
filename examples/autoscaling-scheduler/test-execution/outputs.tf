output "asg_scheduled_suspended_processes" {
  description = "The suspended processes of the scheduled autoscaling group"
  value       = data.aws_autoscaling_group.asg_scheduled.suspended_processes
}

output "asg_not_scheduled_suspended_processes" {
  description = "The suspended processes of the not scheduled autoscaling group"
  value       = data.aws_autoscaling_group.asg_not_scheduled.suspended_processes
}

output "asg_instance_scheduled_state" {
  description = "The state of the scheduled instance"
  value       = data.aws_instance.asg_scheduled.instance_state
}

output "asg_instance_not_scheduled_state" {
  description = "The state of the not scheduled instance"
  value       = data.aws_instance.asg_not_scheduled.instance_state
}
