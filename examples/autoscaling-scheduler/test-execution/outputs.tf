output "asg_scheduled_suspended_processes" {
  value = data.aws_autoscaling_group.asg_scheduled.suspended_processes
}

output "asg_not_scheduled_suspended_processes" {
  value = data.aws_autoscaling_group.asg_not_scheduled.suspended_processes
}

output "asg_instance_scheduled_state" {
  value = data.aws_instance.asg_scheduled.instance_state
}

output "asg_instance_not_scheduled_state" {
  value = data.aws_instance.asg_not_scheduled.instance_state
}
