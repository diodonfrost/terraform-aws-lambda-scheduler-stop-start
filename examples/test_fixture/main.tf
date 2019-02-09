# Deploy two lambda for testing with awspec

provider "aws" {
  region = "eu-west-3"
}

module "ec2-stop-friday" {
  source                         = "../.."
  name                           = "stop-ec2"
  cloudwatch_schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action                = "stop"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}

module "ec2-start-monday" {
  source                         = "../.."
  name                           = "start-ec2"
  cloudwatch_schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action                = "start"
  ec2_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  resources_tag                  = {
    key   = "tostop"
    value = "true"
  }
}
