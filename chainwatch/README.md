# ChainWatch

Prometheus metrics exporter for EVM blockchain nodes.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## What it does

Expose blockchain node metrics as Prometheus gauges. Monitor sync status, peer count, gas prices, and client version across multiple EVM chains from a single exporter.

**Supported chains**: Ethereum · Base · Polygon · Arbitrum

## Quick Start

```bash
cd chainwatch
uv sync
cp .env.example .env

# Start Prometheus exporter
uv run chainwatch exporter --chain ethereum --port 9100

# One-shot health check
uv run chainwatch status --chain polygon

# List supported chains
uv run chainwatch chains
```

Metrics at `http://localhost:9100/metrics`

## Metrics

| Metric | Description | Labels |
|--------|-------------|--------|
| `chainwatch_sync_status` | 1=synced, 0=syncing | chain |
| `chainwatch_current_block` | Current block number | chain |
| `chainwatch_highest_block` | Highest known block | chain |
| `chainwatch_peer_count` | Connected peers | chain |
| `chainwatch_gas_price_gwei` | Gas price in gwei | chain |
| `chainwatch_node` | Client version info | chain |

## Grafana

Scrape config for `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: chainwatch
    static_configs:
      - targets: ['localhost:9100']
```

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

Part of [Celara](https://celara.dev) — open-source DevOps tooling for decentralized systems.
