output "api_gateway_sg_id" {
  description = "Security Group ID of the API Gateway"
  value       = aws_security_group.api_gateway.id
}