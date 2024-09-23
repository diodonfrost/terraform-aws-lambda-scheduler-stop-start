#!/bin/bash
set -e

# Install the Latest version of Terraform
sudo pip install ansible
sudo ansible-galaxy install diodonfrost.terraform
sudo ansible-pull -U https://github.com/diodonfrost/ansible-role-terraform tests/test.yml -e "terraform_version=${terraform_version}"
terraform -version
terraform init

# Test Terraform syntax
export AWS_DEFAULT_REGION=eu-west-1
terraform validate

# Terraform lint
terraform fmt -check -diff main.tf

# Test Terraform fixture example
cd examples/test_fixture || exist
terraform init
terraform validate
terraform -v
