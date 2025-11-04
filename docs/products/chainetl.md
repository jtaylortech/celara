# ChainETL

**Blockchain Data Pipelines**

> Extract, transform, and load on-chain data into standardized schemas for analytics and reporting.

---

## Overview

ChainETL is an open-source data pipeline that ingests on-chain data into data warehouses and lakes. It provides ready-made connectors, schema normalization, and managed hosting for blockchain analytics.

**Think:** Airbyte + dbt for blockchain data.

---

## Core Value Proposition

### The Problem

On-chain data is powerful but difficult to operationalize:
- Custom scripts for each chain
- No standardized schemas
- Difficult to maintain
- Expensive to scale
- Hard to reproduce

### The Solution

ChainETL makes on-chain data operationally ready:
- **Ready-Made Connectors** — Solana, Ethereum, Cosmos
- **Schema Normalization** — DeFi, NFT, staking data
- **Data Lake Support** — S3, GCS, Azure Blob
- **Warehouse Integration** — Snowflake, BigQuery, Redshift
- **Custom Analytics** — SQL-ready data for dashboards

---

## Key Features

### 1. Pre-Built Connectors

**Supported Networks:**
- Ethereum (blocks, transactions, logs, traces)
- Solana (blocks, transactions, accounts, programs)
- Cosmos SDK (blocks, transactions, validators)
- Polygon, Arbitrum, Optimism
- More via community contributions

### 2. Schema Normalization

```sql
-- Standardized DeFi schema
SELECT
  protocol,
  pool_address,
  token_in,
  token_out,
  amount_in,
  amount_out,
  trader,
  timestamp
FROM defi.swaps
WHERE protocol = 'uniswap'
  AND timestamp > '2025-01-01';
```

### 3. Flexible Destinations

**Data Lakes:**
- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- MinIO (self-hosted)

**Data Warehouses:**
- Snowflake
- Google BigQuery
- Amazon Redshift
- Databricks

**Databases:**
- PostgreSQL
- MySQL
- TimescaleDB

### 4. Orchestration

```yaml
pipelines:
  - name: solana_mainnet
    source: solana
    network: mainnet-beta
    destination: snowflake
    schedule: "*/5 * * * *"  # Every 5 minutes
    tables:
      - blocks
      - transactions
      - token_transfers
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              ChainETL Orchestrator                  │
│  (Airflow / Dagster / Prefect)                      │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │Ethereum │    │  Solana   │   │ Cosmos  │
   │Connector│    │ Connector │   │Connector│
   └────┬────┘    └─────┬─────┘   └────┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                   ┌────▼────┐
                   │Transform│
                   │ Engine  │
                   └────┬────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐
   │   S3    │    │ Snowflake │   │BigQuery │
   │         │    │           │   │         │
   └─────────┘    └───────────┘   └─────────┘
```

---

## Use Cases

### Analytics Team

**Scenario:** Research team analyzing DeFi protocols
**Solution:** Ethereum connector → BigQuery → Looker dashboards
**Cost:** Free (OSS) + BigQuery costs

### DAO Treasury

**Scenario:** DAO tracking treasury transactions
**Solution:** Multi-chain connectors → Snowflake → custom reports
**Cost:** $15K/year (managed pipelines)

### Crypto Fund

**Scenario:** Fund analyzing on-chain metrics for investment decisions
**Solution:** Full-chain data → data lake → ML models
**Cost:** Custom enterprise agreement

---

## Pricing

### OSS (Free)

- All connectors
- Self-hosted orchestration
- Community support

### Managed Pipelines (Usage-Based)

- $0.10-$0.50/GB processed
- Hosted orchestration
- Automated scaling
- Priority support

### Enterprise (Custom)

- Dedicated infrastructure
- Custom connectors
- SLA guarantees
- 24/7 support

---

## Getting Started

### Prerequisites

- Python 3.10+
- Data warehouse account (Snowflake, BigQuery, etc.)
- Blockchain RPC endpoint

### Installation

```bash
pip install chainetl

# Initialize project
chainetl init my-pipeline

# Configure connector
chainetl configure \
  --source solana \
  --network mainnet-beta \
  --destination snowflake
```

### Run Pipeline

```bash
# One-time sync
chainetl sync \
  --start-block 100000000 \
  --end-block 100001000

# Continuous sync
chainetl sync --follow
```

---

## Data Schemas

### Ethereum

**Tables:**
- `blocks` — Block headers
- `transactions` — Transaction details
- `logs` — Event logs
- `traces` — Internal transactions
- `token_transfers` — ERC20/721/1155 transfers

### Solana

**Tables:**
- `blocks` — Block metadata
- `transactions` — Transaction details
- `instructions` — Program instructions
- `token_transfers` — SPL token transfers
- `account_updates` — Account state changes

### DeFi (Normalized)

**Tables:**
- `swaps` — DEX swaps
- `liquidity_events` — LP adds/removes
- `lending_events` — Borrow/lend/liquidate
- `staking_events` — Stake/unstake

---

## Roadmap

**Q1 2026:**
- Ethereum + Solana connectors
- Snowflake + BigQuery support
- Basic orchestration

**Q2 2026:**
- Cosmos SDK support
- dbt integration
- Managed hosting beta

**Q3 2026:**
- Real-time streaming
- Advanced transformations
- Custom connector SDK

**Q4 2026:**
- ML-ready datasets
- Cross-chain analytics
- Enterprise features

---

## Community

- **GitHub:** [github.com/celara/chainetl](https://github.com/celara/chainetl)
- **Discord:** [discord.gg/celara](https://discord.gg/celara)
- **Docs:** [docs.celara.dev/chainetl](https://docs.celara.dev/chainetl)

---

## Related Products

- **[ChainWatch](chainwatch.md)** — Visualize ChainETL data
- **[DAOForm](daoform.md)** — Use ChainETL for governance insights
- **[ValidatorHub](validatorhub.md)** — Track validator economics

---

**Ready to unlock on-chain data?**

[Get Started →](https://celara.dev/chainetl)
