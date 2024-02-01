resource "aws_api_gateway_rest_api" "main" {
  name        = var.api_gateway_name
  description = "API Gateway"
}

##########################
### start_bot       ###### 
##########################

resource "aws_api_gateway_resource" "start_bot" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "start_bot"
}

resource "aws_api_gateway_method" "start_bot" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.start_bot.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "start_bot" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.start_bot.id
  http_method = aws_api_gateway_method.start_bot.http_method

  type                    = "HTTP"
  integration_http_method = "POST"
  uri                     = "http://${var.nlb_dns_name}/start_bot"
}

##########################
### stop_bot       #######
##########################

resource "aws_api_gateway_resource" "stop_bot" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "stop_bot"
}

resource "aws_api_gateway_method" "stop_bot" {
  rest_api_id       = aws_api_gateway_rest_api.main.id
  resource_id       = aws_api_gateway_resource.stop_bot.id
  http_method       = "POST"
  authorization     = "NONE"
}

resource "aws_api_gateway_integration" "stop_bot" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.stop_bot.id
  http_method = aws_api_gateway_method.stop_bot.http_method

  type                    = "HTTP"
  integration_http_method = "POST"
  uri                     = "http://${var.nlb_dns_name}/stop_bot"
}

##########################
### deployment      ######
##########################

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
}
