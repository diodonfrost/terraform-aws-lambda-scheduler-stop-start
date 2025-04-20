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

resource "null_resource" "rds_aurora_cluster_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws rds describe-db-clusters \
        --db-cluster-identifier ${var.rds_aurora_cluster_to_scheduled_name} \
        --query 'DBClusters[0].Status' \
        --output text > ${path.module}/rds_aurora_cluster_to_scheduled.state
    EOT
  }

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "rds_aurora_cluster_to_scheduled" {
  filename = "${path.module}/rds_aurora_cluster_to_scheduled.state"

  depends_on = [null_resource.rds_aurora_cluster_to_scheduled]
}

resource "null_resource" "rds_mariadb_instance_to_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws rds describe-db-instances \
        --db-instance-identifier ${var.rds_mariadb_instance_to_scheduled_name} \
        --query 'DBInstances[0].DBInstanceStatus' \
        --output text > ${path.module}/rds_mariadb_instance_to_scheduled.state
    EOT
  }

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "rds_mariadb_instance_to_scheduled" {
  filename = "${path.module}/rds_mariadb_instance_to_scheduled.state"

  depends_on = [null_resource.rds_mariadb_instance_to_scheduled]
}

resource "null_resource" "rds_mysql_instance_to_not_scheduled" {
  provisioner "local-exec" {
    command = <<-EOT
      aws rds describe-db-instances \
        --db-instance-identifier ${var.rds_mysql_instance_to_not_scheduled_name} \
        --query 'DBInstances[0].DBInstanceStatus' \
        --output text > ${path.module}/rds_mysql_instance_to_not_scheduled.state
    EOT
  }

  depends_on = [time_sleep.after_stop_wait_60_seconds]
}

data "local_file" "rds_mysql_instance_to_not_scheduled" {
  filename = "${path.module}/rds_mysql_instance_to_not_scheduled.state"

  depends_on = [null_resource.rds_mysql_instance_to_not_scheduled]
}
