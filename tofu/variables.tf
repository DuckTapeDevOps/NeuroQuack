variable "region" {
  description = "The region to deploy to."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
    description = "The name of the project."
    type        = string
    default     = "NeuroQuack"
}

variable "subnet_ids" {
  description = "The subnet IDs to deploy to."
  type        = list(string)
  default     = ["subnet-0eaa6b55c6426d83b", "subnet-0b58912a3840b038c", "subnet-0725af53583f24e46", "subnet-0bc476f824884d807"]
}

variable "container_image" {
  description = "The container image to deploy."
  type        = string
  default     = "375112818203.dkr.ecr.us-east-1.amazonaws.com/massdriver/ducktronaut:latest"
}

variable "vpc_id" {
  description = "The VPC ID to deploy to."
  type        = string
  default     = "vpc-02f099acc23713697"
}
