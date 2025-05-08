resource "null_resource" "wait_documentdb_cluster_available_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_documentdb_status.py available \
        ${var.docdb_cluster_to_scheduled_name} \
        ${var.docdb_cluster_not_scheduled_name}
    EOT
  }
}

resource "aws_lambda_invocation" "stop_documentdb" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [null_resource.wait_documentdb_cluster_available_state]
}

resource "null_resource" "wait_documentdb_cluster_stopped_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_documentdb_status.py stopped \
        ${var.docdb_cluster_to_scheduled_name} \
    EOT
  }
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

  depends_on = [null_resource.wait_documentdb_cluster_stopped_state]
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

  depends_on = [null_resource.wait_documentdb_cluster_stopped_state]
}

data "local_file" "docdb_cluster_not_scheduled" {
  filename = "${path.module}/docdb_cluster_not_scheduled.state"

  depends_on = [null_resource.docdb_cluster_not_scheduled]
}
