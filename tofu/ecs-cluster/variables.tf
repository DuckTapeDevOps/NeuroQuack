variable "cluster_name" {
  description = "The name of the cluster"
  type        = string
}

variable "subnet_ids" {
  type        = list(string)
  description = "The IDs of the API Gateway subnets."
}