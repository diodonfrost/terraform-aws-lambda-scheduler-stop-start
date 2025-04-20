resource "null_resource" "start_docdb_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      TIMEOUT=600
      START_TIME=$(date +%s)
      
      echo "Waiting for Redshift cluster ${var.redshift_cluster_name} to reach 'stopped' state (timeout: $TIMEOUT seconds)..."
      
      while true; do
        # Check the current state of the DocumentDB cluster
        CURRENT_STATE=$(aws redshift describe-clusters --cluster-identifier ${var.redshift_cluster_name} --query 'Clusters[0].ClusterStatus' --output text)
        
        # Get current elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        
        # Check if cluster is paused
        if [ "$CURRENT_STATE" = "paused" ]; then
          aws redshift start-cluster --cluster-identifier ${var.redshift_cluster_name}
          exit 0
        fi
        
        # Check if we've exceeded the timeout
        if [ $ELAPSED -ge $TIMEOUT ]; then
          echo "Timeout reached. Redshift cluster did not reach 'paused' state within $TIMEOUT seconds."
          exit 1
        fi
        
        # Wait 10 seconds before checking again
        echo "Current state: $CURRENT_STATE (elapsed: $ELAPSED seconds/ $TIMEOUT seconds)..."
        sleep 10
      done
    EOT
  }
}
