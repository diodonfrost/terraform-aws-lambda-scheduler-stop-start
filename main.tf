# Freeze aws provider version
terraform {
  required_version = ">= 0.12"

  required_providers {
    aws     = ">= 2.9.0"
    archive = ">= 1.2.2"
  }
}

data "aws_region" "current" {}

################################################
#
#            IAM CONFIGURATION
#
################################################

resource "aws_iam_role" "this" {
  count              = var.custom_iam_role_arn == null ? 1 : 0
  name               = "${var.name}-scheduler-lambda"
  description        = "Allows Lambda functions to stop and start ec2 and rds resources"
  assume_role_policy = data.aws_iam_policy_document.this.json
  tags               = var.tags
}

data "aws_iam_policy_document" "this" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "autoscaling_group_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-autoscaling-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.autoscaling_group_scheduler.json
}

data "aws_iam_policy_document" "autoscaling_group_scheduler" {
  statement {
    actions = [
      "autoscaling:DescribeScalingProcessTypes",
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DescribeTags",
      "autoscaling:SuspendProcesses",
      "autoscaling:ResumeProcesses",
      "autoscaling:UpdateAutoScalingGroup",
      "autoscaling:DescribeAutoScalingInstances",
      "autoscaling:TerminateInstanceInAutoScalingGroup",
      "ec2:TerminateInstances",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "spot_instance_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-spot-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.spot_instance_scheduler.json
}

data "aws_iam_policy_document" "spot_instance_scheduler" {
  statement {
    actions = [
      "ec2:DescribeInstances",
      "ec2:TerminateSpotInstances",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "instance_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-ec2-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.instance_scheduler.json
}

data "aws_iam_policy_document" "instance_scheduler" {
  statement {
    actions = [
      "ec2:StopInstances",
      "ec2:StartInstances",
      "autoscaling:DescribeAutoScalingInstances",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "rds_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-rds-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.rds_scheduler.json
}

data "aws_iam_policy_document" "rds_scheduler" {
  statement {
    actions = [
      "rds:StartDBCluster",
      "rds:StopDBCluster",
      "rds:StartDBInstance",
      "rds:StopDBInstance",
      "rds:DescribeDBClusters",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "ecs_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-ecs-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.ecs_scheduler.json
}

## This should be scoped to the tagged resources ##
data "aws_iam_policy_document" "ecs_scheduler" {
  statement {
    actions = [
      "ecs:UpdateService",
      "ecs:DescribeService",
    ]

    resources = [
      "arn:aws:ecs:*:*:service/*",
    ]
    condition {
      test     = "StringEqual"
      variable = "aws:ResourceTag/${local.scheduler_tag["key"]}"
      values = [
        local.scheduler_tag["value"]
      ]
    }
  }
}

resource "aws_iam_role_policy" "cloudwatch_alarm_scheduler" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-cloudwatch-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.cloudwatch_alarm_scheduler.json
}

data "aws_iam_policy_document" "cloudwatch_alarm_scheduler" {
  statement {
    actions = [
      "cloudwatch:DisableAlarmActions",
      "cloudwatch:EnableAlarmActions",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "resource_groups_tagging_api" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-resource-groups-tagging-api-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.resource_groups_tagging_api.json
}

data "aws_iam_policy_document" "resource_groups_tagging_api" {
  statement {
    actions = [
      "tag:GetResources",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "lambda_logging" {
  count  = var.custom_iam_role_arn == null ? 1 : 0
  name   = "${var.name}-lambda-logging"
  role   = aws_iam_role.this[0].id
  policy = var.kms_key_arn == null ? jsonencode(local.lambda_logging_policy) : jsonencode(local.lambda_logging_and_kms_policy)
}

# Local variables are used for make iam policy because
# resources cannot have a null value in aws_iam_policy_document.
locals {
  lambda_logging_policy = {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "${aws_cloudwatch_log_group.this.arn}:*",
        "Effect" : "Allow"
      }
    ]
  }
  lambda_logging_and_kms_policy = {
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource" : "${aws_cloudwatch_log_group.this.arn}:*",
        "Effect" : "Allow"
      },
      {
        "Action" : [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:CreateGrant"
        ],
        "Resource" : var.kms_key_arn,
        "Effect" : "Allow"
      }
    ]
  }
  # Backward compatibility with the former scheduler variable name.
  scheduler_tag = var.resources_tag == null ? var.scheduler_tag : var.resources_tag
}

################################################
#
#            LAMBDA FUNCTION
#
################################################

# Convert *.py to .zip because AWS Lambda need .zip
data "archive_file" "this" {
  type        = "zip"
  source_dir  = "${path.module}/package/"
  output_path = "${path.module}/aws-stop-start-resources-3.1.3.zip" # The version should match with the latest git tag
}

# Create Lambda function for stop or start aws resources
resource "aws_lambda_function" "this" {
  filename      = data.archive_file.this.output_path
  function_name = var.name
  role          = var.custom_iam_role_arn == null ? aws_iam_role.this[0].arn : var.custom_iam_role_arn
  handler       = "scheduler.main.lambda_handler"
  runtime       = "python3.7"
  timeout       = "600"
  kms_key_arn   = var.kms_key_arn == null ? "" : var.kms_key_arn

  environment {
    variables = {
      AWS_REGIONS               = var.aws_regions == null ? data.aws_region.current.name : join(", ", var.aws_regions)
      SCHEDULE_ACTION           = var.schedule_action
      TAG_KEY                   = local.scheduler_tag["key"]
      TAG_VALUE                 = local.scheduler_tag["value"]
      EC2_SCHEDULE              = tostring(var.ec2_schedule)
      ECS_SCHEDULE              = tostring(var.ecs_schedule)
      RDS_SCHEDULE              = tostring(var.rds_schedule)
      AUTOSCALING_SCHEDULE      = tostring(var.autoscaling_schedule)
      CLOUDWATCH_ALARM_SCHEDULE = tostring(var.cloudwatch_alarm_schedule)
    }
  }

  tags = var.tags
}

################################################
#
#            CLOUDWATCH EVENT
#
################################################

resource "aws_cloudwatch_event_rule" "this" {
  name                = "trigger-lambda-scheduler-${var.name}"
  description         = "Trigger lambda scheduler"
  schedule_expression = var.cloudwatch_schedule_expression
  tags                = var.tags
}

resource "aws_cloudwatch_event_target" "this" {
  arn  = aws_lambda_function.this.arn
  rule = aws_cloudwatch_event_rule.this.name
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.this.function_name
  source_arn    = aws_cloudwatch_event_rule.this.arn
}

################################################
#
#            CLOUDWATCH LOG
#
################################################
resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 14
  tags              = var.tags
}
