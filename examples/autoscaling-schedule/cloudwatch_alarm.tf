resource "aws_autoscaling_policy" "scheduled" {
  count                  = 3
  name                   = "bar-with-tag-${count.index}"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.scheduled[count.index].name
}

resource "aws_cloudwatch_metric_alarm" "scheduled" {
  count               = 3
  alarm_name          = "bar-with-tag-${count.index}"
  namespace           = "AWS/AutoScaling"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  period              = "60"
  statistic           = "Average"
  threshold           = "90"
  alarm_actions       = [aws_autoscaling_policy.scheduled[count.index].arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.scheduled[count.index].id
  }

  tags = {
    tostop = "true"
  }
}

resource "aws_autoscaling_policy" "not_scheduled" {
  count                  = 2
  name                   = "foo-without-tag-${count.index}"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.not_scheduled[count.index].name
}

resource "aws_cloudwatch_metric_alarm" "not_scheduled" {
  count               = 2
  alarm_name          = "foo-without-tag-${count.index}"
  namespace           = "AWS/AutoScaling"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  period              = "60"
  statistic           = "Average"
  threshold           = "90"
  alarm_actions       = [aws_autoscaling_policy.not_scheduled[count.index].arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.not_scheduled[count.index].id
  }

  tags = {
    tostop = "false"
  }
}
