# ChainOps

**Infrastructure-as-Code for Validators**

> Deploy, manage, and scale blockchain nodes with cloud-native discipline.

---

## Overview

ChainOps is the foundation of Celara — a DevOps framework for blockchain infrastructure. It provides opinionated IaC templates, CDK modules, and CLIs for deploying validators, RPC nodes, and indexers on AWS, GCP, or bare-metal clusters.

**Think:** Terraform for blockchain nodes.

---

## Core Value Proposition

### The Problem

Node operations today are artisanal and error-prone:
- Manual server provisioning
- Scattered bash scripts
- No version control
- Inconsistent security baselines
- Difficult to replicate across environments

### The Solution

ChainOps turns node operations into code:
- **Declarative Infrastructure** — Define validators like Terraform modules
- **Multi-Chain Ready** — Supports Solana, Ethereum, Cosmos, Substrate
- **Automated Rollouts** — Blue/green upgrades, backups, version management
- **Auditable** — Enforces best-practice baselines (network isolation, key mgmt, observability)

---

## Key Features

### 1. One-Command Deployments

```bash
celara deploy validator \
  --chain solana \
  --region us-east-1 \
  --instance-type c5.2xlarge
```

Provisions:
- EC2 instance with optimized networking
- EBS volumes with automated snapshots
- Security groups with minimal attack surface
- CloudWatch monitoring
- Automated updates via Systems Manager

### 2. Multi-Chain Support

**Supported Networks:**
- Ethereum (Geth, Nethermind, Besu)
- Solana (Validator + RPC)
- Cosmos SDK chains
- Polkadot/Substrate
- More coming via community contributions

### 3. Infrastructure-as-Code

```typescript
import { SolanaValidator } from '@celara/chainops-cdk';

new SolanaValidator(this, 'MainnetValidator', {
  network: 'mainnet-beta',
  instanceType: 'c5.2xlarge',
  monitoring: true,
  autoUpdates: true,
  backupRetention: 7,
});
```

### 4. Security Baselines

Every deployment includes:
- Network isolation (VPC + private subnets)
- Key management (AWS KMS or HSM)
- SSH hardening (key-only auth, fail2ban)
- Automated security patches
- Audit logging

### 5. Automated Operations

- **Blue/Green Deployments** — Zero-downtime upgrades
- **Automated Backups** — Scheduled snapshots with retention policies
- **Health Checks** — Automatic restart on failure
- **Version Management** — Pin or auto-update node software

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  ChainOps CLI                       │
│  (celara deploy, celara update, celara monitor)     │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │Terraform│    │  AWS CDK  │   │Pulumi   │
   │Templates│    │  Modules  │   │Modules  │
   └────┬────┘    └─────┬─────┘   └────┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │   AWS   │    │    GCP    │   │  Azure  │
   │         │    │           │   │         │
   └─────────┘    └───────────┘   └─────────┘
```

---

## Use Cases

### Solo Validator

**Scenario:** Individual running a Solana validator
**Solution:** One-command deployment with automated monitoring
**Cost:** ~$200/mo (compute + storage)

### Staking Provider

**Scenario:** Professional operator managing 50+ validators
**Solution:** Multi-region deployments with centralized monitoring
**Cost:** ChainOps Pro ($499/mo) + infrastructure costs

### L1 Foundation

**Scenario:** Protocol foundation supporting ecosystem validators
**Solution:** Reference architectures + grants for ChainOps adoption
**Cost:** Custom enterprise agreement

---

## Pricing

### OSS (Free)

- CLI + Terraform/CDK templates
- Community support (GitHub Discussions)
- Self-hosted

### ChainOps Pro ($49-$499/mo)

- Managed control plane
- Automated state management
- CI/CD integrations
- Priority support

### Enterprise ($25K+/year)

- Private deployment
- Custom integrations
- SLA guarantees
- Dedicated support

---

## Getting Started

### Prerequisites

- AWS account (or GCP/Azure)
- Node.js 20+
- Terraform or AWS CDK

### Installation

```bash
npm install -g @celara/chainops
celara init
```

### Quick Start

```bash
# Deploy a Solana validator
celara deploy validator \
  --chain solana \
  --network mainnet-beta \
  --region us-east-1

# Monitor status
celara status

# Update node software
celara update --version 1.18.0

# Destroy infrastructure
celara destroy
```

---

## Roadmap

**Q1 2025:**
- ✅ Solana + Ethereum support
- ✅ AWS CDK modules
- ✅ Basic monitoring integration

**Q2 2025:**
- Cosmos SDK support
- GCP + Azure support
- ChainOps Pro beta

**Q3 2025:**
- Polkadot/Substrate support
- Multi-region orchestration
- Advanced backup strategies

**Q4 2025:**
- Bare-metal support
- Custom chain integrations
- Enterprise features

---

## Community

- **GitHub:** [github.com/celara/chainops](https://github.com/celara/chainops)
- **Discord:** [discord.gg/celara](https://discord.gg/celara)
- **Docs:** [docs.celara.dev/chainops](https://docs.celara.dev/chainops)

---

## Related Products

- **[ChainWatch](chainwatch.md)** — Monitor your ChainOps deployments
- **[SecurityKit](securitykit.md)** — Secure your validator infrastructure
- **[ValidatorHub](validatorhub.md)** — Track validator economics

---

**Ready to professionalize your validator operations?**

[Get Started →](https://celara.dev/chainops)
