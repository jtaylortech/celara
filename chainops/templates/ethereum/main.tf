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
  description = "Security group for Ethereum validator"
  vpc_id      = aws_vpc.validator.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidrs
    description = "SSH access"
  }

  # Geth P2P TCP
  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Geth P2P TCP"
  }

  # Geth P2P UDP
  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Geth P2P UDP"
  }

  # Beacon node P2P TCP
  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Beacon node P2P TCP"
  }

  # Beacon node P2P UDP
  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Beacon node P2P UDP"
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

# EC2 Instance
resource "aws_instance" "validator" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.validator.id

  vpc_security_group_ids = [aws_security_group.validator.id]
  key_name               = var.key_name

  root_block_device {
    volume_size = var.storage_size
    volume_type = "gp3"
    iops        = 3000
    throughput  = 125
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
