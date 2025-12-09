# ChainWatch

Observability for decentralized systems. Prometheus exporters for blockchain nodes.

**Status:** In Development  
**Supported Chains:** Ethereum

## What is ChainWatch?

ChainWatch provides production-grade monitoring for blockchain infrastructure. Export node metrics to Prometheus, visualize in Grafana, alert on issues.

## Quick Start

### Installation

```bash
cd chainwatch
uv sync
cp .env.example .env
```

### Run the Exporter

```bash
# Start Prometheus exporter on port 9100
uv run chainwatch exporter --chain ethereum

# Custom port and interval
uv run chainwatch exporter --chain ethereum --port 9200 --interval 30
```

### Check Node Status

```bash
uv run chainwatch status --chain ethereum
```

## Metrics Exported

| Metric | Type | Description |
|--------|------|-------------|
| `chainwatch_sync_status` | Gauge | Node sync status (1=synced, 0=syncing) |
| `chainwatch_current_block` | Gauge | Current block number |
| `chainwatch_highest_block` | Gauge | Highest known block number |
| `chainwatch_peer_count` | Gauge | Number of connected peers |
| `chainwatch_gas_price_gwei` | Gauge | Current gas price in gwei |
| `chainwatch_node_info` | Info | Node client version and chain |

## Configuration

Environment variables (or `.env` file):

```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
EXPORTER_PORT=9100
SCRAPE_INTERVAL=15
```

## Prometheus Integration

Add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'chainwatch'
    static_configs:
      - targets: ['localhost:9100']
```

## Grafana Dashboard

Import the dashboard from `dashboards/ethereum.json` (coming soon).

## CLI Reference

### `chainwatch exporter`

Run Prometheus metrics exporter.

| Option | Default | Description |
|--------|---------|-------------|
| `--chain` | `ethereum` | Chain to export metrics for |
| `--port` | `9100` | Prometheus metrics port |
| `--interval` | `15` | Scrape interval in seconds |

### `chainwatch status`

Check node status (one-shot metrics collection).

| Option | Default | Description |
|--------|---------|-------------|
| `--chain` | `ethereum` | Chain to check |

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy src/
```

## Roadmap

- [ ] Solana exporter
- [ ] Beacon chain (consensus) metrics
- [ ] Validator performance metrics
- [ ] Alert rules templates
- [ ] Grafana dashboards

## License

Apache 2.0

---

**Built by [Jarred](https://github.com/jtaylortech) & [Kofi](https://github.com/kofikwarba)**
