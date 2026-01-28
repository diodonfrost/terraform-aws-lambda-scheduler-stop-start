resource "null_resource" "wait_running_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_apprunner.py RUNNING \
        ${var.service_to_scheduled_arn}
    EOT
  }
}

resource "aws_lambda_invocation" "this" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [null_resource.wait_running_state]
}

resource "null_resource" "wait_paused_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_apprunner.py PAUSED \
        ${var.service_to_scheduled_arn}
    EOT
  }

  depends_on = [aws_lambda_invocation.this]
}

data "external" "service_to_scheduled_status" {
  program = ["python3", "${path.module}/get_apprunner_status.py"]

  query = {
    service_arn = var.service_to_scheduled_arn
  }

  depends_on = [null_resource.wait_paused_state]
}

data "external" "service_not_to_scheduled_status" {
  program = ["python3", "${path.module}/get_apprunner_status.py"]

  query = {
    service_arn = var.service_not_to_scheduled_arn
  }

  depends_on = [null_resource.wait_paused_state]
}
