# ChainOps

**Infrastructure-as-Code for Blockchain Validators**

Deploy production-grade blockchain validators with one command. No manual setup, no configuration drift, no vendor lock-in.

```bash
chainops deploy ethereum --network mainnet
# ✓ Validator running in 15 minutes
```

---

## The Problem

Running blockchain validators today is unnecessarily complex:

- **Manual Setup Hell**: Hours of server configuration, networking, and security hardening
- **Configuration Drift**: What worked yesterday breaks today, no version control
- **Multi-Chain Chaos**: Every blockchain has different setup procedures
- **No Reproducibility**: Can't easily replicate or scale your infrastructure
- **Expensive Managed Services**: $500-2000/month with vendor lock-in

**The cost?** Missed rewards, slashing penalties, and countless hours of ops work.

---

## The Solution

ChainOps brings DevOps discipline to validator operations:

### One-Command Deployment
```bash
# Initialize configuration
chainops init ethereum --network mainnet

# Review and customize
vim chainops.yaml

# Deploy to AWS/GCP/bare metal
chainops deploy

# Monitor status
chainops status
```

### Infrastructure-as-Code
```yaml
# chainops.yaml
chain: ethereum
network: mainnet
provider: aws
region: us-east-1

compute:
  instance_type: t3.xlarge
  storage: 2000  # GB

monitoring:
  enabled: true
  alerts:
    - type: offline
      channel: slack
```

### Multi-Chain Support
- **Ethereum** (Geth, Nethermind, Besu)
- **Solana** (Solana validator)
- **Cosmos** (Gaiad, Osmosis, Juno)
- **Polygon** (Bor + Heimdall)
- **Arbitrum** (Nitro)
- **Base** (Optimism client)

### Security by Default
- Firewall rules (only necessary ports)
- SSH key-based auth (no passwords)
- Automatic security updates
- Key management best practices
- DDoS protection

### Cloud-Agnostic
- **AWS** (EC2, EBS, VPC)
- **GCP** (Compute Engine, Persistent Disk)
- **Azure** (Virtual Machines)
- **Bare Metal** (via Ansible)

---

## Why ChainOps?

### For Solo Validators
- **Save Time**: 15 minutes vs 8 hours manual setup
- **Reduce Risk**: Battle-tested configurations, no human error
- **Scale Easily**: Deploy 10 validators as easily as 1
- **Learn Fast**: Templates show best practices

### For Validator-as-a-Service Companies
- **Standardize Operations**: Same process across all chains
- **Reduce Costs**: Automate 90% of deployment work
- **Improve Reliability**: Infrastructure-as-code = fewer outages
- **Faster Onboarding**: New chains in days, not weeks

### For Protocols
- **Lower Barrier to Entry**: More validators = more decentralization
- **Better Documentation**: Code is documentation
- **Community Templates**: Validators share best practices
- **Faster Adoption**: Easy to run = more network participants

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        ChainOps CLI                          │
│  (Python + Typer - User-friendly command interface)         │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   Configuration Layer                        │
│  (YAML + Pydantic - Type-safe, validated configs)          │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                        │
│  (Terraform/CDK - Cloud resource provisioning)              │
│  • Compute instances (EC2, GCE, Azure VM)                   │
│  • Networking (VPC, subnets, security groups)               │
│  • Storage (EBS, persistent disks, 2TB+)                    │
│  • Monitoring (CloudWatch, Stackdriver)                     │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   Provisioning Layer                         │
│  (Ansible + Cloud-Init - Software installation)             │
│  • Validator client installation                            │
│  • Systemd service configuration                            │
│  • Monitoring agent setup                                   │
│  • Key management                                           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    Running Validator                         │
│  • Syncing blocks                                           │
│  • Attesting/proposing                                      │
│  • Earning rewards                                          │
│  • Monitored 24/7                                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- AWS/GCP/Azure account (or bare metal server)
- Cloud CLI configured (aws-cli, gcloud, or az)

### Installation
```bash
# Install via pip
pip install chainops

# Or install from source
git clone https://github.com/celara/chainops
cd chainops
pip install -e .
```

### Deploy Your First Validator

**Ethereum Mainnet:**
```bash
# Initialize configuration
chainops init ethereum --network mainnet

# Review configuration
cat chainops.yaml

# Estimate costs
chainops estimate
# Expected: ~$150/month on AWS

# Deploy
chainops deploy

# Check status
chainops status
# Validator: syncing (45% complete)
# ETA: 6 hours

# View logs
chainops logs --follow

# Once synced, check performance
chainops metrics
```

**Solana Mainnet:**
```bash
chainops init solana --network mainnet
chainops deploy
chainops status
```

---

## Configuration

### Basic Configuration
```yaml
# chainops.yaml
chain: ethereum
network: mainnet
provider: aws
region: us-east-1

compute:
  instance_type: t3.xlarge
  storage: 2000  # GB

monitoring:
  enabled: true
  prometheus: true
  grafana: true
  
alerts:
  - type: offline
    channel: slack
    webhook: https://hooks.slack.com/...
  - type: low_peers
    threshold: 10
    channel: email
```

### Advanced Configuration
```yaml
# chainops.yaml
chain: ethereum
network: mainnet
provider: aws
region: us-east-1

compute:
  instance_type: t3.xlarge
  storage: 2000
  spot_instances: true  # Save 70% on costs
  
networking:
  vpc_cidr: 10.0.0.0/16
  public_ip: true
  ddos_protection: true
  
validator:
  client: nethermind  # or geth, besu
  graffiti: "Powered by ChainOps"
  fee_recipient: "0x..."
  
backup:
  enabled: true
  schedule: "0 2 * * *"  # Daily at 2 AM
  retention: 7  # days
  
monitoring:
  enabled: true
  metrics_port: 9090
  dashboard_port: 3000
```

---

## CLI Reference

### Core Commands
```bash
# Initialize new validator
chainops init <chain> [options]
  --network mainnet|testnet
  --provider aws|gcp|azure|baremetal
  --region us-east-1

# Deploy infrastructure
chainops deploy [options]
  --auto-approve  # Skip confirmation
  --dry-run       # Show plan without deploying

# Check validator status
chainops status [options]
  --json          # Output as JSON
  --watch         # Continuous updates

# View logs
chainops logs [options]
  --follow        # Stream logs
  --tail 100      # Last N lines
  --level error   # Filter by level

# Destroy infrastructure
chainops destroy [options]
  --force         # Skip confirmation
```

### Management Commands
```bash
# Update validator software
chainops update [options]
  --version 1.2.3
  --auto-restart

# Backup validator data
chainops backup [options]
  --destination s3://bucket/path

# Restore from backup
chainops restore [options]
  --source s3://bucket/path

# Estimate costs
chainops estimate [options]
  --monthly       # Monthly estimate
  --yearly        # Yearly estimate

# Export configuration
chainops export [options]
  --format terraform|ansible
```

---

## Cost Breakdown

### Ethereum Validator (AWS)
| Component | Spec | Monthly Cost |
|-----------|------|--------------|
| EC2 Instance | t3.xlarge (4 vCPU, 16GB RAM) | $120 |
| EBS Storage | 2TB gp3 | $160 |
| Data Transfer | ~500GB/month | $45 |
| CloudWatch | Metrics + Logs | $10 |
| **Total** | | **~$335/month** |

**Cost Optimization:**
- Use Spot Instances: Save 70% ($100/month)
- Reserved Instances: Save 40% ($200/month)
- Bare Metal: $50-150/month (self-hosted)

### Solana Validator (AWS)
| Component | Spec | Monthly Cost |
|-----------|------|--------------|
| EC2 Instance | c5.2xlarge (8 vCPU, 16GB RAM) | $250 |
| EBS Storage | 1TB gp3 | $80 |
| Data Transfer | ~1TB/month | $90 |
| **Total** | | **~$420/month** |

---

## Business Model

### Open Source Core (Apache 2.0)
- CLI tool (free forever)
- Infrastructure templates (community-driven)
- Documentation and guides
- Community support

**Why open source?**
- Build trust through transparency
- Community contributions improve quality
- Faster adoption = larger ecosystem
- Validators need to trust their infrastructure

### Managed Service (ChainOps Cloud)
For teams that want zero-ops:
- **Starter**: $99/month - 1 validator, community support
- **Pro**: $299/month - 5 validators, priority support, SLA
- **Enterprise**: Custom - Unlimited validators, 24/7 support, custom SLA

**Revenue Model:**
- Managed control plane (hosted dashboard)
- One-click deployments
- Automated updates and maintenance
- Advanced monitoring and alerting
- Compliance reporting (SOC2, ISO 27001)

### Professional Services
- Custom validator setups
- Multi-chain infrastructure design
- Training and workshops
- Dedicated support contracts

**Target Market:**
- Validator-as-a-Service companies ($10K-50K/year)
- Protocols launching new chains ($25K-100K/year)
- Institutional validators ($50K-250K/year)

---

## Roadmap

### Q1 2026 - Foundation
- [x] Project structure
- [ ] Ethereum support (Geth, Nethermind)
- [ ] AWS provider
- [ ] Basic monitoring
- [ ] CLI v1.0
- [ ] Documentation site

### Q2 2026 - Multi-Chain
- [ ] Solana support
- [ ] Cosmos support
- [ ] GCP provider
- [ ] Advanced monitoring (Grafana dashboards)
- [ ] Backup/restore functionality

### Q3 2026 - Enterprise
- [ ] Azure provider
- [ ] Bare metal support
- [ ] High availability (multi-region)
- [ ] Disaster recovery
- [ ] Compliance reporting

### Q4 2026 - Scale
- [ ] ChainOps Cloud (managed service)
- [ ] Template marketplace
- [ ] Community templates
- [ ] Advanced automation
- [ ] 10+ chains supported

---

## Success Metrics

### Technical
- **Deployment Time**: <15 minutes (Ethereum)
- **Success Rate**: >95% (first-time deployments)
- **Uptime**: >99.5% (validator availability)
- **Cost**: <$200/month (optimized setup)

### Adoption
- **GitHub Stars**: 5,000+ (Year 1)
- **Active Deployments**: 1,000+ validators
- **Chains Supported**: 10+
- **Community Templates**: 50+

### Business
- **Open Source Users**: 10,000+ (Year 1)
- **Managed Service Customers**: 100+ (Year 1)
- **ARR**: $500K+ (Year 1)
- **Enterprise Contracts**: 10+ (Year 2)

---

## Contributing

We welcome contributions! ChainOps is built by the validator community, for the validator community.

**Ways to contribute:**
- Add support for new chains
- Improve existing templates
- Write documentation
- Report bugs
- Share your validator setup

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Community

- **Discord**: [discord.gg/celara](https://discord.gg/celara)
- **GitHub**: [github.com/celara/chainops](https://github.com/celara/chainops)
- **Docs**: [docs.celara.dev/chainops](https://docs.celara.dev/chainops)
- **Twitter**: [@celaradev](https://twitter.com/celaradev)

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

Open-core model: Core CLI and templates are open source. Managed cloud service is commercial.

---

## FAQ

**Q: Is ChainOps production-ready?**  
A: Currently in development. Ethereum support launching Q1 2026.

**Q: What clouds are supported?**  
A: AWS (Q1 2026), GCP (Q2 2026), Azure (Q3 2026), Bare Metal (Q3 2026).

**Q: How much does it cost?**  
A: Open source CLI is free. Cloud costs vary ($150-400/month). Managed service starts at $99/month.

**Q: Can I use my existing infrastructure?**  
A: Yes! ChainOps can manage existing validators or deploy new ones.

**Q: Is my validator key secure?**  
A: Yes. Keys never leave your infrastructure. ChainOps uses best practices for key management.

**Q: What if I need help?**  
A: Community support on Discord. Priority support available with managed service.

---

**Built with ⚡ by the Celara team**

*Making validator operations as simple as `git push`*
