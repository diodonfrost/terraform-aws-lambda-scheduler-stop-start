<!-- BEGIN_TF_DOCS -->
## Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | n/a |
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
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
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_iam_policy_document.autoscaling_group_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.cloudwatch_alarm_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.rds_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.redshift_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.resource_groups_tagging_api](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.spot_instance_scheduler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_autoscaling_schedule"></a> [autoscaling\_schedule](#input\_autoscaling\_schedule) | Enable scheduling on autoscaling resources | `any` | `false` | no |
| <a name="input_autoscaling_terminate_instances"></a> [autoscaling\_terminate\_instances](#input\_autoscaling\_terminate\_instances) | Terminate instances when autoscaling group is scheduled to stop | `bool` | `false` | no |
| <a name="input_aws_regions"></a> [aws\_regions](#input\_aws\_regions) | A list of one or more aws regions where the lambda will be apply, default use the current region | `list(string)` | `null` | no |
| <a name="input_cloudwatch_alarm_schedule"></a> [cloudwatch\_alarm\_schedule](#input\_cloudwatch\_alarm\_schedule) | Enable scheduleding on cloudwatch alarm resources | `any` | `false` | no |
| <a name="input_cloudwatch_schedule_expression"></a> [cloudwatch\_schedule\_expression](#input\_cloudwatch\_schedule\_expression) | Define the aws cloudwatch event rule schedule expression | `string` | `"cron(0 22 ? * MON-FRI *)"` | no |
| <a name="input_custom_iam_role_arn"></a> [custom\_iam\_role\_arn](#input\_custom\_iam\_role\_arn) | Custom IAM role arn for the scheduling lambda | `string` | `null` | no |
| <a name="input_documentdb_schedule"></a> [documentdb\_schedule](#input\_documentdb\_schedule) | Enable scheduling on documentdb resources | `bool` | `false` | no |
| <a name="input_ec2_schedule"></a> [ec2\_schedule](#input\_ec2\_schedule) | Enable scheduling on ec2 resources | `any` | `false` | no |
| <a name="input_ecs_schedule"></a> [ecs\_schedule](#input\_ecs\_schedule) | Enable scheduling on ecs services | `bool` | `false` | no |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn) | The ARN for the KMS encryption key. If this configuration is not provided when environment variables are in use, AWS Lambda uses a default service key. | `string` | `null` | no |
| <a name="input_name"></a> [name](#input\_name) | Define name to use for lambda function, cloudwatch event and iam role | `string` | n/a | yes |
| <a name="input_rds_schedule"></a> [rds\_schedule](#input\_rds\_schedule) | Enable scheduling on rds resources | `any` | `false` | no |
| <a name="input_redshift_schedule"></a> [redshift\_schedule](#input\_redshift\_schedule) | Enable scheduling on redshift resources | `any` | `false` | no |
| <a name="input_resources_tag"></a> [resources\_tag](#input\_resources\_tag) | DEPRECATED, use scheduler\_tag variable instead | `map(string)` | `null` | no |
| <a name="input_schedule_action"></a> [schedule\_action](#input\_schedule\_action) | Define schedule action to apply on resources, accepted value are 'stop or 'start | `string` | `"stop"` | no |
| <a name="input_scheduler_tag"></a> [scheduler\_tag](#input\_scheduler\_tag) | Set the tag to use for identify aws resources to stop or start | `map(string)` | <pre>{<br>  "key": "tostop",<br>  "value": "true"<br>}</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | Custom tags on aws resources | `map(any)` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_iam_role_arn"></a> [lambda\_iam\_role\_arn](#output\_lambda\_iam\_role\_arn) | The ARN of the IAM role used by Lambda function |
| <a name="output_lambda_iam_role_name"></a> [lambda\_iam\_role\_name](#output\_lambda\_iam\_role\_name) | The name of the IAM role used by Lambda function |
| <a name="output_scheduler_lambda_arn"></a> [scheduler\_lambda\_arn](#output\_scheduler\_lambda\_arn) | The ARN of the Lambda function |
| <a name="output_scheduler_lambda_function_last_modified"></a> [scheduler\_lambda\_function\_last\_modified](#output\_scheduler\_lambda\_function\_last\_modified) | The date Lambda function was last modified |
| <a name="output_scheduler_lambda_function_version"></a> [scheduler\_lambda\_function\_version](#output\_scheduler\_lambda\_function\_version) | Latest published version of your Lambda function |
| <a name="output_scheduler_lambda_invoke_arn"></a> [scheduler\_lambda\_invoke\_arn](#output\_scheduler\_lambda\_invoke\_arn) | The ARN to be used for invoking Lambda function from API Gateway |
| <a name="output_scheduler_lambda_name"></a> [scheduler\_lambda\_name](#output\_scheduler\_lambda\_name) | The name of the Lambda function |
| <a name="output_scheduler_log_group_arn"></a> [scheduler\_log\_group\_arn](#output\_scheduler\_log\_group\_arn) | The Amazon Resource Name (ARN) specifying the log group |
| <a name="output_scheduler_log_group_name"></a> [scheduler\_log\_group\_name](#output\_scheduler\_log\_group\_name) | The name of the scheduler log group |
<!-- END_TF_DOCS -->