# ChainOps Quick Start

Deploy an Ethereum validator in 15 minutes.

## Prerequisites

1. **AWS Account** with credentials configured
2. **Terraform** installed (`brew install terraform`)
3. **Python 3.11+** installed
4. **SSH Key** in AWS (optional but recommended)

## Installation

```bash
cd celara-homepage/chainops

# Install dependencies
uv sync --all-extras

# Verify installation
uv run chainops --help
```

## Deploy to Testnet (Recommended First)

```bash
# 1. Initialize configuration
uv run chainops init ethereum --network sepolia

# 2. Review configuration
cat chainops.yaml

# 3. Estimate costs
uv run chainops estimate
# Expected: ~$50-80/month with spot instances

# 4. Deploy (dry run first)
uv run chainops deploy --dry-run

# 5. Deploy for real
uv run chainops deploy

# 6. Check status
uv run chainops status

# 7. SSH into validator
ssh ubuntu@<public-ip>

# 8. Check Geth sync status
sudo systemctl status geth
sudo journalctl -u geth -f
```

## Deploy to Mainnet

```bash
# 1. Initialize configuration
uv run chainops init ethereum --network mainnet

# 2. Customize configuration
vim chainops.yaml
# - Set allowed_ssh_cidrs to your IP
# - Consider spot_instances: true for savings
# - Adjust instance_type if needed

# 3. Estimate costs
uv run chainops estimate
# Expected: ~$335/month (or ~$100 with spot)

# 4. Deploy
uv run chainops deploy

# 5. Monitor sync progress
ssh ubuntu@<public-ip>
validator-status
```

## Configuration Options

### Minimal (Testnet)
```yaml
name: my-validator
chain: ethereum
network: sepolia
provider: aws
region: us-east-1
```

### Production (Mainnet)
```yaml
name: my-validator
chain: ethereum
network: mainnet
provider: aws
region: us-east-1

compute:
  instance_type: t3.xlarge
  storage_size: 2000
  spot_instances: false

networking:
  vpc_cidr: 10.0.0.0/16
  public_ip: true
  allowed_ssh_cidrs:
    - "1.2.3.4/32"  # Your IP only

monitoring:
  enabled: true
  metrics_port: 9090
```

## Common Commands

```bash
# Initialize new validator
uv run chainops init ethereum --network mainnet

# Deploy infrastructure
uv run chainops deploy

# Check status
uv run chainops status

# Estimate costs
uv run chainops estimate

# Destroy infrastructure
uv run chainops destroy
```

## Troubleshooting

### Terraform not found
```bash
brew install terraform
```

### AWS credentials not configured
```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

### SSH connection refused
Wait 2-3 minutes after deployment for cloud-init to complete.

### Geth not syncing
```bash
ssh ubuntu@<public-ip>
sudo journalctl -u geth -f
# Check for errors
```

## Cost Optimization

### Use Spot Instances (70% savings)
```yaml
compute:
  spot_instances: true
```

### Smaller Instance for Testnet
```yaml
compute:
  instance_type: t3.large  # vs t3.xlarge
  storage_size: 500  # vs 2000
```

### Reserved Instances (40% savings)
Purchase 1-year reserved instance in AWS Console.

## Next Steps

1. **Monitor Sync Progress**: Takes 6-12 hours for Ethereum mainnet
2. **Setup Beacon Node**: Required for validation (coming soon)
3. **Configure Monitoring**: CloudWatch dashboards (coming soon)
4. **Backup Keys**: Store validator keys securely

## Support

- **Issues**: Open GitHub issue
- **Discord**: [discord.gg/celara](https://discord.gg/celara)
- **Docs**: [docs.celara.dev/chainops](https://docs.celara.dev/chainops)
