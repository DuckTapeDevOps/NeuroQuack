data "aws_vpc" "main" {
  id = var.vpc_id
}

resource "aws_ecs_service" "main" {
  name            = var.service_name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.main.arn
  iam_role        = aws_iam_role.execution_role.arn
  desired_count   = 0
  launch_type    = "FARGATE"

  network_configuration {
    subnets          = var.api_gateway_subnet_ids
    security_groups = [aws_security_group.ecs_service.id]
  }

}

resource "aws_ecs_task_definition" "main" {
  family                   = var.task_family_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory

  container_definitions = jsonencode([
      {
        name      = "${var.service_name}-container"
        image     = var.container_image
        essential = true
        portMappings = [
          {
            containerPort = 8080
            hostPort      = 8080
          }
        ]
      }
    ])
  }
