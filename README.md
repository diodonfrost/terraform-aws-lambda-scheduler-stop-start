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
*  redshift clusters scheduling
*  documentdb clusters scheduling
*  autoscalings scheduling
*  cloudwatch alarm scheduling
*  Aws CloudWatch logs for lambda
*  Aws Transfer scheduling

## Usage

```hcl
module "stop_ec2_instance" {
  source  = "diodonfrost/lambda-scheduler-stop-start/aws"
  version = "x.x.x"

  name                      = "ec2_stop"
  schedule_expression       = "cron(0 0 ? * FRI *)"
  schedule_action           = "stop"
  autoscaling_schedule      = "false"
  documendb_schedule        = "false"
  ec2_schedule              = "true"
  ecs_schedule              = "false"
  rds_schedule              = "false"
  redshift_schedule         = "false"
  cloudwatch_alarm_schedule = "false"
  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "start_ec2_instance" {
  source  = "diodonfrost/lambda-scheduler-stop-start/aws"
  version = "x.x.x"

  name                      = "ec2_start"
  schedule_expression       = "cron(0 8 ? * MON *)"
  schedule_action           = "start"
  autoscaling_schedule      = "false"
  documendb_schedule        = "false"
  ec2_schedule              = "true"
  ecs_schedule              = "false"
  rds_schedule              = "false"
  redshift_schedule         = "false"
  cloudwatch_alarm_schedule = "false"
  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
```

## Examples

*   [Autoscaling scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/autoscaling-scheduler) - Create lambda functions to suspend autoscaling group with tag `tostop = true` and terminate its ec2 instances on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Documentdb scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/documentdb-scheduler) - Create lambda functions to stop documentdb cluster with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Instance scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/instance-scheduler) - Create lambda functions to stop ec2 with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [Rds aurora - mariadb scheduler](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/rds-scheduler) - Create lambda functions to stop rds mariadb and aurora cluster with tag `tostop = true` on Friday at 23:00 Gmt and start them on Monday at 07:00 GMT
*   [test fixture](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/tree/master/examples/test_fixture) - Deploy environment for testing module

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_archive"></a> [archive](#requirement\_archive) | 2.3.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.94.1 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.3.0 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 5.94.1 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_iam_policy.scheduler_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.scheduler_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.autoscaling_group_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.cloudwatch_alarm_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.ecs_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.lambda_logging](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.rds_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.redshift_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.resource_groups_tagging_api](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.spot_instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.transfer_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy_attachment.scheduler_lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_scheduler_schedule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/scheduler_schedule) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/2.3.0/docs/data-sources/file) | data source |
| [aws_iam_policy_document.autoscaling_group_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.cloudwatch_alarm_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.lambda_logging_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.rds_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.redshift_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.resource_groups_tagging_api](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.scheduler_assume_role_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.spot_instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.transfer_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_autoscaling_schedule"></a> [autoscaling\_schedule](#input\_autoscaling\_schedule) | Enable scheduling on autoscaling resources | `bool` | `false` | no |
| <a name="input_autoscaling_terminate_instances"></a> [autoscaling\_terminate\_instances](#input\_autoscaling\_terminate\_instances) | Terminate instances when autoscaling group is scheduled to stop | `bool` | `false` | no |
| <a name="input_aws_regions"></a> [aws\_regions](#input\_aws\_regions) | A list of one or more aws regions where the lambda will be apply, default use the current region | `list(string)` | `null` | no |
| <a name="input_cloudwatch_alarm_schedule"></a> [cloudwatch\_alarm\_schedule](#input\_cloudwatch\_alarm\_schedule) | Enable scheduleding on cloudwatch alarm resources | `bool` | `false` | no |
| <a name="input_custom_iam_role_arn"></a> [custom\_iam\_role\_arn](#input\_custom\_iam\_role\_arn) | Custom IAM role arn for the scheduling lambda | `string` | `null` | no |
| <a name="input_documentdb_schedule"></a> [documentdb\_schedule](#input\_documentdb\_schedule) | Enable scheduling on documentdb resources | `bool` | `false` | no |
| <a name="input_ec2_schedule"></a> [ec2\_schedule](#input\_ec2\_schedule) | Enable scheduling on ec2 resources | `bool` | `false` | no |
| <a name="input_ecs_schedule"></a> [ecs\_schedule](#input\_ecs\_schedule) | Enable scheduling on ecs services | `bool` | `false` | no |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key. | `string` | `null` | no |
| <a name="input_name"></a> [name](#input\_name) | Define name to use for lambda function, cloudwatch event and iam role | `string` | n/a | yes |
| <a name="input_rds_schedule"></a> [rds\_schedule](#input\_rds\_schedule) | Enable scheduling on rds resources | `bool` | `false` | no |
| <a name="input_redshift_schedule"></a> [redshift\_schedule](#input\_redshift\_schedule) | Enable scheduling on redshift resources | `bool` | `false` | no |
| <a name="input_resources_tag"></a> [resources\_tag](#input\_resources\_tag) | DEPRECATED, use scheduler\_tag variable instead | `map(string)` | `null` | no |
| <a name="input_runtime"></a> [runtime](#input\_runtime) | The runtime environment for the Lambda function that you are uploading | `string` | `"python3.13"` | no |
| <a name="input_schedule_action"></a> [schedule\_action](#input\_schedule\_action) | Define schedule action to apply on resources, accepted value are 'stop or 'start | `string` | `"stop"` | no |
| <a name="input_schedule_expression"></a> [schedule\_expression](#input\_schedule\_expression) | Define the aws event rule schedule expression, https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html | `string` | `"cron(0 22 ? * MON-FRI *)"` | no |
| <a name="input_schedule_expression_timezone"></a> [schedule\_expression\_timezone](#input\_schedule\_expression\_timezone) | Timezone in which the scheduling expression is evaluated. Example : 'America/New\_York', 'Europe/Paris' | `string` | `"UTC"` | no |
| <a name="input_scheduler_tag"></a> [scheduler\_tag](#input\_scheduler\_tag) | Set the tag to use for identify aws resources to stop or start | `map(string)` | <pre>{<br/>  "key": "tostop",<br/>  "value": "true"<br/>}</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | Custom tags on aws resources | `map(any)` | `null` | no |
| <a name="input_transfer_schedule"></a> [transfer\_schedule](#input\_transfer\_schedule) | Enable scheduling on AWS Transfer (SFTP) servers | `bool` | `false` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_iam_role_arn"></a> [lambda\_iam\_role\_arn](#output\_lambda\_iam\_role\_arn) | The ARN of the IAM role used by Lambda function |
| <a name="output_lambda_iam_role_name"></a> [lambda\_iam\_role\_name](#output\_lambda\_iam\_role\_name) | The name of the IAM role used by Lambda function |
| <a name="output_scheduler_expression"></a> [scheduler\_expression](#output\_scheduler\_expression) | The expression of the scheduler |
| <a name="output_scheduler_lambda_arn"></a> [scheduler\_lambda\_arn](#output\_scheduler\_lambda\_arn) | The ARN of the Lambda function |
| <a name="output_scheduler_lambda_function_last_modified"></a> [scheduler\_lambda\_function\_last\_modified](#output\_scheduler\_lambda\_function\_last\_modified) | The date Lambda function was last modified |
| <a name="output_scheduler_lambda_function_version"></a> [scheduler\_lambda\_function\_version](#output\_scheduler\_lambda\_function\_version) | Latest published version of your Lambda function |
| <a name="output_scheduler_lambda_invoke_arn"></a> [scheduler\_lambda\_invoke\_arn](#output\_scheduler\_lambda\_invoke\_arn) | The ARN to be used for invoking Lambda function from API Gateway |
| <a name="output_scheduler_lambda_name"></a> [scheduler\_lambda\_name](#output\_scheduler\_lambda\_name) | The name of the Lambda function |
| <a name="output_scheduler_log_group_arn"></a> [scheduler\_log\_group\_arn](#output\_scheduler\_log\_group\_arn) | The Amazon Resource Name (ARN) specifying the log group |
| <a name="output_scheduler_log_group_name"></a> [scheduler\_log\_group\_name](#output\_scheduler\_log\_group\_name) | The name of the scheduler log group |
| <a name="output_scheduler_timezone"></a> [scheduler\_timezone](#output\_scheduler\_timezone) | The timezone of the scheduler |
<!-- END_TF_DOCS -->

## Tests

Some of these tests create real resources in an AWS account. That means they cost money to run, especially if you don't clean up after yourself. Please be considerate of the resources you create and take extra care to clean everything up when you're done!

In order to run tests that access your AWS account, you will need to configure your [AWS CLI
credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). For example, you could
set the credentials as the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### End-to-end tests

```shell
# Test basic terraform deployment
cd examples/instance-scheduler
terraform test -verbose

# Test rds scheduler
cd examples/rds-scheduler
terraform test -verbose
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
