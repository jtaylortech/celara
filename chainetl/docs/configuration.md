# Configuration

## Environment Variables

ChainETL reads from environment variables or a `.env` file in the project root.

| Variable | Default | Description |
|----------|---------|-------------|
| `ETHEREUM_RPC_URL` | `https://eth.llamarpc.com` | Ethereum JSON-RPC endpoint |
| `BASE_RPC_URL` | `https://mainnet.base.org` | Base L2 RPC endpoint |
| `POLYGON_RPC_URL` | `https://polygon-rpc.com` | Polygon PoS RPC endpoint |
| `ARBITRUM_RPC_URL` | `https://arb1.arbitrum.io/rpc` | Arbitrum One RPC endpoint |
| `DATABASE_URL` | `postgresql://localhost/chainetl_dev` | PostgreSQL connection string |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

## Example `.env`

```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
BASE_RPC_URL=https://mainnet.base.org
POLYGON_RPC_URL=https://polygon-rpc.com
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
DATABASE_URL=postgresql://user:password@localhost/chainetl
LOG_LEVEL=INFO
```

## RPC Providers

Any EVM-compatible RPC endpoint works. Options:

- **Public (free)**: llamarpc.com, base.org, polygon-rpc.com
- **Alchemy**: `https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY`
- **Infura**: `https://mainnet.infura.io/v3/YOUR_KEY`
- **QuickNode**: Your dedicated endpoint
- **Self-hosted**: Geth, Erigon, Nethermind, Reth
