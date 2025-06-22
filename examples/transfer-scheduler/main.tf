resource "random_pet" "suffix" {}

resource "aws_transfer_server" "to_scheduled" {
  endpoint_type = "VPC"

  endpoint_details {
    subnet_ids = [aws_subnet.transfer_1.id]
    vpc_id     = aws_vpc.transfer.id
  }

  protocols = ["SFTP"]

  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_transfer_server" "not_to_scheduled" {
  endpoint_type = "VPC"

  endpoint_details {
    subnet_ids = [aws_subnet.transfer_2.id]
    vpc_id     = aws_vpc.transfer.id
  }

  protocols = ["SFTP"]

  tags = {
    tostop = "false"
  }
}


module "transfer_stop_friday" {
  source = "../.."

  name                = "stop-transfer-${random_pet.suffix.id}"
  schedule_expression = "cron(0 23 ? * FRI *)"
  schedule_action     = "stop"
  transfer_schedule   = true

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "transfer_start_monday" {
  source = "../.."

  name                = "start-transfer-${random_pet.suffix.id}"
  schedule_expression = "cron(0 07 ? * MON *)"
  schedule_action     = "start"
  transfer_schedule   = true

  scheduler_tag = {
    key   = "tostop"
    value = "true-${random_pet.suffix.id}"
  }
}

module "test_execution" {
  count  = var.test_mode ? 1 : 0
  source = "./test-execution"

  lambda_stop_name                 = module.transfer_stop_friday.scheduler_lambda_name
  transfer_server_to_scheduled_id  = aws_transfer_server.to_scheduled.id
  transfer_server_not_scheduled_id = aws_transfer_server.not_to_scheduled.id
}
