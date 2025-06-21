data "aws_region" "current" {}

# Convert *.py to .zip because AWS Lambda need .zip
data "archive_file" "this" {
  type        = "zip"
  source_dir  = "${path.module}/package/"
  output_path = "${path.module}/aws-stop-start-resources.zip"
}

# Create Lambda function for stop or start aws resources
resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  source_code_hash = data.archive_file.this.output_base64sha256
  function_name    = var.name
  role             = var.custom_iam_role_arn == null ? aws_iam_role.this[0].arn : var.custom_iam_role_arn
  handler          = "scheduler.main.lambda_handler"
  runtime          = var.runtime
  timeout          = "600"
  kms_key_arn      = var.kms_key_arn == null ? "" : var.kms_key_arn

  environment {
    variables = {
      AWS_REGIONS                     = var.aws_regions == null ? data.aws_region.current.name : join(", ", var.aws_regions)
      SCHEDULE_ACTION                 = var.schedule_action
      TAG_KEY                         = local.scheduler_tag["key"]
      TAG_VALUE                       = local.scheduler_tag["value"]
      DOCUMENTDB_SCHEDULE             = tostring(var.documentdb_schedule)
      EC2_SCHEDULE                    = tostring(var.ec2_schedule)
      ECS_SCHEDULE                    = tostring(var.ecs_schedule)
      RDS_SCHEDULE                    = tostring(var.rds_schedule)
      REDSHIFT_SCHEDULE               = tostring(var.redshift_schedule)
      AUTOSCALING_SCHEDULE            = tostring(var.autoscaling_schedule)
      AUTOSCALING_TERMINATE_INSTANCES = tostring(var.autoscaling_terminate_instances)
      CLOUDWATCH_ALARM_SCHEDULE       = tostring(var.cloudwatch_alarm_schedule)
      TRANSFER_SCHEDULE               = tostring(var.transfer_schedule)
      SCHEDULER_EXCLUDED_DATES        = jsonencode(var.scheduler_excluded_dates)
    }
  }

  tags = var.tags
}

resource "aws_scheduler_schedule" "this" {
  name                         = "trigger-lambda-scheduler-${var.name}"
  description                  = "Trigger lambda scheduler"
  schedule_expression          = var.schedule_expression
  schedule_expression_timezone = var.schedule_expression_timezone

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.this.arn
    role_arn = aws_iam_role.scheduler_lambda.arn
  }
}
