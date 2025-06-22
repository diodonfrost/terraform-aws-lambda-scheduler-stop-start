resource "null_resource" "start_rds_aurora_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      TIMEOUT=600
      START_TIME=$(date +%s)

      echo "Waiting for rds aurora cluster ${var.rds_aurora_cluster_name} to reach 'stopped' state (timeout: $TIMEOUT seconds)..."

      while true; do
        # Check the current state of the rds aurora cluster
        CURRENT_STATE=$(aws rds describe-db-clusters --db-cluster-identifier ${var.rds_aurora_cluster_name} --query 'DBClusters[0].Status' --output text)

        # Get current elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))

        # Check if cluster is stopped
        if [ "$CURRENT_STATE" = "stopped" ]; then
          aws rds start-db-cluster --db-cluster-identifier ${var.rds_aurora_cluster_name}
          exit 0
        fi

        # Check if we've exceeded the timeout
        if [ $ELAPSED -ge $TIMEOUT ]; then
          echo "Timeout reached. rds aurora cluster did not reach 'stopped' state within $TIMEOUT seconds."
          exit 1
        fi

        # Wait 10 seconds before checking again
        echo "Current state: $CURRENT_STATE (elapsed: $ELAPSED seconds/ $TIMEOUT seconds)..."
        sleep 10
      done
    EOT
  }
}

resource "null_resource" "waiting_for_rds_aurora_cluster_to_start" {
  provisioner "local-exec" {
    command = <<-EOT
      TIMEOUT=600
      START_TIME=$(date +%s)

      echo "Waiting for rds aurora cluster ${var.rds_aurora_cluster_name} to reach 'available' state (timeout: $TIMEOUT seconds)..."

      while true; do
        # Check the current state of the rds aurora cluster
        CURRENT_STATE=$(aws rds describe-db-clusters --db-cluster-identifier ${var.rds_aurora_cluster_name} --query 'DBClusters[0].Status' --output text)

        # Get current elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))

        # Check if cluster is available
        if [ "$CURRENT_STATE" = "available" ]; then
          exit 0
        fi

        # Check if we've exceeded the timeout
        if [ $ELAPSED -ge $TIMEOUT ]; then
          echo "Timeout reached. rds aurora cluster did not reach 'available' state within $TIMEOUT seconds."
          exit 1
        fi

        # Wait 10 seconds before checking again
        echo "Current state: $CURRENT_STATE (elapsed: $ELAPSED seconds/ $TIMEOUT seconds)..."
        sleep 10
      done
    EOT
  }

  depends_on = [null_resource.start_rds_aurora_cluster]
}
