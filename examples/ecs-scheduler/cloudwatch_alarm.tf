resource "aws_cloudwatch_metric_alarm" "service_count" {
  alarm_name          = "ecs-cluster-hello-service-count"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "SampleCount"
  threshold           = "2"
  alarm_description   = "Less than 2 Running Service on cluster"
  dimensions = {
    ClusterName = aws_ecs_cluster.hello.id
  }

  tags = {
    tostop = "true"
  }
}
