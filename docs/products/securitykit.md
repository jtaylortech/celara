# SecurityKit

**Automated Security for Node Operators**

> Modern security automation for Web3 infrastructure — key management, threat detection, and compliance.

---

## Overview

SecurityKit is Vault + Falco for blockchain nodes. It provides automated key management, runtime security monitoring, and compliance reporting for decentralized infrastructure.

**Think:** Enterprise-grade security for systems that move billions in assets.

---

## Core Value Proposition

### The Problem

Security is the single greatest point of failure in decentralized infrastructure:
- Manual key management
- No runtime threat detection
- Compliance burden for custodians
- Configuration drift
- Reactive incident response

### The Solution

SecurityKit creates a professional security baseline:
- **Key Custody Policies** — HSM/KMS integrations
- **Agent-Based Monitoring** — Real-time threat detection
- **Compliance Automation** — SOC2, NIST, ISO reports
- **Configuration Enforcement** — Prevent drift
- **Incident Response** — Automated alerting and remediation

---

## Key Features

### 1. Key Management

**Supported Backends:**
- AWS KMS
- Google Cloud KMS
- Azure Key Vault
- HashiCorp Vault
- Hardware Security Modules (HSMs)
- Ledger/Trezor (cold storage)

**Key Lifecycle:**
```bash
# Generate validator keys with KMS
securitykit keys generate \
  --chain solana \
  --backend aws-kms \
  --region us-east-1

# Rotate keys
securitykit keys rotate \
  --validator ABC123 \
  --backup-to s3://backups/

# Audit key access
securitykit keys audit \
  --since 30d
```

### 2. Runtime Security

**Agent Capabilities:**
- Process monitoring (unauthorized binaries)
- Network monitoring (unexpected connections)
- File integrity monitoring (config changes)
- SSH access logging
- Signing anomaly detection

**Example Alert:**
```yaml
alert: unauthorized_ssh_access
severity: critical
details:
  source_ip: 203.0.113.42
  user: root
  timestamp: 2025-01-15T14:32:00Z
action: block_ip, notify_team
```

### 3. Compliance Automation

**Supported Frameworks:**
- SOC2 Type II
- NIST Cybersecurity Framework
- ISO 27001
- GDPR (data handling)
- Custom frameworks

**Auto-Generated Reports:**
- Access control audit logs
- Encryption status
- Patch management
- Incident response logs
- Configuration baselines

### 4. Policy Enforcement

```yaml
policies:
  - name: require_mfa
    scope: all_ssh_access
    enforcement: strict
  
  - name: key_rotation
    scope: validator_keys
    frequency: 90d
    enforcement: warn
  
  - name: network_isolation
    scope: validator_nodes
    allowed_ips: [10.0.0.0/8]
    enforcement: strict
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│            SecurityKit Dashboard                    │
│  (Alerts, Compliance Reports, Key Management)       │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │  Key    │    │  Policy   │   │Compliance│
   │  Vault  │    │  Engine   │   │  Engine  │
   └────┬────┘    └─────┬─────┘   └────┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │Security │    │ Validator │   │   RPC   │
   │  Agent  │───►│   Nodes   │   │  Nodes  │
   └─────────┘    └───────────┘   └─────────┘
```

---

## Use Cases

### Solo Validator

**Scenario:** Individual securing a single validator
**Solution:** Basic key management + SSH hardening
**Cost:** Free (OSS agent)

### Staking Provider

**Scenario:** Professional operator managing 50+ validators
**Solution:** Centralized key management + runtime monitoring
**Cost:** $99-$999/mo

### Custodian/Exchange

**Scenario:** Institution requiring SOC2 compliance
**Solution:** Full suite with compliance automation
**Cost:** $50K+/year

---

## Pricing

### OSS (Free)

- Security agent
- Basic key management
- Community support

### Pro ($99-$999/mo)

- Centralized dashboard
- KMS/HSM integrations
- Custom policies
- Priority support

### Enterprise ($50K+/year)

- Compliance automation
- Dedicated security engineer
- Custom integrations
- 24/7 support
- SLA guarantees

---

## Getting Started

### Prerequisites

- Running validator or RPC node
- AWS/GCP account (for KMS)

### Installation

```bash
# Install SecurityKit agent
curl -sSL https://get.celara.dev/securitykit | bash

# Initialize
securitykit init \
  --chain solana \
  --key-backend aws-kms

# Start monitoring
securitykit agent start
```

### Dashboard Access

Visit [securitykit.celara.dev](https://securitykit.celara.dev) to view alerts and compliance status.

---

## Security Baselines

### Validator Hardening

- ✅ SSH key-only authentication
- ✅ Fail2ban enabled
- ✅ Firewall rules (minimal ports)
- ✅ Automated security patches
- ✅ File integrity monitoring
- ✅ Process whitelisting

### Key Management

- ✅ Keys never touch disk unencrypted
- ✅ KMS/HSM for signing operations
- ✅ Automated key rotation
- ✅ Multi-signature support
- ✅ Audit logging

### Network Security

- ✅ VPC isolation
- ✅ Private subnets
- ✅ VPN/bastion access only
- ✅ DDoS protection
- ✅ Rate limiting

---

## Roadmap

**Q1 2025:**
- ✅ Security agent (Linux)
- ✅ AWS KMS integration
- ✅ Basic monitoring

**Q2 2025:**
- HSM support
- Multi-signature workflows
- Windows support

**Q3 2025:**
- Vault integration
- Compliance automation (SOC2)
- Advanced threat detection

**Q4 2025:**
- ML-based anomaly detection
- Automated remediation
- Custom framework support

---

## Community

- **GitHub:** [github.com/celara/securitykit](https://github.com/celara/securitykit)
- **Discord:** [discord.gg/celara](https://discord.gg/celara)
- **Docs:** [docs.celara.dev/securitykit](https://docs.celara.dev/securitykit)

---

## Related Products

- **[ChainOps](chainops.md)** — Deploy with security baselines
- **[ChainWatch](chainwatch.md)** — Monitor security events
- **[ValidatorHub](validatorhub.md)** — Track validator security posture

---

**Ready to secure your infrastructure?**

[Get Started →](https://celara.dev/securitykit)
