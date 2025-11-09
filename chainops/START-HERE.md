# ChainOps - Start Here

Infrastructure-as-Code for blockchain validators. You know Terraform, you know cloud - let's build this.

## Quick Start

```bash
# Navigate to project
cd celara-homepage/chainops

# Install dependencies
uv sync --all-extras

# Run tests (when we have them)
uv run pytest

# Try the CLI (skeleton)
uv run chainops --help
```

## What You're Building

**Goal:** Deploy production-grade validators with one command.

```bash
chainops init ethereum --network mainnet
chainops deploy
# Validator running in 15 minutes
```

## Architecture

```
ChainOps CLI (Python/Typer)
    ↓
Configuration (YAML + Pydantic)
    ↓
Terraform Modules (HCL)
    ↓
Cloud Provider (AWS/GCP/Azure)
    ↓
Provisioning (Cloud-Init + Ansible)
    ↓
Running Validator
```

## Week 1: Foundation

**Day 1-2: CLI + Config**
- [ ] Build CLI skeleton with Typer
- [ ] Create Pydantic config models
- [ ] YAML config parsing
- [ ] Validation logic

**Day 3-5: Terraform Templates**
- [ ] Ethereum validator template (AWS)
- [ ] VPC, security groups, EC2
- [ ] EBS storage (2TB gp3)
- [ ] CloudWatch monitoring

**Day 6-7: Provisioning**
- [ ] Cloud-init script for Geth
- [ ] Systemd service configuration
- [ ] Basic monitoring setup
- [ ] Test end-to-end deployment

## Week 2: Make It Work

**Goals:**
- [ ] Deploy working Ethereum validator on AWS
- [ ] Proper error handling
- [ ] Cost estimation
- [ ] Basic documentation

## Tech Stack

**You Already Know:**
- Terraform (your bread and butter)
- AWS (EC2, VPC, EBS, CloudWatch)
- Python (for CLI)
- Ansible/Cloud-Init (provisioning)

**New Stuff:**
- Geth/Nethermind (Ethereum clients)
- Validator operations (we'll figure it out)

## Project Structure

```
chainops/
├── src/chainops/
│   ├── cli.py              # Typer CLI (you build this)
│   ├── config.py           # Pydantic models
│   ├── deployer.py         # Terraform wrapper
│   └── providers/
│       └── aws.py          # AWS-specific logic
├── templates/
│   └── ethereum/
│       ├── main.tf         # Your Terraform magic
│       ├── variables.tf
│       ├── outputs.tf
│       └── cloud-init.yaml # Geth installation
└── tests/
    └── test_cli.py
```

## First Terraform Template

Start with this structure:

```hcl
# templates/ethereum/main.tf

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
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.validator_name}-vpc"
  }
}

# Subnet
resource "aws_subnet" "validator" {
  vpc_id                  = aws_vpc.validator.id
  cidr_block              = "10.0.1.0/24"
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
    cidr_blocks = ["0.0.0.0/0"] # TODO: Restrict this
  }

  # Geth P2P
  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30303
    to_port     = 30303
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Beacon node P2P
  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
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
  key_name              = var.key_name

  root_block_device {
    volume_size = var.storage_size
    volume_type = "gp3"
    iops        = 3000
    throughput  = 125
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
}

# Outputs
output "instance_id" {
  value = aws_instance.validator.id
}

output "public_ip" {
  value = aws_instance.validator.public_ip
}

output "ssh_command" {
  value = "ssh ubuntu@${aws_instance.validator.public_ip}"
}
```

## Cloud-Init Script

```yaml
# templates/ethereum/cloud-init.yaml
#cloud-config

package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose
  - git

runcmd:
  # Install Geth
  - add-apt-repository -y ppa:ethereum/ethereum
  - apt-get update
  - apt-get install -y geth
  
  # Create geth user
  - useradd -m -s /bin/bash geth
  
  # Create data directory
  - mkdir -p /data/geth
  - chown -R geth:geth /data/geth
  
  # Create systemd service
  - |
    cat > /etc/systemd/system/geth.service <<EOF
    [Unit]
    Description=Geth Ethereum Client
    After=network.target
    
    [Service]
    Type=simple
    User=geth
    ExecStart=/usr/bin/geth \
      --datadir /data/geth \
      --http \
      --http.addr 0.0.0.0 \
      --http.api eth,net,web3 \
      --ws \
      --ws.addr 0.0.0.0 \
      --ws.api eth,net,web3 \
      --authrpc.addr 0.0.0.0 \
      --authrpc.vhosts * \
      --metrics \
      --metrics.addr 0.0.0.0
    Restart=always
    RestartSec=10
    
    [Install]
    WantedBy=multi-user.target
    EOF
  
  # Start Geth
  - systemctl daemon-reload
  - systemctl enable geth
  - systemctl start geth

write_files:
  - path: /etc/motd
    content: |
      Ethereum Validator Node
      Managed by ChainOps
```

## CLI Skeleton

```python
# src/chainops/cli.py
import typer
from pathlib import Path
from chainops.config import ChainOpsConfig
from chainops.deployer import Deployer

app = typer.Typer(help="ChainOps - Infrastructure-as-Code for validators")

@app.command()
def init(
    chain: str = typer.Argument(..., help="Blockchain (ethereum, solana)"),
    network: str = typer.Option("mainnet", help="Network (mainnet, testnet)"),
    provider: str = typer.Option("aws", help="Cloud provider (aws, gcp, azure)"),
):
    """Initialize validator configuration."""
    typer.echo(f"Initializing {chain} validator on {network}...")
    
    config = ChainOpsConfig(
        chain=chain,
        network=network,
        provider=provider,
    )
    
    config_path = Path("chainops.yaml")
    config.save(config_path)
    
    typer.echo(f"✓ Configuration saved to {config_path}")
    typer.echo(f"\nNext steps:")
    typer.echo(f"  1. Review and customize: vim chainops.yaml")
    typer.echo(f"  2. Deploy: chainops deploy")

@app.command()
def deploy(
    config_file: Path = typer.Option("chainops.yaml", help="Config file"),
    auto_approve: bool = typer.Option(False, help="Skip confirmation"),
):
    """Deploy validator infrastructure."""
    typer.echo("Deploying validator...")
    
    config = ChainOpsConfig.load(config_file)
    deployer = Deployer(config)
    
    if not auto_approve:
        typer.confirm("Deploy infrastructure?", abort=True)
    
    deployer.deploy()
    typer.echo("✓ Validator deployed successfully")

@app.command()
def status():
    """Check validator status."""
    typer.echo("Validator Status:")
    typer.echo("  Status: Running")
    typer.echo("  Sync: 45% complete")

@app.command()
def destroy(
    force: bool = typer.Option(False, help="Skip confirmation"),
):
    """Destroy validator infrastructure."""
    if not force:
        typer.confirm("Destroy all infrastructure?", abort=True)
    
    typer.echo("Destroying infrastructure...")
    typer.echo("✓ Infrastructure destroyed")

if __name__ == "__main__":
    app()
```

## Resources

**Ethereum Validator Setup:**
- [Ethereum Staking Guide](https://ethereum.org/en/staking/)
- [Geth Documentation](https://geth.ethereum.org/docs)
- [Lighthouse (Consensus Client)](https://lighthouse-book.sigmaprime.io/)

**Terraform AWS:**
- You already know this stuff

**Testing:**
- Deploy to testnet first (Sepolia)
- Use Spot instances for cost savings
- Monitor with CloudWatch

## Success Criteria

**Week 1:**
- [ ] CLI works (`chainops init`, `chainops deploy`)
- [ ] Terraform deploys EC2 instance
- [ ] Geth starts syncing

**Week 2:**
- [ ] Full Ethereum validator running
- [ ] Monitoring configured
- [ ] Documentation complete
- [ ] Cost < $200/month

## Let's Ship This

You've got the skills. The template above is your starting point. Make it production-grade.

Questions? Hit me up.

— Q
