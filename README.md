# terraform-aws-lambda-scheduler-stop-start

[![CI](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/workflows/CI/badge.svg)](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/actions)

Stop and start instance, rds resources and autoscaling groups with lambda function.

## Terraform versions
For Terraform 0.15 use version v3.* of this module.

If you are using Terraform 0.11 you can use versions v1.*.

## Features

*  Aws lambda runtine Python 3.7
*  ec2 instances scheduling
*  ecs service scheduling
*  rds clusters scheduling
*  rds instances scheduling
*  autoscalings scheduling
*  cloudwatch alarm scheduling
*  Aws CloudWatch logs for lambda

## Usage

```hcl
module "stop_ec2_instance" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "ec2_stop"
  cloudwatch_schedule_expression = "cron(0 0 ? * FRI *)"
  schedule_action                = "stop"
  autoscaling_schedule           = "false"
  ec2_schedule                   = "true"
  ecs_schedule                   = "false"
  rds_schedule                   = "false"
  cloudwatch_alarm_schedule      = "false"
  scheduler_tag                  = {
    key   = "tostop"
    value = "true"
  }
}

module "start_ec2_instance" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "ec2_start"
  cloudwatch_schedule_expression = "cron(0 8 ? * MON *)"
  schedule_action                = "start"
  autoscaling_schedule           = "false"
  ec2_schedule                   = "true"
  ecs_schedule                   = "false"
  rds_schedule                   = "false"
  cloudwatch_alarm_schedule      = "false"
  scheduler_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
```

## Examples

*   [Autoscaling scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/autoscaling-scheduler) - Create lambda functions to suspend autoscaling group with tag `tostop = true` and terminate its ec2 instances on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [EC2 scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/ec2-scheduler) - Create lambda functions to stop ec2 with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Rds aurora - mariadb scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/rds-scheduler) - Create lambda functions to stop rds mariadb and aurora cluster with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [test fixture](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/test_fixture) - Deploy environment for testing module

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Define name to use for lambda function, cloudwatch event and iam role | string | n/a | yes |
| custom_iam_role_arn | Custom IAM role arn for the scheduling lambda | string | null | no |
| tags | Custom tags on aws resources | map | null | no |
| kms_key_arn | The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key | string | null | no |
| aws_regions | A list of one or more aws regions where the lambda will be apply, default use the current region | list | null | no |
| cloudwatch_schedule_expression | The scheduling expression | string | `"cron(0 22 ? * MON-FRI *)"` | yes |
| autoscaling_schedule | Enable scheduling on autoscaling resources | string | `"false"` | no |
| ec2_schedule | Enable scheduling on ec2 instance resources | string | `"false"` | no |
| ecs_schedule | Enable scheduling on ecs services resources | string | `"false"` | no |
| rds_schedule | Enable scheduling on rds resources | string | `"false"` | no |
| cloudwatch_alarm_schedule | Enable scheduleding on cloudwatch alarm resources | string | `"false"` | no |
| schedule_action | Define schedule action to apply on resources | string | `"stop"` | yes |
| scheduler_tag | Set the tag to use for identify aws resources to stop or start | map | {"key" = "tostop", "value" = "true"} | yes |

## Outputs

| Name | Description |
|------|-------------|
| lambda_iam_role_arn | The ARN of the IAM role used by Lambda function |
| lambda_iam_role_name | The name of the IAM role used by Lambda function |
| scheduler_lambda_arn | The ARN of the Lambda function |
| scheduler_lambda_name | The name of the Lambda function |
| scheduler_lambda_invoke_arn | The ARN to be used for invoking Lambda function from API Gateway |
| scheduler_lambda_function_last_modified | The date Lambda function was last modified |
| scheduler_lambda_function_version | Latest published version of your Lambda function |
| scheduler_log_group_name | The name of the scheduler log group |
| scheduler_log_group_arn | The Amazon Resource Name (ARN) specifying the log group |

## Tests

Some of these tests create real resources in an AWS account. That means they cost money to run, especially if you don't clean up after yourself. Please be considerate of the resources you create and take extra care to clean everything up when you're done!

In order to run tests that access your AWS account, you will need to configure your [AWS CLI
credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). For example, you could
set the credentials as the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Integration tests

Integration tests are realized with python `boto3` and `pytest` modules.

Install Python dependency:

```shell
python3 -m pip install -r requirements-dev.txt
```

```shell
# Test python code use by instance scheduler scheduler
python3 -m pytest -n 4 --cov=package tests/integration/test_instance_scheduler.py

# Test python code use by autoscaling scheduler
python3 -m pytest -n 4 --cov=package tests/integration/test_asg_scheduler.py

# Test python code use by rds scheduler
python3 -m pytest -n 8 --cov=package tests/integration/test_rds_scheduler.py

# Test pythn code use by cloudwatch alarm scheduler
python3 -m pytest -n 12 --cov=package tests/integration/test_cloudwatch_alarm_scheduler.py

# Test all python code
python3 -m pytest -n 30 --cov=package tests/integration/
```

### End-to-end tests

This module has been packaged with [Terratest](https://github.com/gruntwork-io/terratest) to tests this Terraform module.

Install Terratest with depedencies:

```shell
# Prerequisite: install Go
go get ./...
```

```shell
# Test instance scheduler
go test -timeout 900s -v tests/end-to-end/instance_scheduler_test.go

# Test autoscaling scheduler
go test -timeout 900s -v tests/end-to-end/autoscaling_scheduler_test.go
```

## Authors

Modules managed by [diodonfrost](https://github.com/diodonfrost)

## Licence

Apache 2 Licensed. See LICENSE for full details.

## Resources

*   [cloudwatch schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
*   [Python boto3 ec2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
*   [Python boto3 ecs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html)
*   [Python boto3 rds](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
*   [Python boto3 autoscaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html)
*   [Terratest](https://github.com/gruntwork-io/terratest)
