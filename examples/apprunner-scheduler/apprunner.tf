resource "aws_apprunner_service" "to_scheduled" {
  service_name = "test-to-stop-${random_pet.suffix.id}"

  source_configuration {
    auto_deployments_enabled = false

    image_repository {
      image_configuration {
        port = "8080"
      }
      image_identifier      = "public.ecr.aws/aws-containers/hello-app-runner:latest"
      image_repository_type = "ECR_PUBLIC"
    }
  }

  tags = {
    tostop = "true-${random_pet.suffix.id}"
  }
}

resource "aws_apprunner_service" "not_to_scheduled" {
  service_name = "test-not-to-stop-${random_pet.suffix.id}"

  source_configuration {
    auto_deployments_enabled = false

    image_repository {
      image_configuration {
        port = "8080"
      }
      image_identifier      = "public.ecr.aws/aws-containers/hello-app-runner:latest"
      image_repository_type = "ECR_PUBLIC"
    }
  }

  tags = {
    tostop = "false"
  }
}
