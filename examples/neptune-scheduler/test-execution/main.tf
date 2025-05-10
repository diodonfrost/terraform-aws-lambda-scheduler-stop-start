resource "null_resource" "wait_neptune_cluster_available_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_neptune_status.py available \
        ${var.neptune_cluster_to_scheduled_name} \
        ${var.neptune_cluster_not_scheduled_name}
    EOT
  }
}

resource "aws_lambda_invocation" "stop_neptune" {
  function_name = var.lambda_stop_name

  input = jsonencode({
    key1 = "value1"
    key2 = "value2"
  })

  depends_on = [null_resource.wait_neptune_cluster_available_state]
}

resource "null_resource" "wait_neptune_cluster_stopped_state" {
  provisioner "local-exec" {
    command = <<-EOT
      python3 ${path.module}/wait_neptune_status.py stopped \
        ${var.neptune_cluster_to_scheduled_name}
    EOT
  }
}

resource "null_resource" "neptune_cluster_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws neptune describe-db-clusters \
        --db-cluster-identifier ${var.neptune_cluster_to_scheduled_name} \
        --query 'DBClusters[0].Status' \
        --output text > ${path.module}/neptune_cluster_to_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_neptune_cluster_stopped_state]
}

data "local_file" "neptune_cluster_to_scheduled" {
  filename = "${path.module}/neptune_cluster_to_scheduled.state"

  depends_on = [null_resource.neptune_cluster_to_scheduled]
}

resource "null_resource" "neptune_cluster_not_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws neptune describe-db-clusters \
        --db-cluster-identifier ${var.neptune_cluster_not_scheduled_name} \
        --query 'DBClusters[0].Status' \
        --output text > ${path.module}/neptune_cluster_not_scheduled.state
    EOT
  }

  depends_on = [null_resource.wait_neptune_cluster_stopped_state]
}

data "local_file" "neptune_cluster_not_scheduled" {
  filename = "${path.module}/neptune_cluster_not_scheduled.state"

  depends_on = [null_resource.neptune_cluster_not_scheduled]
} 