# terraform-aws-lambda-scheduler-stop-start

Terraform module which create lambda scheduler for stop and start resources on AWS

## Features

* Aws lambda runtine Python 3.6
* ec2 instance scheduling
* rds aurora scheduling
* rds instance scheduling

## Usage
```hcl
module "lambda_scheduler_stop_start" {
  cloudwatch_schedule_expression = "cron(0 00 ? * FRI *)"
  source                         = "diodonfrost/lambda-scheduler-stop-start/aws"
  schedule_action                = "stop"
  ec2_schedule                   = "true"
  rds_schedule                   = "true"
  autoscaling_schedule           = "true"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
```

## Examples

* [EC2 scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/ec2-schedule) - Create lamnda functions to stop ec2 with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
* [Rds aurora - mariadb scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/rds-schedule) - Create lamnda functions to stop rds mariadb and aurora cluster with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
* [Autoscaling scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/autoscaling-schedule) - Create lamnda functions to suspend autoscaling group and stop ec2 instances in it with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT


<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| name | Define name to use for lambda function, cloudwatch event and iam role | string | n/a | yes |
| cloudwatch_schedule_expression | The scheduling expression | string | `"cron(0 22 ? * MON-FRI *)"` | yes |
| schedule_action | Define schedule action to apply on resources | string | `"stop"` | yes |
| resources_tag | Set the tag use for identify resources to stop or start | map | { tostop = "true" } | yes |
| ec2_schedule | Enable scheduling on ec2 resources | string | `"false"` | no |
| rds_schedule | Enable scheduling on rds resources | string | `"false"` | no |
| autoscaling_schedule | Enable scheduling on autoscaling resources | string | `"false"` | no |

## Outputs

| Name | Description |
|------|-------------|
| scheduler_lambda_arn | The Amazon Resource Name (ARN) identifying your Lambda Function |
| lambda_iam_role_name | The name of the IAM role used by Lambda function |
| scheduler_lambda_arn | The ARN of the Lambda function |
| scheduler_function_name | The name of the Lambda function |
| scheduler_lambda_invoke_arn | The ARN to be used for invoking Lambda function from API Gateway |
| scheduler_lambda_function_last_modified | The date Lambda function was last modified |
| scheduler_lambda_function_version | Latest published version of your Lambda function |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Authors

Modules managed by [diodonfrost](https://github.com/diodonfrost)

## Licence

Apache 2 Licensed. See LICENSE for full details.

## Resources

* [cloudwatch schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
* [Python boto3 ec2](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
* [Python boto3 rds](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
* [Python boto3 autoscaling](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html)
