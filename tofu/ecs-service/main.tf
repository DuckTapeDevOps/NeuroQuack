data "aws_ecs_cluster" "main" {
  cluster_name = var.cluster_name
}

resource "aws_ecs_service" "main" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  iam_role        = aws_iam_role.execution_role.arn
  desired_count   = 0
  launch_type    = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.example.id]
    security_groups = [aws_security_group.example.id]
  }

  # load_balancer {
  #   target_group_arn = aws_lb_target_group.example.arn
  #   container_name   = "${var.service_name}-container"
  #   container_port   = 8080
  # }

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
