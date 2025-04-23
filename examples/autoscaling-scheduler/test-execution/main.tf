resource "time_sleep" "before_stop_wait_60_seconds" {
  create_duration = "60s"
}

resource "aws_lambda_invocation" "this" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [time_sleep.before_stop_wait_60_seconds]
}

resource "time_sleep" "after_stop_wait_60_seconds" {
  create_duration = "60s"

  depends_on = [aws_lambda_invocation.this]
}

data "aws_autoscaling_group" "asg_scheduled" {
  name = var.asg_scheduled_name

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_autoscaling_group" "asg_not_scheduled" {
  name = var.asg_not_scheduled_name

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instances" "asg_scheduled" {
  instance_tags = {
    "aws:autoscaling:groupName" = var.asg_scheduled_name
  }
  instance_state_names = [
    "running",
    "shutting-down",
    "stopped",
    "stopping",
  ]
  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "asg_scheduled" {
  instance_id = data.aws_instances.asg_scheduled.ids[0]
}

data "aws_instances" "asg_not_scheduled" {
  instance_tags = {
    "aws:autoscaling:groupName" = var.asg_not_scheduled_name
  }
  instance_state_names = [
    "running",
    "shutting-down",
    "stopped",
    "stopping",
  ]

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "asg_not_scheduled" {
  instance_id = data.aws_instances.asg_not_scheduled.ids[0]
}
