# Deploy two lambda for testing with awspec

provider "aws" {
  region = "eu-west-3"
}

module "aws-stop-friday" {
  source                         = "../.."
  name                           = "stop-aws"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "true"
  rds_schedule                   = "true"
  autoscaling_schedule           = "true"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}

module "aws-start-monday" {
  source                         = "../.."
  name                           = "start-aws"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "true"
  rds_schedule                   = "true"
  autoscaling_schedule           = "true"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
