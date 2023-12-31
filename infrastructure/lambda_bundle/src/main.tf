locals {
  api_id = split("/", var.api_gateway.data.infrastructure.arn)[2]
  split_role = split("/", module.lambda_application.identity)
  role_name  = element(local.split_role, length(local.split_role) - 1)
  api_paths = { for p in var.api.api_paths : p.path => p }
}

module "lambda_application" {
  source            = "github.com/massdriver-cloud/terraform-modules//massdriver-application-aws-lambda?ref=23a47fa"
  md_metadata       = var.md_metadata
  image             = var.runtime.image
  x_ray_enabled     = var.observability.x-ray.enabled
  retention_days    = var.observability.retention_days
  memory_size       = var.runtime.memory_size
  execution_timeout = var.runtime.execution_timeout
}

########

resource "aws_api_gateway_resource" "api_resource" {
  for_each    = local.api_paths
  rest_api_id = local.api_id
  parent_id   = var.api_gateway.data.infrastructure.root_resource_id
  path_part   = each.value.path
}

resource "aws_api_gateway_method" "api_method" {
  for_each      = local.api_paths
  rest_api_id   = local.api_id
  resource_id   = aws_api_gateway_resource.api_resource[each.key].id
  http_method   = each.value.http_method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api_integration" {
  for_each                 = local.api_paths
  rest_api_id              = local.api_id
  resource_id              = aws_api_gateway_resource.api_resource[each.key].id
  http_method              = aws_api_gateway_method.api_method[each.key].http_method
  integration_http_method  = "POST"
  type                     = "AWS_PROXY"
  uri                      = module.lambda_application.function_invoke_arn
}
