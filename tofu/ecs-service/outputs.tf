output "ecs_service_sg_id" {
  description = "Security Group ID of the ECS Service"
  value       = aws_security_group.ecs_service.id
}