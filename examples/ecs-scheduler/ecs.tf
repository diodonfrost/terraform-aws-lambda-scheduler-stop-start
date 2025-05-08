resource "aws_ecs_cluster" "this" {
  name = "test-ecs-cluster-${random_pet.suffix.id}"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_ecs_service" "to_scheduled" {
  name            = "test-to-stop-${random_pet.suffix.id}"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.primary.id]
  }

  tags = {
    tostop = "true",
  }
  lifecycle {
    ignore_changes = [
      desired_count,
      tags
    ]
  }
}

resource "aws_ecs_service" "not_to_scheduled" {
  name            = "test-not-to-stop-${random_pet.suffix.id}"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [aws_subnet.primary.id]
  }

  tags = {
    tostop = "false",
  }
  lifecycle {
    ignore_changes = [
      desired_count,
      tags
    ]
  }
}

resource "aws_ecs_task_definition" "this" {
  family = "test-${random_pet.suffix.id}"

  # Refer to https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html
  # for cpu and memory values
  cpu    = 256
  memory = 512

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  # execution_role_arn = aws_iam_role.ecs_service.arn
  task_role_arn = aws_iam_role.hello_ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "hello-world-rest"
      image     = "docker.io/library/nginx:alpine"
      cpu       = 10
      memory    = 128
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
    }
  ])
}
