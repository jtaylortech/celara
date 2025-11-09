# SecurityKit

**Automated Security for Node Operators**

Continuous security scanning and hardening for blockchain infrastructure. Catch vulnerabilities before they cost you.

```bash
securitykit scan --target validator.example.com
# Security Score: 87/100 (Good)
# 3 issues found, 2 auto-fixable
```

---

## The Problem

Blockchain security is high-stakes and complex:

- **Validators Hold Significant Value**: $100K-10M+ in staked assets at risk
- **Smart Contracts Are Immutable**: One bug = permanent loss
- **Security Expertise Is Scarce**: $300-500/hour for audits
- **Manual Audits Are One-Time**: Threats evolve, audits don't
- **Generic Tools Miss Blockchain Issues**: Slither/Mythril don't check infrastructure

**The cost?** Slashing, hacks, lost funds, reputation damage.

Real examples:
- Validator slashed: -32 ETH ($100K+)
- Smart contract exploit: $10M+ drained
- SSH compromise: Validator keys stolen
- Misconfigured firewall: DDoS attack

---

## The Solution

SecurityKit provides continuous, automated security:

### Pre-Deployment Scanning
Catch issues before they go live:
```bash
# Scan smart contract
securitykit analyze token.sol
# ✓ No reentrancy vulnerabilities
# ✓ Access control properly configured
# ⚠ Gas optimization: 3 issues found
# ✗ Missing event emissions: 2 functions

# Scan infrastructure
securitykit scan --target validator.example.com
# ✓ SSH key-based auth enabled
# ✓ Firewall configured correctly
# ⚠ OS patches 15 days old
# ✗ Root SSH access enabled (CRITICAL)
```

### Continuous Monitoring
24/7 security checks:
- Configuration drift detection
- Vulnerability scanning (CVE database)
- Threat intelligence integration
- Compliance monitoring (SOC2, ISO 27001)

### Automated Remediation
Fix common issues automatically:
```bash
securitykit fix --auto
# Fixing: Disable root SSH access... ✓
# Fixing: Update firewall rules... ✓
# Fixing: Apply OS patches... ✓
# Manual review required: 1 issue
```

### Compliance Reporting
Generate audit-ready reports:
```bash
securitykit report --format pdf --compliance soc2
# Generated: security-report-2026-01-15.pdf
# SOC2 Compliance: 94% (47/50 controls)
```

---

## Why SecurityKit?

### For Solo Validators
- **Protect Your Stake**: Prevent slashing and key theft
- **Learn Security**: Understand what matters
- **Save Money**: Avoid expensive audits
- **Sleep Better**: Know you're secure

### For Validator-as-a-Service Companies
- **Scale Security**: Secure 100+ validators consistently
- **Customer Trust**: Show security posture to clients
- **Compliance**: SOC2/ISO 27001 ready
- **Reduce Risk**: Prevent incidents before they happen

### For Smart Contract Developers
- **Pre-Deployment Checks**: Catch bugs before mainnet
- **Continuous Monitoring**: Detect new vulnerabilities
- **Gas Optimization**: Save users money
- **Audit Preparation**: Clean reports for auditors

### For Protocols
- **Validator Security**: Ensure operators follow best practices
- **Network Health**: Reduce slashing events
- **Reputation**: Secure network = more adoption
- **Compliance**: Help validators meet requirements

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Scan Targets                          │
│  • Validator infrastructure (SSH, firewall, OS)             │
│  • Smart contracts (Solidity, Rust)                         │
│  • Dependencies (npm, cargo, pip)                           │
│  • Configuration files (systemd, nginx, etc)                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                      SecurityKit Scanners                    │
│  (Python + Rust - Fast, comprehensive scanning)             │
│  • Infrastructure scanner (SSH, firewall, keys)             │
│  • Smart contract analyzer (Slither, Mythril)               │
│  • Dependency checker (CVE database)                        │
│  • Configuration auditor (CIS benchmarks)                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                     Analysis Engine                          │
│  (Python + PostgreSQL - Risk scoring & intelligence)        │
│  • Vulnerability database (NVD, GitHub Security)            │
│  • Risk scoring (CVSS + custom blockchain metrics)         │
│  • Compliance mapping (SOC2, ISO 27001, CIS)               │
│  • Threat intelligence (emerging attacks)                   │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   Remediation Engine                         │
│  (Python + Ansible - Automated fixes)                       │
│  • Auto-fix common issues                                   │
│  • Patch management                                         │
│  • Configuration updates                                    │
│  • Rollback capability                                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    Dashboard & Reports                       │
│  (Next.js + React - Security visibility)                    │
│  • Security score (0-100)                                   │
│  • Vulnerability tracking                                   │
│  • Compliance reports                                       │
│  • Alert management                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- SSH access to validators (for infrastructure scans)
- Solidity/Rust contracts (for smart contract scans)

### Installation

```bash
# Install via pip
pip install securitykit

# Or install from source
git clone https://github.com/celara/securitykit
cd securitykit
pip install -e .
```

### Scan Your First Validator

**Infrastructure Scan:**
```bash
# Scan validator
securitykit scan --target validator.example.com

# Output:
# ┌─────────────────────────────────────────────┐
# │ Security Scan Results                       │
# ├─────────────────────────────────────────────┤
# │ Target: validator.example.com               │
# │ Scan Time: 2026-01-15 10:30:00             │
# │ Security Score: 87/100 (Good)              │
# │                                             │
# │ Critical Issues: 1                          │
# │ • Root SSH access enabled                   │
# │                                             │
# │ Warnings: 2                                 │
# │ • OS patches 15 days old                    │
# │ • Firewall allows unnecessary port 8080     │
# │                                             │
# │ Passed Checks: 15                           │
# └─────────────────────────────────────────────┘

# Auto-fix issues
securitykit fix --target validator.example.com --auto
```

**Smart Contract Scan:**
```bash
# Analyze contract
securitykit analyze contracts/Token.sol

# Output:
# ┌─────────────────────────────────────────────┐
# │ Smart Contract Analysis                     │
# ├─────────────────────────────────────────────┤
# │ Contract: Token.sol                         │
# │ Security Score: 92/100 (Excellent)         │
# │                                             │
# │ Critical Issues: 0                          │
# │                                             │
# │ Warnings: 3                                 │
# │ • Gas optimization: Use ++i instead of i++  │
# │ • Missing event: transfer() should emit     │
# │ • Unchecked return: approve() return value  │
# │                                             │
# │ Passed Checks: 25                           │
# └─────────────────────────────────────────────┘

# Generate detailed report
securitykit analyze contracts/Token.sol --report audit-report.pdf
```

---

## Features

### Infrastructure Security

**SSH Configuration:**
- Key-based authentication enforced
- Root login disabled
- Strong ciphers only
- Fail2ban enabled
- SSH key rotation

**Firewall Rules:**
- Only necessary ports open
- Rate limiting configured
- DDoS protection enabled
- Geographic restrictions (optional)

**OS Security:**
- Patches up to date (<30 days)
- Unnecessary services disabled
- Secure boot enabled
- Disk encryption verified

**Key Management:**
- Validator keys properly secured
- Backup keys encrypted
- Key rotation schedule
- Hardware security module (HSM) support

**Monitoring:**
- Security event logging
- Intrusion detection
- File integrity monitoring
- Anomaly detection

### Smart Contract Security

**Vulnerability Detection:**
- Reentrancy attacks
- Integer overflow/underflow
- Access control issues
- Front-running vulnerabilities
- Timestamp dependence
- Unchecked external calls

**Code Quality:**
- Gas optimization
- Code complexity
- Test coverage
- Documentation completeness

**Best Practices:**
- Event emission
- Error handling
- Upgrade patterns
- Emergency stops

**Compliance:**
- ERC standards compliance
- Security patterns (Checks-Effects-Interactions)
- OpenZeppelin usage
- Audit readiness

### Dependency Security

**Vulnerability Scanning:**
- CVE database checks
- GitHub Security Advisories
- Known exploits
- Outdated packages

**License Compliance:**
- License compatibility
- Copyleft detection
- Attribution requirements

**Supply Chain:**
- Package integrity
- Maintainer reputation
- Dependency tree analysis

---

## Security Rules

### Infrastructure Rules

**Critical:**
- No root SSH access
- SSH key-based auth only
- Firewall configured
- OS patches <30 days old
- Validator keys encrypted

**High:**
- Fail2ban enabled
- Disk encryption enabled
- Monitoring configured
- Backup system active
- DDoS protection enabled

**Medium:**
- Strong SSH ciphers
- Unnecessary services disabled
- Log rotation configured
- Time synchronization (NTP)
- Secure boot enabled

**Low:**
- SSH banner configured
- Hostname properly set
- Timezone configured
- Locale configured

### Smart Contract Rules

**Critical:**
- No reentrancy vulnerabilities
- Access control properly configured
- No integer overflow/underflow
- External calls checked
- No selfdestruct without protection

**High:**
- Events emitted for state changes
- Error messages clear
- Gas limits reasonable
- Upgrade mechanism secure
- Emergency stop implemented

**Medium:**
- Gas optimizations applied
- Code complexity reasonable
- Test coverage >80%
- Documentation complete
- OpenZeppelin patterns used

**Low:**
- Naming conventions followed
- Comments present
- Unused code removed
- Formatting consistent

---

## CLI Reference

```bash
# Infrastructure scanning
securitykit scan --target <host>
  --port 22                    # SSH port
  --user ubuntu                # SSH user
  --key ~/.ssh/id_rsa         # SSH key
  --output json               # Output format

# Smart contract analysis
securitykit analyze <contract.sol>
  --solc-version 0.8.20       # Solidity version
  --optimize                  # Enable optimizations
  --report audit-report.pdf   # Generate report

# Dependency checking
securitykit deps check
  --package-manager npm       # npm, cargo, pip
  --fix                       # Auto-update safe deps

# Continuous monitoring
securitykit monitor
  --schedule daily            # Scan frequency
  --targets targets.yaml      # Target list
  --alerts slack              # Alert channel

# Auto-remediation
securitykit fix --target <host>
  --auto                      # Auto-fix safe issues
  --dry-run                   # Show what would be fixed
  --rollback                  # Rollback last fix

# Compliance reporting
securitykit report
  --compliance soc2           # SOC2, ISO27001, CIS
  --format pdf                # pdf, html, json
  --period 90d                # Reporting period
```

---

## Configuration

### Security Policy
```yaml
# securitykit.yaml
policy:
  infrastructure:
    ssh:
      root_login: false
      password_auth: false
      key_types: [ed25519, rsa]
      min_key_size: 4096
    
    firewall:
      default_policy: deny
      allowed_ports: [22, 30303, 9000]
      rate_limiting: true
    
    os:
      max_patch_age: 30  # days
      required_services: [fail2ban, ufw]
      
  smart_contracts:
    solidity:
      version: ">=0.8.0"
      optimizer: true
      runs: 200
    
    checks:
      reentrancy: error
      overflow: error
      access_control: error
      gas_optimization: warning
      
  compliance:
    frameworks: [soc2, iso27001]
    evidence_retention: 365  # days
```

### Scan Targets
```yaml
# targets.yaml
targets:
  - name: Ethereum Validator 1
    type: infrastructure
    host: eth-validator-1.example.com
    port: 22
    user: ubuntu
    key: ~/.ssh/validator-key
    
  - name: Token Contract
    type: smart_contract
    path: contracts/Token.sol
    chain: ethereum
    
  - name: Backend Dependencies
    type: dependencies
    path: backend/
    package_manager: npm
```

---

## Business Model

### Open Source Core (Apache 2.0)
- CLI scanner (free forever)
- Security rules (community-driven)
- Basic reporting
- Community support

**Why open source?**
- Security through transparency
- Community contributions improve coverage
- Build trust with validators
- Faster adoption

### SecurityKit Cloud (Managed SaaS)

**Free Tier:**
- 1 target (validator or contract)
- Weekly scans
- Basic reports
- Community support

**Pro ($99/month):**
- 10 targets
- Daily scans
- Auto-remediation
- Priority support
- Compliance reports

**Team ($299/month):**
- 50 targets
- Continuous monitoring
- Advanced remediation
- Team collaboration
- API access
- Custom rules

**Enterprise (Custom):**
- Unlimited targets
- Real-time monitoring
- 24/7 support
- Custom SLA
- On-premise deployment
- White-label option
- Dedicated security engineer

### Professional Services
- **Security Audits**: $5K-50K per audit
- **Penetration Testing**: $10K-100K per engagement
- **Security Training**: $2K-10K per workshop
- **Incident Response**: $500-1000/hour

**Target Market:**
- Solo validators: 5,000+ (Free/Pro)
- Validator-as-a-Service: 200+ (Team/Enterprise)
- Smart contract projects: 1,000+ (Pro/Team)
- Protocols: 50+ (Enterprise)

---

## Roadmap

### Q1 2026 - Foundation
- [x] Project structure
- [ ] Infrastructure scanner
- [ ] Basic security rules
- [ ] CLI v1.0
- [ ] Documentation

### Q2 2026 - Smart Contracts
- [ ] Solidity analyzer
- [ ] Rust analyzer (Solana/Cosmos)
- [ ] Gas optimization
- [ ] Audit report generation
- [ ] SecurityKit Cloud launch

### Q3 2026 - Automation
- [ ] Auto-remediation engine
- [ ] Continuous monitoring
- [ ] Threat intelligence
- [ ] Compliance automation
- [ ] API v1

### Q4 2026 - Enterprise
- [ ] On-premise deployment
- [ ] White-label option
- [ ] Advanced analytics
- [ ] Custom rule engine
- [ ] 24/7 support

---

## Success Metrics

### Technical
- **Scan Time**: <5 minutes (full infrastructure)
- **False Positive Rate**: <5%
- **Vulnerability Detection**: >95% (known CVEs)
- **Auto-Fix Success**: >90%

### Adoption
- **GitHub Stars**: 5,000+ (Year 1)
- **Active Users**: 2,000+ (Year 1)
- **Targets Scanned**: 10,000+ (Year 1)
- **Vulnerabilities Found**: 50,000+ (cumulative)

### Business
- **Free Users**: 1,500+ (Year 1)
- **Paid Customers**: 200+ (Year 1)
- **ARR**: $300K+ (Year 1)
- **Enterprise Contracts**: 10+ (Year 2)

---

## Contributing

We welcome contributions! Security is a community effort.

**Ways to contribute:**
- Add security rules
- Improve scanners
- Report false positives
- Write documentation
- Share threat intelligence

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Community

- **Discord**: [discord.gg/celara](https://discord.gg/celara)
- **GitHub**: [github.com/celara/securitykit](https://github.com/celara/securitykit)
- **Docs**: [docs.securitykit.dev](https://docs.securitykit.dev)
- **Security**: [security@celara.dev](mailto:security@celara.dev)

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

Open-core model: Core scanner is open source. Managed cloud service is commercial.

---

## FAQ

**Q: Is SecurityKit production-ready?**  
A: Currently in development. Infrastructure scanner launching Q2 2026.

**Q: Can SecurityKit prevent all attacks?**  
A: No tool can guarantee 100% security. SecurityKit reduces risk significantly but should be part of a defense-in-depth strategy.

**Q: How often should I scan?**  
A: Infrastructure: daily. Smart contracts: before every deployment. Dependencies: weekly.

**Q: Will auto-fix break my validator?**  
A: Auto-fix only applies safe, tested fixes. Critical changes require manual approval. Rollback is always available.

**Q: Can I use SecurityKit for audits?**  
A: Yes! Reports are audit-ready. However, we recommend professional audits for high-value contracts.

**Q: Is my data secure?**  
A: Yes. Self-hosted = you control data. Cloud = encrypted, SOC2 compliant, never shared.

---

**Built with ⚡ by the Celara team**

*Because security is not optional*
