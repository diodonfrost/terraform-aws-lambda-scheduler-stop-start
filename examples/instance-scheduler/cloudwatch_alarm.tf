resource "aws_cloudwatch_metric_alarm" "scheduled" {
  count               = 3
  alarm_name          = "instance-scheduled-autorecovery-${count.index}"
  namespace           = "AWS/EC2"
  evaluation_periods  = "2"
  period              = "60"
  alarm_description   = "This metric auto recovers EC2 instances"
  alarm_actions       = ["arn:aws:automate:${data.aws_region.current.name}:ec2:reboot"]
  statistic           = "Minimum"
  comparison_operator = "GreaterThanThreshold"
  threshold           = "0.0"
  metric_name         = "StatusCheckFailed_Instance"
  dimensions = {
    InstanceId = aws_instance.scheduled[count.index].id
  }

  tags = {
    tostop = "true"
  }
}


resource "aws_cloudwatch_metric_alarm" "not_scheduled" {
  count               = 2
  alarm_name          = "instance-not-scheduled-autorecovery-${count.index}"
  namespace           = "AWS/EC2"
  evaluation_periods  = "2"
  period              = "60"
  alarm_description   = "This metric auto recovers EC2 instances"
  alarm_actions       = ["arn:aws:automate:${data.aws_region.current.name}:ec2:reboot"]
  statistic           = "Minimum"
  comparison_operator = "GreaterThanThreshold"
  threshold           = "0.0"
  metric_name         = "StatusCheckFailed_Instance"
  dimensions = {
    InstanceId = aws_instance.not_scheduled[count.index].id
  }

  tags = {
    tostop = "false"
  }
}
