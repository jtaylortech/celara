# Metrics Reference

All metrics are Prometheus gauges labeled with `chain`.

## Gauges

| Metric | Type | Description |
|--------|------|-------------|
| `chainwatch_sync_status` | Gauge | `1` = synced, `0` = syncing. Alert if 0 for >5m. |
| `chainwatch_current_block` | Gauge | Current block number. Track rate for stall detection. |
| `chainwatch_highest_block` | Gauge | Highest known block. Gap with current = sync progress. |
| `chainwatch_peer_count` | Gauge | Connected peers. Alert if <3 (network isolation). |
| `chainwatch_gas_price_gwei` | Gauge | Gas price in gwei. Useful for cost monitoring. |
| `chainwatch_node` | Info | Client version string + chain name. |

## Labels

Every metric has a `chain` label: `ethereum`, `base`, `polygon`, `arbitrum`.

```promql
# Filter by chain
chainwatch_peer_count{chain="ethereum"}

# Aggregate across chains
sum(chainwatch_peer_count)
```

## Recommended Alerts

```yaml
groups:
  - name: chainwatch
    rules:
      - alert: SyncLost
        expr: chainwatch_sync_status == 0
        for: 5m
        labels: { severity: critical }

      - alert: LowPeers
        expr: chainwatch_peer_count < 3
        for: 2m
        labels: { severity: warning }

      - alert: BlockStall
        expr: rate(chainwatch_current_block[5m]) == 0
        labels: { severity: critical }

      - alert: GasSpike
        expr: chainwatch_gas_price_gwei > 100
        labels: { severity: info }
```

## Grafana

Import `dashboards/node-health.json` into Grafana. 7 panels with a `$chain` template variable for switching between chains.
