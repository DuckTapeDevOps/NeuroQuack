variable "service_name" {
  description = "The name of the cluster"
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

variable "api_gateway_subnet_ids" {
  type        = list(string)
  description = "The IDs of the API Gateway subnets."
}

variable "api_gateway_name" {
  type        = string
  description = "The name of the API Gateway."
}