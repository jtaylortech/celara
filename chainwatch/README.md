# ChainWatch

**Observability for Decentralized Systems**

Know your validators. Maximize your uptime. Track your economics.

```bash
chainwatch monitor --validator 0x1234...
# Real-time monitoring across all your validators
```

---

## The Problem

Blockchain infrastructure monitoring is broken:

- **Generic Tools Don't Understand Blockchain**: Datadog/Grafana miss attestations, proposals, slashing risks
- **Chain-Specific Tools Don't Scale**: Different dashboard for every chain you run
- **No Economic Visibility**: How much are you actually earning after costs?
- **Alert Fatigue**: 100 alerts/day, 99 are noise
- **Expensive Enterprise Solutions**: $500-2000/month for basic monitoring

**The cost?** Missed attestations = lost rewards. Downtime = slashing. No visibility = no optimization.

---

## The Solution

ChainWatch provides blockchain-native observability:

### Unified Dashboard
One view for all your validators across all chains:
```
┌─────────────────────────────────────────────────────────┐
│ ChainWatch Dashboard                                    │
├─────────────────────────────────────────────────────────┤
│ Ethereum Validators: 5 active, 0 offline               │
│ Solana Validators: 2 active, 0 offline                 │
│ Cosmos Validators: 3 active, 0 offline                 │
│                                                         │
│ Today's Performance:                                    │
│ • Attestations: 1,247 / 1,250 (99.76%)                │
│ • Proposals: 3 / 3 (100%)                              │
│ • Rewards: 0.045 ETH ($150)                            │
│ • Uptime: 99.98%                                       │
└─────────────────────────────────────────────────────────┘
```

### Blockchain-Native Metrics
Metrics that actually matter:
- **Validator Status**: Active, syncing, offline, slashed
- **Attestation Performance**: Success rate, inclusion distance
- **Block Proposals**: Proposed, missed, rewards
- **Economic Metrics**: Rewards earned, costs, ROI
- **Network Health**: Peer count, sync status, chain head
- **Infrastructure**: CPU, memory, disk, network

### Smart Alerting
Context-aware alerts that reduce noise:
```yaml
# Only alert on what matters
alerts:
  - name: Validator Offline
    severity: critical
    condition: status == "offline" for 5 minutes
    
  - name: Low Attestation Performance
    severity: warning
    condition: attestation_rate < 95% for 1 hour
    
  - name: Slashing Risk
    severity: critical
    condition: double_sign_detected
```

### Multi-Chain Support
- **Ethereum** (Consensus + Execution)
- **Solana**
- **Cosmos** (Hub, Osmosis, Juno)
- **Polygon**
- **Arbitrum**
- **Base**

---

## Why ChainWatch?

### For Solo Validators
- **Peace of Mind**: Know your validator is healthy 24/7
- **Maximize Rewards**: Optimize performance with data
- **Reduce Stress**: Smart alerts, not alert spam
- **Track Economics**: See real ROI after costs

### For Validator-as-a-Service Companies
- **Unified Operations**: Monitor 100+ validators from one dashboard
- **Customer Transparency**: Share performance dashboards with clients
- **Proactive Support**: Fix issues before customers notice
- **Economic Reporting**: Track profitability per validator

### For Protocols
- **Network Health**: Monitor overall validator performance
- **Identify Issues**: Detect network-wide problems early
- **Validator Relations**: Share performance data with operators
- **Decentralization Metrics**: Track validator distribution

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Validator Nodes                         │
│  (Ethereum, Solana, Cosmos validators running)              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                    Metrics Exporters                         │
│  (Prometheus exporters + custom collectors)                 │
│  • Beacon chain metrics                                     │
│  • Execution client metrics                                 │
│  • Validator client metrics                                 │
│  • Custom blockchain metrics                                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   ChainWatch Backend                         │
│  (FastAPI + PostgreSQL + TimescaleDB + Redis)               │
│  • Metrics aggregation                                      │
│  • Alert evaluation                                         │
│  • Economics calculations                                   │
│  • API for dashboards                                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                   ChainWatch Frontend                        │
│  (Next.js + React + Recharts)                               │
│  • Real-time dashboards                                     │
│  • Alert management                                         │
│  • Economics reports                                        │
│  • Mobile app                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Running validator(s)
- Docker + Docker Compose (for self-hosted)
- Or use ChainWatch Cloud (managed service)

### Self-Hosted Installation

**1. Install ChainWatch:**
```bash
# Clone repository
git clone https://github.com/celara/chainwatch
cd chainwatch

# Start services
docker-compose up -d

# Access dashboard
open http://localhost:3000
```

**2. Install Exporters on Validators:**
```bash
# Ethereum validator
curl -sSL https://get.chainwatch.dev/ethereum | bash

# Solana validator
curl -sSL https://get.chainwatch.dev/solana | bash

# Configure exporter
chainwatch-exporter config \
  --validator-address 0x1234... \
  --chainwatch-url http://your-chainwatch-server:8000
```

**3. Add Validator to Dashboard:**
```bash
# Via CLI
chainwatch add-validator \
  --chain ethereum \
  --address 0x1234... \
  --name "My Validator"

# Or via Web UI
# Navigate to Settings > Add Validator
```

### ChainWatch Cloud (Managed)

**1. Sign up:**
```bash
# Create account
chainwatch signup

# Login
chainwatch login
```

**2. Install agent on validator:**
```bash
# One-line install
curl -sSL https://cloud.chainwatch.dev/install | bash

# Agent auto-registers with your account
```

**3. View dashboard:**
```bash
# Open dashboard
chainwatch dashboard

# Or visit https://cloud.chainwatch.dev
```

---

## Features

### Real-Time Monitoring

**Validator Overview:**
- Status (active, syncing, offline)
- Uptime percentage
- Current balance
- Rewards earned (today, week, month, all-time)

**Performance Metrics:**
- Attestation success rate
- Attestation inclusion distance
- Block proposals (successful, missed)
- Sync committee participation

**Infrastructure Health:**
- CPU usage
- Memory usage
- Disk space
- Network bandwidth
- Peer count

### Alerting

**Built-in Alert Types:**
- Validator offline
- Missed attestations (threshold-based)
- Low peer count
- Disk space warning
- Sync issues
- Slashing risk detected

**Notification Channels:**
- Email
- Slack
- Discord
- Telegram
- PagerDuty
- Webhooks (custom integrations)

**Alert Configuration:**
```yaml
# alerts.yaml
alerts:
  - name: Critical Offline
    condition: status == "offline"
    duration: 5m
    severity: critical
    channels: [slack, pagerduty]
    
  - name: Performance Degradation
    condition: attestation_rate < 95%
    duration: 1h
    severity: warning
    channels: [email]
    
  - name: Disk Space Low
    condition: disk_usage > 85%
    duration: 30m
    severity: warning
    channels: [slack]
```

### Economics Tracking

**Revenue:**
- Attestation rewards
- Block proposal rewards
- Sync committee rewards
- MEV rewards (if applicable)

**Costs:**
- Infrastructure (compute, storage, network)
- Electricity (for bare metal)
- Maintenance time (estimated)

**Profitability:**
- Daily/weekly/monthly P&L
- ROI calculation
- Break-even analysis
- Forecasting

**Example Economics Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│ Validator Economics (Last 30 Days)                     │
├─────────────────────────────────────────────────────────┤
│ Revenue:                                                │
│ • Attestations:        0.45 ETH  ($1,500)             │
│ • Block Proposals:     0.12 ETH  ($400)               │
│ • Sync Committee:      0.03 ETH  ($100)               │
│ • Total Revenue:       0.60 ETH  ($2,000)             │
│                                                         │
│ Costs:                                                  │
│ • Infrastructure:                 ($335)               │
│ • Maintenance:                    ($100)               │
│ • Total Costs:                    ($435)               │
│                                                         │
│ Profit:                0.47 ETH  ($1,565)             │
│ ROI:                   360% annualized                 │
└─────────────────────────────────────────────────────────┘
```

### Historical Analysis

**Performance Trends:**
- Attestation rate over time
- Proposal success rate
- Uptime trends
- Reward trends

**Comparative Analysis:**
- Your performance vs network average
- Validator ranking
- Peer comparison

**Reporting:**
- Daily/weekly/monthly reports
- Export to CSV/PDF
- Custom date ranges
- Shareable links

---

## CLI Reference

```bash
# Add validator
chainwatch add-validator --chain ethereum --address 0x1234...

# List validators
chainwatch list

# Check status
chainwatch status [validator-id]

# View metrics
chainwatch metrics [validator-id] --period 24h

# Configure alerts
chainwatch alert add --type offline --channel slack

# Generate report
chainwatch report --period 30d --format pdf

# Export data
chainwatch export --format csv --period 90d
```

---

## API

ChainWatch provides a REST API for custom integrations:

```bash
# Get validator status
curl https://api.chainwatch.dev/v1/validators/0x1234.../status

# Get metrics
curl https://api.chainwatch.dev/v1/validators/0x1234.../metrics?period=24h

# Get economics
curl https://api.chainwatch.dev/v1/validators/0x1234.../economics?period=30d

# List alerts
curl https://api.chainwatch.dev/v1/alerts?validator=0x1234...
```

Full API documentation: [docs.chainwatch.dev/api](https://docs.chainwatch.dev/api)

---

## Business Model

### Open Source Core (Apache 2.0)
- Metrics exporters (free forever)
- Self-hosted backend (free forever)
- Basic dashboards
- Community support

**Why open source?**
- Validators need to trust their monitoring
- Community contributions improve coverage
- Faster adoption across chains
- Transparency builds credibility

### ChainWatch Cloud (Managed SaaS)

**Free Tier:**
- 1 validator
- 7 days data retention
- Basic alerts
- Community support

**Pro ($49/month):**
- 10 validators
- 90 days data retention
- Advanced alerts
- Email support
- Custom dashboards

**Team ($199/month):**
- 50 validators
- 1 year data retention
- Priority alerts
- Slack/Discord support
- Team collaboration
- API access

**Enterprise (Custom):**
- Unlimited validators
- Unlimited data retention
- 24/7 support
- Custom SLA
- On-premise deployment
- White-label option

### Revenue Model
- **SaaS Subscriptions**: $50-500/month per customer
- **Enterprise Contracts**: $10K-100K/year
- **API Access**: Usage-based pricing
- **Professional Services**: Custom dashboards, integrations

**Target Market:**
- Solo validators: 10,000+ (Free/Pro tier)
- Validator-as-a-Service: 500+ (Team/Enterprise)
- Protocols: 100+ (Enterprise)

---

## Roadmap

### Q1 2026 - Foundation
- [x] Project structure
- [ ] Ethereum exporter
- [ ] Backend API
- [ ] Basic dashboard
- [ ] Alert system
- [ ] Self-hosted deployment

### Q2 2026 - Multi-Chain
- [ ] Solana support
- [ ] Cosmos support
- [ ] Economics tracking
- [ ] Mobile app (iOS/Android)
- [ ] ChainWatch Cloud launch

### Q3 2026 - Advanced Features
- [ ] Predictive alerts (ML-based)
- [ ] Performance optimization recommendations
- [ ] Comparative analytics
- [ ] Custom dashboards
- [ ] API v2

### Q4 2026 - Enterprise
- [ ] White-label option
- [ ] On-premise deployment
- [ ] Advanced security (SSO, RBAC)
- [ ] Compliance reporting
- [ ] 10+ chains supported

---

## Success Metrics

### Technical
- **Metric Latency**: <30 seconds (real-time)
- **Alert Latency**: <60 seconds (critical)
- **Uptime**: >99.9%
- **False Positive Rate**: <5%

### Adoption
- **GitHub Stars**: 10,000+ (Year 1)
- **Validators Monitored**: 10,000+ (Year 1)
- **Chains Supported**: 6+ (Year 1)
- **Active Users**: 5,000+ (Year 1)

### Business
- **Free Users**: 8,000+ (Year 1)
- **Paid Customers**: 500+ (Year 1)
- **ARR**: $500K+ (Year 1)
- **Enterprise Contracts**: 20+ (Year 2)

---

## Integrations

### Existing Integrations
- **ChainOps**: Auto-configure monitoring for deployed validators
- **Prometheus**: Native Prometheus exporter
- **Grafana**: Pre-built dashboards
- **Slack**: Alert notifications
- **Discord**: Alert notifications
- **PagerDuty**: Incident management

### Planned Integrations
- **Telegram**: Alert notifications
- **Datadog**: Metrics forwarding
- **Splunk**: Log aggregation
- **Jira**: Incident tracking
- **Zapier**: Custom workflows

---

## Contributing

We welcome contributions! ChainWatch is built by the validator community.

**Ways to contribute:**
- Add support for new chains
- Improve exporters
- Build custom dashboards
- Write documentation
- Report bugs

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Community

- **Discord**: [discord.gg/celara](https://discord.gg/celara)
- **GitHub**: [github.com/celara/chainwatch](https://github.com/celara/chainwatch)
- **Docs**: [docs.chainwatch.dev](https://docs.chainwatch.dev)
- **Twitter**: [@celaradev](https://twitter.com/celaradev)

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

Open-core model: Core monitoring tools are open source. Managed cloud service is commercial.

---

## FAQ

**Q: Is ChainWatch production-ready?**  
A: Currently in development. Ethereum support launching Q2 2026.

**Q: Can I self-host ChainWatch?**  
A: Yes! Docker Compose deployment available. Or use ChainWatch Cloud for zero-ops.

**Q: How much does it cost?**  
A: Self-hosted is free. Cloud starts at $0 (1 validator) to $199/month (50 validators).

**Q: What chains are supported?**  
A: Ethereum (Q2 2026), Solana (Q2 2026), Cosmos (Q3 2026), more coming.

**Q: Can I monitor validators I don't operate?**  
A: Yes! Public validators can be monitored read-only.

**Q: Is my data secure?**  
A: Yes. Self-hosted = you control data. Cloud = encrypted at rest and in transit, SOC2 compliant.

---

**Built with ⚡ by the Celara team**

*Because downtime is expensive*
