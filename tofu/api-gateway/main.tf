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

resource "aws_api_gateway_method" "start_bot_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.start_bot.id
  http_method   = "POST"
  authorization = "NONE"
}


##########################
### stop_bot       #######
##########################

resource "aws_api_gateway_resource" "stop_bot" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "stop_bot"
}

resource "aws_api_gateway_method" "stop_bot_post" {
  rest_api_id       = aws_api_gateway_rest_api.main.id
  resource_id       = aws_api_gateway_resource.stop_bot.id
  http_method       = "POST"
  authorization     = "NONE"

}

##########################
### deployment      ######
##########################

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
}

##########################
### integration     ######
##########################

resource "aws_api_gateway_integration" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.main.id
  http_method = aws_api_gateway_method.main.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.main.invoke_arn
}