resource "time_sleep" "before_stop_wait_30_seconds" {
  create_duration = "30s"
}

resource "aws_lambda_invocation" "stop_documentdb" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [time_sleep.before_stop_wait_30_seconds]
}

resource "time_sleep" "after_stop_wait_60_seconds" {
  create_duration = "60s"

  depends_on = [aws_lambda_invocation.stop_documentdb]
}

resource "null_resource" "docdb_cluster_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws docdb describe-db-clusters \
        --db-cluster-identifier ${var.docdb_cluster_to_scheduled_name} \
        --query 'DBClusters[0].Status' \
        --output text > ${path.module}/docdb_cluster_to_scheduled.state
    EOT
  }

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "docdb_cluster_to_scheduled" {
  filename = "${path.module}/docdb_cluster_to_scheduled.state"

  depends_on = [null_resource.docdb_cluster_to_scheduled]
}

resource "null_resource" "docdb_cluster_not_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws docdb describe-db-clusters \
        --db-cluster-identifier ${var.docdb_cluster_not_scheduled_name} \
        --query 'DBClusters[0].Status' \
        --output text > ${path.module}/docdb_cluster_not_scheduled.state
    EOT
  }

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "docdb_cluster_not_scheduled" {
  filename = "${path.module}/docdb_cluster_not_scheduled.state"

  depends_on = [null_resource.docdb_cluster_not_scheduled]
}
