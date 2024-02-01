resource "aws_security_group" "ecs_service" {
  name = "ecs_service"
  vpc_id = "${var.vpc_id}"
}
