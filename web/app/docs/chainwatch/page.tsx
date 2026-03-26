export default function ChainWatchDocs() {
  return (
    <div className="space-y-16">
      <section>
        <h1 className="text-3xl font-bold mb-4">ChainWatch</h1>
        <p className="text-[var(--muted)] leading-relaxed">Prometheus metrics exporter for EVM blockchain nodes. Monitor sync status, peer count, gas prices, and client version. Grafana dashboard included.</p>
        <p className="text-[var(--muted)] mt-2"><strong className="text-[var(--text)]">Supported chains:</strong> Ethereum, Base, Polygon, Arbitrum</p>
      </section>

      <section id="quick-start">
        <h2 className="text-xl font-bold mb-4">Quick Start</h2>
        <Pre code={`pip install chainwatch

# Start exporter
chainwatch exporter --chain ethereum --port 9100

# Metrics at http://localhost:9100/metrics

# One-shot health check
chainwatch status --chain polygon`} />
      </section>

      <section id="metrics">
        <h2 className="text-xl font-bold mb-4">Metrics Reference</h2>
        <div className="border border-[var(--border)] rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">Metric</th><th className="text-left px-4 py-2 font-medium">Type</th><th className="text-left px-4 py-2 font-medium">Description</th></tr></thead>
            <tbody>
              {[
                ["chainwatch_sync_status", "Gauge", "1=synced, 0=syncing"],
                ["chainwatch_current_block", "Gauge", "Current block number"],
                ["chainwatch_highest_block", "Gauge", "Highest known block"],
                ["chainwatch_peer_count", "Gauge", "Connected peers"],
                ["chainwatch_gas_price_gwei", "Gauge", "Gas price in gwei"],
                ["chainwatch_node", "Info", "Client version + chain"],
              ].map((r) => (
                <tr key={r[0]} className="border-t border-[var(--border)]">
                  <td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td>
                  <td className="px-4 py-2 text-[var(--muted)]">{r[1]}</td>
                  <td className="px-4 py-2 text-[var(--muted)]">{r[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-sm text-[var(--muted)] mt-3">All metrics are labeled with <code className="text-emerald-400">chain</code> for multi-chain filtering.</p>
      </section>

      <section id="grafana">
        <h2 className="text-xl font-bold mb-4">Grafana Dashboard</h2>
        <p className="text-sm text-[var(--muted)] mb-4">Import <code className="text-emerald-400">dashboards/node-health.json</code> into Grafana. 7 panels with a <code className="text-emerald-400">$chain</code> template variable:</p>
        <ul className="text-sm text-[var(--muted)] space-y-1">
          <li>1. Sync Status (stat — green/red)</li>
          <li>2. Current Block (stat)</li>
          <li>3. Peer Count (gauge with thresholds)</li>
          <li>4. Gas Price (stat)</li>
          <li>5. Block Height Over Time (timeseries)</li>
          <li>6. Peer Count Over Time (timeseries)</li>
          <li>7. Gas Price Over Time (timeseries)</li>
        </ul>
        <Pre code={`# prometheus.yml
scrape_configs:
  - job_name: chainwatch
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:9100']`} />
      </section>

      <section id="alerts">
        <h2 className="text-xl font-bold mb-4">Alert Rules</h2>
        <Pre code={`# Recommended Prometheus alerts
- alert: SyncLost
  expr: chainwatch_sync_status == 0
  for: 5m

- alert: LowPeers
  expr: chainwatch_peer_count < 3
  for: 2m

- alert: BlockStall
  expr: rate(chainwatch_current_block[5m]) == 0

- alert: GasSpike
  expr: chainwatch_gas_price_gwei > 100`} />
      </section>

      <section id="cli">
        <h2 className="text-xl font-bold mb-4">CLI Reference</h2>
        <Table rows={[
          ["chainwatch exporter --chain ethereum --port 9100", "Start Prometheus exporter"],
          ["chainwatch exporter --interval 30", "Custom scrape interval"],
          ["chainwatch status --chain ethereum", "One-shot health check"],
          ["chainwatch chains", "List supported chains"],
        ]} />
      </section>
    </div>
  );
}

function Pre({ code }: { code: string }) {
  return <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto mt-4"><code className="text-emerald-400">{code}</code></pre>;
}
function Table({ rows }: { rows: string[][] }) {
  return (
    <div className="border border-[var(--border)] rounded-lg overflow-hidden">
      <table className="w-full text-sm"><thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">Command</th><th className="text-left px-4 py-2 font-medium">Description</th></tr></thead>
        <tbody>{rows.map((r) => (<tr key={r[0]} className="border-t border-[var(--border)]"><td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td><td className="px-4 py-2 text-[var(--muted)]">{r[1]}</td></tr>))}</tbody>
      </table>
    </div>
  );
}
