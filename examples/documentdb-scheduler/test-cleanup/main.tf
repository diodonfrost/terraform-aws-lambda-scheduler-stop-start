resource "null_resource" "start_docdb_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      TIMEOUT=600
      START_TIME=$(date +%s)
      
      echo "Waiting for DocumentDB cluster ${var.docdb_cluster_name} to reach 'stopped' state (timeout: $TIMEOUT seconds)..."
      
      while true; do
        # Check the current state of the DocumentDB cluster
        CURRENT_STATE=$(aws docdb describe-db-clusters --db-cluster-identifier ${var.docdb_cluster_name} --query 'DBClusters[0].Status' --output text)
        
        # Get current elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        
        # Check if cluster is stopped
        if [ "$CURRENT_STATE" = "stopped" ]; then
          aws docdb start-db-cluster --db-cluster-identifier ${var.docdb_cluster_name}
          exit 0
        fi
        
        # Check if we've exceeded the timeout
        if [ $ELAPSED -ge $TIMEOUT ]; then
          echo "Timeout reached. DocumentDB cluster did not reach 'stopped' state within $TIMEOUT seconds."
          exit 1
        fi
        
        # Wait 10 seconds before checking again
        echo "Current state: $CURRENT_STATE (elapsed: $ELAPSED seconds/ $TIMEOUT seconds)..."
        sleep 10
      done
    EOT
  }
}

resource "null_resource" "waiting_for_docdb_cluster_to_start" {
  provisioner "local-exec" {
    command = <<-EOT
      TIMEOUT=600
      START_TIME=$(date +%s)
      
      echo "Waiting for DocumentDB cluster ${var.docdb_cluster_name} to reach 'available' state (timeout: $TIMEOUT seconds)..."
      
      while true; do
        # Check the current state of the DocumentDB cluster
        CURRENT_STATE=$(aws docdb describe-db-clusters --db-cluster-identifier ${var.docdb_cluster_name} --query 'DBClusters[0].Status' --output text)
        
        # Get current elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        
        # Check if cluster is available
        if [ "$CURRENT_STATE" = "available" ]; then
          exit 0
        fi
        
        # Check if we've exceeded the timeout
        if [ $ELAPSED -ge $TIMEOUT ]; then
          echo "Timeout reached. DocumentDB cluster did not reach 'available' state within $TIMEOUT seconds."
          exit 1
        fi
        
        # Wait 10 seconds before checking again
        echo "Current state: $CURRENT_STATE (elapsed: $ELAPSED seconds/ $TIMEOUT seconds)..."
        sleep 10
      done
    EOT
  }

  depends_on = [null_resource.start_docdb_cluster]
}
