# terraform-aws-lambda-scheduler-stop-start

[![Build Status](https://api.travis-ci.org/diodonfrost/terraform-aws-lambda-scheduler-stop-start.svg?branch=master)](https://travis-ci.org/diodonfrost/terraform-aws-lambda-scheduler-stop-start)

Stop and start ec2, rds resources and autoscaling groups with lambda function.

## Terraform versions
For Terraform 0.12 use version v2.* of this module.

If you are using Terraform 0.11 you can use versions v1.*.

## Future version v3.*

*  Multi aws tags support (backward compatibility)
*  Terminate action for autoscaling group instance 
*  Python type hints

## Features

*   Aws lambda runtine Python 3.7
*   ec2 instances scheduling
*   spot instances scheduling
*   rds clusters scheduling
*   rds instances scheduling
*   autoscalings scheduling
*   Aws CloudWatch logs for lambda

### Caveats
You can't stop and start an [Amazon Spot instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-spot-instances-work.html) (only the Spot service can stop and start a Spot Instance), but you can reboot or terminate a Spot Instance. That why this module support only scheduler action `terminate` for spot instance.

## Usage

```hcl
module "stop_ec2_instance" {
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  name                           = "ec2_stop"
  cloudwatch_schedule_expression = "cron(0 0 ? * FRI *)"
  schedule_action                = "stop"
  autoscaling_schedule           = "false"
  spot_schedule                  = "terminate"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  resources_tag                  = {
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
  spot_schedule                  = "false"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
```

## Examples

*   [Autoscaling scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/autoscaling-schedule) - Create lambda functions to suspend autoscaling group with tag `tostop = true` and terminate its ec2 instances on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Spot scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/spot-schedule) - Create lambda functions to stop spot instance with tag `tostop = true` on Friday at 23:00 Gmt
*   [EC2 scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/ec2-schedule) - Create lambda functions to stop ec2 with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Rds aurora - mariadb scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/rds-schedule) - Create lambda functions to stop rds mariadb and aurora cluster with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [test fixture](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/test_fixture) - Deploy environment for testing module

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Define name to use for lambda function, cloudwatch event and iam role | string | n/a | yes |
| custom_iam_role_arn | Custom IAM role arn for the scheduling lambda | string | null | no |
| aws_regions | A list of one or more aws regions where the lambda will be apply, default use the current region | list | null | no |
| cloudwatch_schedule_expression | The scheduling expression | string | `"cron(0 22 ? * MON-FRI *)"` | yes |
| schedule_action | Define schedule action to apply on resources | string | `"stop"` | yes |
| resources_tag | Set the tag use for identify resources to stop or start | map | { tostop = "true" } | yes |
| autoscaling_schedule | Enable scheduling on autoscaling resources | string | `"false"` | no |
| spot_schedule | Enable scheduling on spot instance resources | string | `"false"` | no |
| ec2_schedule | Enable scheduling on ec2 instance resources | string | `"false"` | no |
| rds_schedule | Enable scheduling on rds resources | string | `"false"` | no |

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

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Tests

Some of these tests create real resources in an AWS account. That means they cost money to run, especially if you don't clean up after yourself. Please be considerate of the resources you create and take extra care to clean everything up when you're done!

In order to run tests that access your AWS account, you will need to configure your [AWS CLI
credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). For example, you could
set the credentials as the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Integration tests

Integration tests are realized with python `boto3` and `pytest` modules. 

Install Python dependency:

```shell
python3 -m pip install boto3 pytest pytest-cov pytest-xdist
```

```shell
# Test python code use by ec2 scheduler scheduler
python3 -m pytest -n 4 --cov=package tests/integration/test_ec2_scheduler.py

# Test python code use by spot scheduler scheduler
python3 -m pytest -n 2--cov=package tests/integration/test_spot_scheduler.py

# Test python code use by autoscaling scheduler
python3 -m pytest -n 4 --cov=package tests/integration/test_asg_scheduler.py

# Test python code use by rds scheduler
python3 -m pytest -n 8 --cov=package tests/integration/test_rds_scheduler.py

# Test all python code
python3 -m pytest -n 18 --cov=package tests/integration/
```

### End-to-end tests

This module has been packaged with [Terratest](https://github.com/gruntwork-io/terratest) to tests this Terraform module.

Install Terratest with depedencies:

```shell
# Prerequisite: install Go
go get ./...
```

```shell
# Test ec2 scheduler
go test -v tests/end-to-end/ec2_scheduler_test.go

# Test spot scheduler
go test -v tests/end-to-end/spot_scheduler_test.go

# Test autoscaling scheduler
go test -v tests/end-to-end/autoscaling_scheduler_test.go
```

## Authors

Modules managed by [diodonfrost](https://github.com/diodonfrost)

## Licence

Apache 2 Licensed. See LICENSE for full details.

## Resources

*   [cloudwatch schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
*   [Python boto3 ec2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
*   [Python boto3 rds](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
*   [Python boto3 autoscaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html)
*   [Terratest](https://github.com/gruntwork-io/terratest)
