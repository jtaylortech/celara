# Base L2 Sync Examples

This guide shows how to sync Base L2 blockchain data using ChainETL.

## About Base L2

Base is an Ethereum Layer 2 (L2) solution built on Optimism's OP Stack. It's EVM-compatible, meaning it uses the same RPC interface as Ethereum but with:
- Lower transaction fees
- Faster block times (~2 seconds)
- L2-specific metadata (L1 batch info)

## Prerequisites

1. Set up your environment:
```bash
cp .env.example .env
# Edit .env and set BASE_RPC_URL and DATABASE_URL
```

2. Initialize the database:
```bash
# Make sure PostgreSQL is running
psql -c "CREATE DATABASE chainetl_dev;"
```

## Basic Usage

### Sync a Single Block

Sync block 10000000 from Base L2:
```bash
chainetl sync --chain base --start-block 10000000
```

### Sync Multiple Blocks

Sync 100 blocks starting from block 10000000:
```bash
chainetl sync --chain base --start-block 10000000 --count 100
```

### Sync Latest Blocks

Sync the latest block:
```bash
chainetl sync --chain base
```

### Resume from Checkpoint

Continue syncing from where you left off:
```bash
chainetl sync --chain base --resume --count 1000
```

### Batch Syncing

Sync large ranges efficiently:
```bash
# Sync 10,000 blocks (faster than Ethereum due to 2s block time)
chainetl sync --chain base --start-block 10000000 --count 10000
```

## Monitoring

### Check Sync Status

View current sync progress:
```bash
chainetl status --chain base
```

Example output:
```
ChainETL Status:
  Chain: base
  Status: Ready
  RPC: https://mainnet.base.org
  Database: postgresql://localhost/chainetl_dev

Checkpoint:
  Last synced block: 10000999
  Last synced hash: 0x4c7bfdcf18428770bd82d9f0e5a9b8e3d1c2f6a8b9c0d1e2f3a4b5c6d7e8f9a0
  Synced at: 2025-11-16 00:22:02.395782
  Status: active
```

## Multi-Chain Setup

### Running Ethereum and Base Together

You can sync both chains simultaneously with independent checkpoints:

```bash
# Terminal 1: Ethereum sync
chainetl sync --chain ethereum --resume --count 100

# Terminal 2: Base sync
chainetl sync --chain base --resume --count 500
```

Each chain maintains its own checkpoint, so they won't interfere with each other.

### Check Both Chains

```bash
chainetl status --chain ethereum
chainetl status --chain base
```

## Production Setup

### Continuous Syncing

Run in a loop to keep syncing new blocks:
```bash
while true; do
  chainetl sync --chain base --resume --count 500
  sleep 30  # Wait 30 seconds (Base has ~2s blocks)
done
```

### Using systemd (Linux)

Create a systemd service for continuous syncing:

```ini
[Unit]
Description=ChainETL Base L2 Sync
After=network.target postgresql.service

[Service]
Type=simple
User=chainetl
WorkingDirectory=/opt/chainetl
ExecStart=/usr/local/bin/chainetl sync --chain base --resume --count 500
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

## Base L2 Specifics

### Block Times

- Base produces blocks every ~2 seconds
- Much faster than Ethereum's ~12 seconds
- Adjust your sync frequency accordingly

### RPC Endpoints

Recommended Base L2 RPC providers:
- `https://mainnet.base.org` (official)
- `https://base.llamarpc.com` (LlamaNodes)
- `https://base.publicnode.com` (PublicNode)

### L2-Specific Fields

Base blocks may contain additional L2-specific metadata:
- `l1BlockNumber`: The L1 (Ethereum) block when this L2 block was posted
- `l1BatchNumber`: The batch number on L1
- Deposit transactions (from L1 to L2)
- Withdrawal transactions (from L2 to L1)

Note: ChainETL currently uses the standard block model. Advanced L2 features (deposits/withdrawals) are planned for future releases.

## Performance Tips

1. **Higher Throughput**: Base's faster blocks mean you can sync more blocks per second
2. **Batch Size**: Use larger --count values (500-1000) for efficient syncing
3. **RPC Selection**: Official Base RPC is recommended for best reliability
4. **Database**: Same optimization tips as Ethereum apply

## Troubleshooting

### RPC Issues

Base's official RPC is generally reliable, but if you encounter issues:
- Try alternative RPC providers
- Check Base network status at status.base.org
- Ensure your RPC URL is correct in .env

### Checkpoint Issues

Reset Base checkpoint if needed:
```sql
DELETE FROM checkpoints WHERE chain = 'base';
```

### Comparing with Ethereum

If syncing both chains, note that:
- Base blocks are numbered independently from Ethereum
- Checkpoints are stored separately per chain
- Database stores blocks from both chains in the same table
