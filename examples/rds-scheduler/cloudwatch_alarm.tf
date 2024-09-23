resource "aws_cloudwatch_metric_alarm" "aurora_scheduled_cpu" {
  alarm_name          = "aurora-cluster-with-tag-highCPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "60"
  statistic           = "Average"
  threshold           = "90"
  alarm_description   = "Average database CPU utilization is too high."
  dimensions = {
    DBClusterIdentifier = aws_rds_cluster.aurora_scheduled.id
  }

  tags = {
    tostop = "true"
  }
}

resource "aws_cloudwatch_metric_alarm" "mariadb_scheduled_cpu" {
  alarm_name          = "mariadbwithtag-highCPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "60"
  statistic           = "Average"
  threshold           = "90"
  alarm_description   = "Average database CPU utilization is too high."
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.mariadb_scheduled.id
  }

  tags = {
    tostop = "true"
  }
}

resource "aws_cloudwatch_metric_alarm" "mysql_not_scheduled_cpu" {
  alarm_name          = "mysqlwithouttag-highCPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "60"
  statistic           = "Average"
  threshold           = "90"
  alarm_description   = "Average database CPU utilization is too high."
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.mysql_not_scheduled.id
  }

  tags = {
    tostop = "false"
  }
}
