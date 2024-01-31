locals {
  cluster_name = "${var.project_name}-cluster"
  service_name = "${var.project_name}-service"
  family_name = "${var.project_name}-family"
}

module "ecs_cluster" {
  source = "./ecs-cluster"

  cluster_name = local.cluster_name

  # Pass variables to the module
}

module "ecs_service" {
  source = "./ecs-service"
  api_gateway_subnet_ids = var.subnet_ids
  cluster_id   = module.ecs_cluster.ecs_cluster_id
  service_name = local.service_name
  container_image = var.container_image
  task_family_name = local.family_name
  task_cpu = 256
  task_memory = 512
  account_id = data.aws_caller_identity.current.account_id
  region = data.aws_region.current.name
  vpc_id = var.vpc_id
  desired_count = 1
  container_env_vars = {
    "AWS_DEFAULT_REGION" = data.aws_region.current.name
    "AWS_ACCOUNT_ID" = data.aws_caller_identity.current.account_id
  }
}

module "api_gateway" {
  source = "./api-gateway"
  api_gateway_subnet_ids = var.subnet_ids
  service_name = local.service_name
  account_id = data.aws_caller_identity.current.account_id
  api_gateway_name = "${var.project_name}-api-gw"
  region = data.aws_region.current.name
}