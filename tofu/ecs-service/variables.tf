variable "container_image" {
  description = "The image of the service"
  type        = string
}

variable "task_family_name" {
  description = "The name of the task family"
  type        = string
}

variable "service_name" {
  description = "The name of the cluster"
  type        = string
}

variable "task_cpu" {
  description = "The cpu of the task"
  type        = number
}

variable "task_memory" {
  description = "The memory of the task"
  type        = number
}

variable "cluster_id" {
  description = "The ID of the ECS cluster"
  type        = string
}

variable "region" {
  description = "The region of the cluster"
  type        = string
}

variable "account_id" {
  description = "The account id of the cluster"
  type        = string
}

variable "desired_count" {
  description = "The desired count of the service"
  type        = number
}

variable "container_env_vars" {
  description = "The environment variables of the container"
  type        = map(string)
}

variable "vpc_id" {
  description = "The vpc id of the cluster's vpc"
  type        = string
}

variable "subnet_ids" {
  type        = list(string)
  description = "The IDs of the API Gateway subnets."
}