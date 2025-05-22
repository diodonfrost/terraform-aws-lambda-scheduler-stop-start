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
  count  = var.custom_iam_role_arn == null && (var.autoscaling_schedule == true || var.autoscaling_terminate_instances == true) ? 1 : 0
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
  count  = var.custom_iam_role_arn == null && var.ec2_schedule == true ? 1 : 0
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
  count  = var.custom_iam_role_arn == null && var.ec2_schedule == true ? 1 : 0
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
  count  = var.custom_iam_role_arn == null && var.rds_schedule == true ? 1 : 0
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
  count  = var.custom_iam_role_arn == null && var.ecs_schedule == true ? 1 : 0
  name   = "${var.name}-ecs-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.ecs_scheduler.json
}

data "aws_iam_policy_document" "ecs_scheduler" {
  statement {
    actions = [
      "ecs:UpdateService",
      "ecs:DescribeService",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "redshift_scheduler" {
  count  = var.custom_iam_role_arn == null && var.redshift_schedule == true ? 1 : 0
  name   = "${var.name}-redshift-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.redshift_scheduler.json
}

data "aws_iam_policy_document" "redshift_scheduler" {
  statement {
    actions = [
      "redshift:ResumeCluster",
      "redshift:PauseCluster",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "cloudwatch_alarm_scheduler" {
  count  = var.custom_iam_role_arn == null && var.cloudwatch_alarm_schedule == true ? 1 : 0
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
  policy = data.aws_iam_policy_document.lambda_logging_policy.json
}

data "aws_iam_policy_document" "lambda_logging_policy" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "${aws_cloudwatch_log_group.this.arn}:*"
    ]
    effect = "Allow"
  }

  dynamic "statement" {
    for_each = var.kms_key_arn == null ? [] : [var.kms_key_arn]
    content {
      actions = [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:CreateGrant"
      ]
      resources = [statement.value]
      effect    = "Allow"
    }
  }
}

locals {
  # Backward compatibility with the former scheduler variable name.
  scheduler_tag = var.resources_tag == null ? var.scheduler_tag : var.resources_tag
}

resource "aws_iam_role" "scheduler_lambda" {
  name               = "${var.name}-scheduler-lambda-role"
  description        = "Allows Lambda functions to invoke ${var.name} lambda function"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume_role_policy.json
  tags               = var.tags
}

resource "aws_iam_role_policy_attachment" "scheduler_lambda" {
  role       = aws_iam_role.scheduler_lambda.name
  policy_arn = aws_iam_policy.scheduler_lambda.arn
}

data "aws_iam_policy_document" "scheduler_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "scheduler_lambda" {
  name = "${var.name}-Scheduler-Lambda-Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Action" : [
          "lambda:InvokeFunction"
        ],
        Effect   = "Allow"
        Resource = aws_lambda_function.this.arn
      },
    ]
  })
}

resource "aws_iam_role_policy" "transfer_scheduler" {
  count  = var.custom_iam_role_arn == null && var.transfer_schedule == true ? 1 : 0
  name   = "${var.name}-transfer-custom-policy-scheduler"
  role   = aws_iam_role.this[0].id
  policy = data.aws_iam_policy_document.transfer_scheduler.json
}

data "aws_iam_policy_document" "transfer_scheduler" {
  statement {
    actions = [
      "transfer:StartServer",
      "transfer:StopServer",
      "transfer:ListServers",
      "transfer:DescribeServer"
    ]

    resources = [
      "*",
    ]
  }
}
