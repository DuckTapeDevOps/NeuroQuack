locals {
  cluster_name = "${var.project_name}-cluster"
  service_name = "${var.project_name}-service"
  family_name = "${var.project_name}-family"
  container_image = "375112818203.dkr.ecr.us-east-1.amazonaws.com/massdriver/ducktronaut:latest"
}

module "ecs_cluster" {
  source = "./ecs-cluster"

  cluster_name = local.cluster_name

  # Pass variables to the module
}

module "ecs_service" {
  source = "./ecs-service"

  cluster_name = local.cluster_name
  service_name = local.service_name
  container_image = local.container_image
  task_family_name = local.family_name
  task_cpu = 256
  task_memory = 512
  account_id = data.aws_caller_identity.current.account_id
  region = data.aws_region.current.name
  desired_count = 1
  container_env_vars = {
    "AWS_DEFAULT_REGION" = data.aws_region.current.name
    "AWS_ACCOUNT_ID" = data.aws_caller_identity.current.account_id
  }
}