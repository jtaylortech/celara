terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# VPC
resource "aws_vpc" "validator" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.validator_name}-vpc"
  }
}

# Subnet
resource "aws_subnet" "validator" {
  vpc_id                  = aws_vpc.validator.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, 1)
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "${var.validator_name}-subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "validator" {
  vpc_id = aws_vpc.validator.id

  tags = {
    Name = "${var.validator_name}-igw"
  }
}

# Route Table
resource "aws_route_table" "validator" {
  vpc_id = aws_vpc.validator.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.validator.id
  }

  tags = {
    Name = "${var.validator_name}-rt"
  }
}

resource "aws_route_table_association" "validator" {
  subnet_id      = aws_subnet.validator.id
  route_table_id = aws_route_table.validator.id
}

# Security Group
resource "aws_security_group" "validator" {
  name        = "${var.validator_name}-sg"
  description = "Security group for Solana validator"
  vpc_id      = aws_vpc.validator.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
    description = "SSH access"
  }

  # Solana Gossip
  ingress {
    from_port   = 8000
    to_port     = 8020
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Solana gossip TCP"
  }

  ingress {
    from_port   = 8000
    to_port     = 8020
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Solana gossip UDP"
  }

  # Solana RPC
  ingress {
    from_port   = 8899
    to_port     = 8899
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
    description = "Solana RPC"
  }

  # Solana WebSocket
  ingress {
    from_port   = 8900
    to_port     = 8900
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
    description = "Solana WebSocket"
  }

  # Metrics
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
    description = "Prometheus metrics"
  }

  # Outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = {
    Name = "${var.validator_name}-sg"
  }
}

# EC2 Instance - Solana requires high-performance instances
resource "aws_instance" "validator" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.validator.id

  vpc_security_group_ids = [aws_security_group.validator.id]
  key_name               = var.key_name

  root_block_device {
    volume_size = 500
    volume_type = "gp3"
    iops        = 3000
    throughput  = 125
    encrypted   = true
  }

  # Ledger storage - NVMe for performance
  ebs_block_device {
    device_name = "/dev/sdf"
    volume_size = var.storage_size
    volume_type = "gp3"
    iops        = 16000
    throughput  = 1000
    encrypted   = true
  }

  # Accounts storage
  ebs_block_device {
    device_name = "/dev/sdg"
    volume_size = 500
    volume_type = "gp3"
    iops        = 10000
    throughput  = 700
    encrypted   = true
  }

  user_data = file("${path.module}/cloud-init.yaml")

  tags = {
    Name = var.validator_name
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
