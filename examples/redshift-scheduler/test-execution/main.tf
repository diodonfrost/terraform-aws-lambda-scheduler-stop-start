resource "null_resource" "wait_redshift_cluster_available_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_redshift_status.py Available \
        ${var.redshift_cluster_to_scheduled_name} \
        ${var.redshift_cluster_not_scheduled_name}
    EOT
  }
}

resource "aws_lambda_invocation" "stop_redshift" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [null_resource.wait_redshift_cluster_available_state]
}

resource "null_resource" "wait_redshift_cluster_paused_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_redshift_status.py Paused \
        ${var.redshift_cluster_to_scheduled_name} \
    EOT
  }
}

resource "null_resource" "redshift_cluster_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws redshift describe-clusters \
        --cluster-identifier ${var.redshift_cluster_to_scheduled_name} \
        --query 'Clusters[0].ClusterStatus' \
        --output text > ${path.module}/redshift_cluster_to_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_redshift_cluster_paused_state]
}

data "local_file" "redshift_cluster_to_scheduled" {
  filename = "${path.module}/redshift_cluster_to_scheduled.state"

  depends_on = [null_resource.redshift_cluster_to_scheduled]
}

resource "null_resource" "redshift_cluster_not_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws redshift describe-clusters \
        --cluster-identifier ${var.redshift_cluster_not_scheduled_name} \
        --query 'Clusters[0].ClusterStatus' \
        --output text > ${path.module}/redshift_cluster_not_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_redshift_cluster_paused_state]
}

data "local_file" "redshift_cluster_not_scheduled" {
  filename = "${path.module}/redshift_cluster_not_scheduled.state"

  depends_on = [null_resource.redshift_cluster_not_scheduled]
}
