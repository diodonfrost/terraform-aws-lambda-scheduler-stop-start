# Terraform ecs with lambda scheduler

# Get aws availability zones
data "aws_availability_zones" "available" {}

### Terraform modules ###

module "ecs-stop-friday" {
  source                         = "../../"
  name                           = "stop-ecs"
  schedule_expression            = "cron(45 21 * * ? *)"
  schedule_expression_timezone   = "Europe/Berlin"
  schedule_action                = "stop"
  ec2_schedule                   = "false"
  ecs_schedule                   = "true"
  rds_schedule                   = "false"
  autoscaling_schedule           = "false"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}

module "ecs-start-monday" {
  source                         = "../../"
  name                           = "start-ecs"
  schedule_expression            = "cron(45 21 * * ? *)"
  schedule_expression_timezone   = "Europe/Berlin"
  schedule_action                = "start"
  ec2_schedule                   = "false"
  ecs_schedule                   = "true"
  autoscaling_schedule           = "false"
  cloudwatch_alarm_schedule      = "true"

  scheduler_tag = {
    key   = "tostop"
    value = "true"
  }
}
