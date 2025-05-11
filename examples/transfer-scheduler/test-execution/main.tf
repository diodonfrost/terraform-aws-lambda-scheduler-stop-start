resource "null_resource" "wait_transfer_server_available_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_transfer_status.py ONLINE \
        ${var.transfer_server_to_scheduled_id} \
        ${var.transfer_server_not_scheduled_id}
    EOT
  }
}

resource "aws_lambda_invocation" "stop_transfer" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [null_resource.wait_transfer_server_available_state]
}

resource "null_resource" "wait_transfer_server_offline_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_transfer_status.py OFFLINE \
        ${var.transfer_server_to_scheduled_id} \
    EOT
  }
}

resource "null_resource" "transfer_server_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws transfer describe-server \
        --server-id ${var.transfer_server_to_scheduled_id} \
        --query 'Server.State' \
        --output text > ${path.module}/transfer_server_to_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_transfer_server_offline_state]
}

data "local_file" "transfer_server_to_scheduled" {
  filename = "${path.module}/transfer_server_to_scheduled.state"

  depends_on = [null_resource.transfer_server_to_scheduled]
}

resource "null_resource" "transfer_server_not_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws transfer describe-server \
        --server-id ${var.transfer_server_not_scheduled_id} \
        --query 'Server.State' \
        --output text > ${path.module}/transfer_server_not_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_transfer_server_offline_state]
}

data "local_file" "transfer_server_not_scheduled" {
  filename = "${path.module}/transfer_server_not_scheduled.state"

  depends_on = [null_resource.transfer_server_not_scheduled]
}
