resource "time_sleep" "before_stop_wait_30_seconds" {
  create_duration = "30s"
}

resource "aws_lambda_invocation" "this" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [time_sleep.before_stop_wait_30_seconds]
}

resource "time_sleep" "after_stop_wait_60_seconds" {
  create_duration = "60s"

  depends_on = [aws_lambda_invocation.this]
}

data "aws_instance" "instance_1_to_scheduled_id" {
  instance_id = var.instance_1_to_scheduled_id

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "instance_2_to_scheduled_id" {
  instance_id = var.instance_2_to_scheduled_id

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "instance_3_to_scheduled_id" {
  instance_id = var.instance_3_to_scheduled_id

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "instance_1_not_to_scheduled_id" {
  instance_id = var.instance_1_not_to_scheduled_id

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "aws_instance" "instance_2_not_to_scheduled_id" {
  instance_id = var.instance_2_not_to_scheduled_id

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}
