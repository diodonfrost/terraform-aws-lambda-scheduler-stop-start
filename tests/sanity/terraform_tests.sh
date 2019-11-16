#!/bin/bash

# Install the Latest version of Terraform
sudo pip install ansible
sudo ansible-galaxy install diodonfrost.terraform && sudo ln -s ~/.ansible/roles/diodonfrost.terraform ~/.ansible/roles/ansible-role-terraform
sudo ansible-pull -U https://github.com/diodonfrost/ansible-role-terraform tests/test.yml -e "terraform_version=${terraform_version}"
terraform -version
terraform init

# Test Terraform syntax
terraform validate \
  -var "region=${AWS_REGION}" \
  -var "name=stop-aws-resources" \
  -var "cloudwatch_schedule_expression=cron(0 22 ? * MON-FRI *)" \
  -var "schedule_action=stop" \
  -var "ec2_schedule=true" \
  -var "rds_schedule=true" \
  -var "autoscaling_schedule=true"

# Terraform lint
terraform fmt -check -diff main.tf

# Test Terraform fixture example
cd examples/test_fixture || exist
terraform init
terraform validate
terraform -v
