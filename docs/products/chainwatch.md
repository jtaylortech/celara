# ChainWatch

**Observability for Decentralized Systems**

> Real-time monitoring, alerting, and analytics for blockchain infrastructure.

---

## Overview

ChainWatch is Datadog for blockchain infrastructure — pre-wired for on-chain metrics, validator performance, and consensus health. It provides unified dashboards, custom alerts, and performance analytics for node operators.

**Think:** Prometheus + Grafana, but blockchain-native.

---

## Core Value Proposition

### The Problem

Infrastructure without observability is trust without verification:
- No visibility into validator performance
- Manual log parsing
- Reactive incident response
- No historical data for optimization
- Difficult to benchmark against network

### The Solution

ChainWatch provides:
- **Unified Dashboards** — Network health, validator uptime, block production
- **Anomaly Detection** — Slashing, downtime, network partition risk
- **Custom Alerts** — Slack, Discord, PagerDuty, email
- **Historical Analytics** — Performance trends, revenue tracking
- **Multi-Chain Support** — Solana, Ethereum, Cosmos, and more

---

## Key Features

### 1. Real-Time Monitoring

**Validator Metrics:**
- Uptime percentage
- Block production rate
- Vote credits (Solana)
- Attestation effectiveness (Ethereum)
- Stake distribution
- Commission changes

**Network Metrics:**
- Consensus health
- Network latency
- Peer connectivity
- Chain height
- Fork detection

**Infrastructure Metrics:**
- CPU/memory/disk usage
- Network I/O
- RPC response times
- Database performance

### 2. Custom Alerting

```yaml
alerts:
  - name: validator_down
    condition: uptime < 99%
    severity: critical
    channels: [slack, pagerduty]
  
  - name: low_vote_credits
    condition: vote_credits < network_avg * 0.95
    severity: warning
    channels: [discord]
  
  - name: high_skip_rate
    condition: skip_rate > 5%
    severity: warning
    channels: [email]
```

### 3. Public Dashboards

Share validator performance with delegators:

```
https://chainwatch.celara.dev/validator/ABC123
```

Features:
- 30-day uptime history
- Block production stats
- Stake distribution
- Commission history
- Network ranking

### 4. Integration Ecosystem

**Native Integrations:**
- Prometheus (metrics export)
- Grafana (custom dashboards)
- OpenTelemetry (distributed tracing)
- Datadog (enterprise monitoring)
- PagerDuty (incident management)

**ChainOps Integration:**
Auto-configure monitoring for ChainOps deployments:

```bash
celara deploy validator --monitoring enabled
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              ChainWatch Dashboard                   │
│  (Web UI + Mobile App + API)                        │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │Metrics  │    │  Alerts   │   │Analytics│
   │Collector│    │  Engine   │   │ Engine  │
   └────┬────┘    └─────┬─────┘   └────┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │Validator│    │    RPC    │   │ Network │
   │ Nodes   │    │   Nodes   │   │  Data   │
   └─────────┘    └───────────┘   └─────────┘
```

---

## Use Cases

### Solo Validator

**Scenario:** Individual monitoring a single validator
**Solution:** Free public dashboard + basic alerts
**Cost:** Free

### Staking Provider

**Scenario:** Professional operator managing 50+ validators
**Solution:** Multi-validator dashboard + custom alerts + API access
**Cost:** $10/user/mo

### L1 Foundation

**Scenario:** Protocol foundation monitoring network health
**Solution:** Network-wide analytics + public transparency dashboard
**Cost:** Custom enterprise agreement

---

## Pricing

### Free Tier

- Public dashboards
- 7-day data retention
- Basic alerts (email)
- Community support

### Team ($10/user/mo)

- Private dashboards
- 90-day data retention
- Custom alerts (Slack, Discord, PagerDuty)
- API access
- Priority support

### Organization ($1,500+/mo)

- Unlimited dashboards
- 1-year data retention
- Advanced analytics
- Custom integrations
- SLA guarantees
- Dedicated support

### Enterprise (Custom)

- Multi-year data retention
- White-label dashboards
- On-premise deployment
- Custom development
- 24/7 support

---

## Getting Started

### Prerequisites

- Running validator or RPC node
- Prometheus or compatible metrics exporter

### Installation

```bash
# Install ChainWatch agent
npm install -g @celara/chainwatch

# Configure monitoring
chainwatch init \
  --chain solana \
  --validator-pubkey ABC123 \
  --api-key YOUR_API_KEY

# Start collecting metrics
chainwatch start
```

### Dashboard Access

Visit [chainwatch.celara.dev](https://chainwatch.celara.dev) and sign in with your API key.

---

## Metrics Reference

### Solana Validators

- `validator_uptime` — Percentage of epochs online
- `validator_vote_credits` — Vote credits earned
- `validator_skip_rate` — Percentage of skipped slots
- `validator_stake` — Total stake delegated
- `validator_commission` — Current commission rate
- `validator_delinquent` — Delinquency status

### Ethereum Validators

- `validator_balance` — Current balance
- `validator_effectiveness` — Attestation effectiveness
- `validator_proposals` — Block proposals
- `validator_slashings` — Slashing events
- `validator_sync_committee` — Sync committee participation

### Infrastructure

- `node_cpu_usage` — CPU utilization
- `node_memory_usage` — Memory utilization
- `node_disk_usage` — Disk utilization
- `node_network_io` — Network I/O
- `rpc_response_time` — RPC latency

---

## Roadmap

**Q1 2025:**
- ✅ Solana + Ethereum support
- ✅ Prometheus exporters
- ✅ Basic dashboards

**Q2 2025:**
- Public dashboard launch
- Cosmos SDK support
- Mobile app (iOS + Android)

**Q3 2025:**
- SaaS freemium launch
- Custom alert rules
- API access

**Q4 2025:**
- Advanced analytics
- Anomaly detection ML
- Network benchmarking

---

## Community

- **GitHub:** [github.com/celara/chainwatch](https://github.com/celara/chainwatch)
- **Discord:** [discord.gg/celara](https://discord.gg/celara)
- **Docs:** [docs.celara.dev/chainwatch](https://docs.celara.dev/chainwatch)

---

## Related Products

- **[ChainOps](chainops.md)** — Deploy infrastructure with built-in monitoring
- **[SecurityKit](securitykit.md)** — Security monitoring and alerting
- **[ChainETL](chainetl.md)** — Export metrics for custom analytics

---

**Ready to gain visibility into your infrastructure?**

[Get Started →](https://celara.dev/chainwatch)
