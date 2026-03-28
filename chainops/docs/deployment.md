# Deployment Guide

## How ChainOps Works

1. `chainops init` generates a `chainops.yaml` config with chain-specific defaults
2. `chainops deploy` copies Terraform templates, generates `terraform.tfvars`, runs `terraform init → plan → apply`
3. `chainops status` queries Terraform state
4. `chainops destroy` runs `terraform destroy`

## Chain Defaults

| Chain | Instance | Storage | Estimated Cost |
|-------|----------|---------|----------------|
| Ethereum | t3.xlarge (4 vCPU, 16 GB) | 2 TB gp3 | ~$335/mo |
| Solana | r6i.2xlarge (8 vCPU, 64 GB) | 2 TB gp3 | ~$715/mo |

Spot instances reduce compute cost by ~70% (not recommended for mainnet validators).

## Config File

```yaml
# chainops.yaml
name: ethereum-validator
chain: ethereum
network: mainnet
provider: aws
region: us-east-1
compute:
  instance_type: t3.xlarge
  storage_size: 2000
  spot_instances: false
```

## Prerequisites

- **Terraform** >= 1.0 installed and in PATH
- **AWS credentials** configured (`aws configure` or env vars)
- **SSH key pair** for node access
- Sufficient AWS quotas for the instance type

## What Gets Created

The Terraform templates provision:

- EC2 instance with chain-specific AMI
- EBS volumes (gp3) for chain data
- Security group (SSH + P2P + RPC ports)
- CloudWatch monitoring
- Cloud-init script for node software installation

## Cost Breakdown

### Ethereum
| Component | Monthly |
|-----------|---------|
| EC2 (t3.xlarge) | $120 |
| EBS 2TB gp3 | $160 |
| Data transfer ~500GB | $45 |
| CloudWatch | $10 |
| **Total** | **$335** |

### Solana
| Component | Monthly |
|-----------|---------|
| EC2 (r6i.2xlarge) | $360 |
| EBS Ledger 2TB | $200 |
| EBS Accounts 500GB | $50 |
| Data transfer ~1TB | $90 |
| CloudWatch | $15 |
| **Total** | **$715** |
