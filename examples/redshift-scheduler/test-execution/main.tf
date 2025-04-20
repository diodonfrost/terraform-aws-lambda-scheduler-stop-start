resource "time_sleep" "before_stop_wait_240_seconds" {
  create_duration = "240s"
}

resource "aws_lambda_invocation" "stop_redshift" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [time_sleep.before_stop_wait_240_seconds]
}

resource "time_sleep" "after_stop_wait_60_seconds" {
  create_duration = "60s"

  depends_on = [aws_lambda_invocation.stop_redshift]
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

  depends_on = [time_sleep.after_stop_wait_60_seconds]
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

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "redshift_cluster_not_scheduled" {
  filename = "${path.module}/redshift_cluster_not_scheduled.state"

  depends_on = [null_resource.redshift_cluster_not_scheduled]
}
