# Ethereum Sync Examples

This guide shows how to sync Ethereum blockchain data using ChainETL.

## Prerequisites

1. Set up your environment:
```bash
cp .env.example .env
# Edit .env and set ETHEREUM_RPC_URL and DATABASE_URL
```

2. Initialize the database:
```bash
# Make sure PostgreSQL is running
psql -c "CREATE DATABASE chainetl_dev;"
```

## Basic Usage

### Sync a Single Block

Sync block 18000000 from Ethereum mainnet:
```bash
chainetl sync --chain ethereum --start-block 18000000
```

### Sync Multiple Blocks

Sync 100 blocks starting from block 18000000:
```bash
chainetl sync --chain ethereum --start-block 18000000 --count 100
```

### Sync Latest Blocks

Sync the latest block (no start-block specified):
```bash
chainetl sync --chain ethereum
```

### Resume from Checkpoint

Continue syncing from where you left off:
```bash
chainetl sync --chain ethereum --resume --count 1000
```

### Batch Syncing

Sync large ranges efficiently:
```bash
# Sync 10,000 blocks
chainetl sync --chain ethereum --start-block 18000000 --count 10000
```

## Monitoring

### Check Sync Status

View current sync progress:
```bash
chainetl status --chain ethereum
```

Example output:
```
ChainETL Status:
  Chain: ethereum
  Status: Ready
  RPC: https://eth.llamarpc.com
  Database: postgresql://localhost/chainetl_dev

Checkpoint:
  Last synced block: 18000999
  Last synced hash: 0x7f7889c3686d7f560dd690aeb2a10b49e3a76844543cf78cc0dfe4687e2985d2
  Synced at: 2025-11-16 00:22:02.395782
  Status: active
```

## Production Setup

### Continuous Syncing

Run in a loop to keep syncing new blocks:
```bash
while true; do
  chainetl sync --chain ethereum --resume --count 100
  sleep 60  # Wait 1 minute between syncs
done
```

### Using systemd (Linux)

Create a systemd service for continuous syncing:

```ini
[Unit]
Description=ChainETL Ethereum Sync
After=network.target postgresql.service

[Service]
Type=simple
User=chainetl
WorkingDirectory=/opt/chainetl
ExecStart=/usr/local/bin/chainetl sync --chain ethereum --resume --count 100
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

### Performance Tips

1. **Batch Size**: Use larger --count for faster syncing
2. **RPC Selection**: Use a reliable RPC endpoint or run your own node
3. **Database**: Use connection pooling for better performance
4. **Monitoring**: Set up alerts for sync lag

## Troubleshooting

### RPC Rate Limits

If you hit rate limits, try:
- Using a different RPC provider
- Adding retry delays
- Running your own Ethereum node

### Database Performance

For large syncs, ensure:
- Database has sufficient disk space
- Indexes are created properly
- Connection pool is sized correctly

### Checkpoint Issues

Reset checkpoint if needed:
```sql
DELETE FROM checkpoints WHERE chain = 'ethereum';
```
