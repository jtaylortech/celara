# Celara Product Architecture

**Last Updated:** November 4, 2025

## Overview

Celara operates as a unified ecosystem with interoperable modules, all open-source at the core but with enterprise and managed variants layered on top.

Think of it like **Terraform + Consul + Vault + Nomad, but for decentralized infrastructure.**

---

## Three-Pillar Strategy

### 1. Infrastructure (Build & Deploy)

**Focus:** Provision, monitor, and scale blockchain infrastructure

**Products:**
- **ChainOps** — Infrastructure-as-Code for validators
- **ChainETL** — Blockchain data pipelines
- **ValidatorHub** — Operator economics dashboard

### 2. Security (Protect & Govern)

**Focus:** Automated security checks and governance-as-code

**Products:**
- **SecurityKit** — Automated security for smart contracts
- **DAOForm** — Governance-as-Code

### 3. Platform (Operate & Scale)

**Focus:** Managed services for enterprise validator operations

**Products:**
- **ChainWatch** — Observability for decentralized systems
- **RunNode Cloud** — Managed control plane
- **Celara Network** — Federated validator mesh

---

## Product Details

### ChainOps — Infrastructure-as-Code for Validators

**Value Proposition:**
Deploy blockchain validators with cloud-native discipline. One-command deployments, multi-chain support, automated updates.

**Core Features:**
- Declarative node infrastructure (Terraform/CDK modules)
- Multi-chain support (Ethereum, Solana, Cosmos, Substrate)
- Automated rollouts and backups
- Auditable infrastructure baselines

**OSS Layer:** CLI + templates
**Paid Layer:** Managed control plane, state management, SLA support

**Target Users:** Validators, staking providers, infrastructure engineers

---

### ChainWatch — Observability for Decentralized Systems

**Value Proposition:**
Datadog for blockchain infrastructure. Real-time monitoring, custom alerts, performance analytics.

**Core Features:**
- Unified dashboard for network health
- Validator uptime and block production metrics
- Anomaly detection for slashing and downtime
- Prometheus/Grafana/OpenTelemetry integration

**OSS Layer:** Metrics exporters + dashboards
**Paid Layer:** Hosted dashboards, custom alerts, data retention

**Target Users:** Node operators, DevOps teams, protocol foundations

---

### SecurityKit — Automated Security for Node Operators

**Value Proposition:**
Vault + Falco for blockchain nodes. Automated key management, threat detection, compliance reporting.

**Core Features:**
- Key custody policies (HSM/KMS integration)
- Agent-based security telemetry
- Auto-generated compliance reports (SOC2, NIST, ISO)
- Real-time alerting on configuration drift

**OSS Layer:** Security agent
**Paid Layer:** Orchestration, compliance modules, audit support

**Target Users:** Custodians, exchanges, staking providers

---

### ChainETL — Blockchain Data Pipelines

**Value Proposition:**
Airbyte + dbt for blockchain data. Extract on-chain data to warehouses with standardized schemas.

**Core Features:**
- Ready-made ETL connectors (Solana, Ethereum, Cosmos)
- Schema normalization for DeFi, NFT, staking data
- Data lake and warehouse support (S3, Snowflake, BigQuery)
- Custom analytics dashboards

**OSS Layer:** Connectors
**Paid Layer:** Managed pipelines, usage-based billing

**Target Users:** Analytics teams, research labs, DAOs, funds

---

### DAOForm — Governance-as-Code

**Value Proposition:**
Notion for DAOs. Off-chain coordination with on-chain execution. Governance proposals, treasury management, contributor ops.

**Core Features:**
- Governance proposal builder (off-chain draft → on-chain execution)
- Contributor management (roles, vesting, bounties)
- Integration with Gnosis Safe, Snapshot, Discord/Slack
- DAO constitution templates

**OSS Layer:** Base templates + contract interfaces
**Paid Layer:** Hosted dashboard, integrations

**Target Users:** DAOs, protocol foundations, community managers

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Celara Cloud                         │
│              (Unified Management Console)               │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │ ChainOps│       │ChainWatch │     │SecurityKit│
   │         │       │           │     │           │
   │ Deploy  │◄──────┤ Monitor   │────►│  Secure   │
   └────┬────┘       └─────┬─────┘     └─────┬─────┘
        │                  │                  │
        │            ┌─────▼─────┐            │
        │            │ ChainETL  │            │
        └───────────►│           │◄───────────┘
                     │  Analyze  │
                     └─────┬─────┘
                           │
                     ┌─────▼─────┐
                     │  DAOForm  │
                     │           │
                     │  Govern   │
                     └───────────┘
```

**Integration Points:**
- ChainOps deployments auto-configure ChainWatch monitoring
- SecurityKit policies enforce ChainOps infrastructure baselines
- ChainETL ingests metrics from ChainWatch
- DAOForm uses ChainETL data for governance insights

---

## Open-Core Strategy

**Core Principle:** Open-source builds trust; managed services monetize reliability.

| Layer | Description | Monetization |
|-------|-------------|--------------|
| **OSS Core** | CLIs, templates, exporters, agents | Free (community growth) |
| **SaaS** | Hosted dashboards, alerting, integrations | Usage-based monthly pricing |
| **Enterprise** | Private deployment, compliance, SLAs | Annual contracts ($20K-$100K+) |
| **Advisory** | Integration projects, deployment support | One-time + retainer |

---

## Why This Architecture Matters

**Composability:** Each product works standalone or as part of the suite
**Interoperability:** Shared data models and APIs enable cross-product workflows
**Defensibility:** Network effects compound as adoption grows
**Scalability:** Open-core model allows community-driven expansion

---

## Next Steps

See:
- [Business Model](business-model.md) for monetization details
- [GTM Playbook](gtm-playbook.md) for go-to-market strategy
- [Phase Map](phase-map.md) for development timeline
