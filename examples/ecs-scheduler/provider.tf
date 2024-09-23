terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.20.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.2.0"
    }
  }
  required_version = ">= 1.0.11"
}

provider "aws" {
  region = "us-west-1"
  default_tags {
    tags = {
      Created_by = "Terraform"
      Project    = "esc-scheduler-testing-example"
    }
  }
}

