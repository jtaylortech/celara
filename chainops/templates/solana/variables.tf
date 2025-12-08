variable "validator_name" {
  description = "Name of the validator"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type (Solana requires high-performance)"
  type        = string
  default     = "r6i.2xlarge"
}

variable "storage_size" {
  description = "Ledger storage size in GB"
  type        = number
  default     = 2000
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "allowed_ssh_cidrs" {
  description = "Allowed CIDR blocks for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "key_name" {
  description = "SSH key pair name (optional)"
  type        = string
  default     = null
}

variable "network" {
  description = "Solana network (mainnet-beta, testnet, devnet)"
  type        = string
  default     = "devnet"
}
