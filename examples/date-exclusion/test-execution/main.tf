resource "null_resource" "wait_running_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_instances.py running \
        ${var.instance_1_to_scheduled_id} \
        ${var.instance_2_to_scheduled_id}
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

resource "null_resource" "wait_exclusion_check" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "Waiting for exclusion date verification..."
      sleep 30
    EOT
  }

  depends_on = [aws_lambda_invocation.this]
}

data "aws_instance" "instance_1_to_scheduled_id" {
  instance_id = var.instance_1_to_scheduled_id

  depends_on = [null_resource.wait_exclusion_check]
}

data "aws_instance" "instance_2_to_scheduled_id" {
  instance_id = var.instance_2_to_scheduled_id

  depends_on = [null_resource.wait_exclusion_check]
}

data "aws_instance" "instance_not_to_scheduled_id" {
  instance_id = var.instance_not_to_scheduled_id

  depends_on = [null_resource.wait_exclusion_check]
}
