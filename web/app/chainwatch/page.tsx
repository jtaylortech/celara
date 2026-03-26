import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainWatch — Blockchain Observability | Celara",
  description: "Prometheus metrics exporter for EVM nodes. Grafana dashboards included.",
};

export default function ChainWatch() {
  return (
    <ProductPage
      name="ChainWatch"
      tagline="Observability for decentralized systems"
      description="Prometheus metrics exporter for blockchain nodes. Monitor sync status, peer count, gas prices, and client version across multiple EVM chains. All metrics are labeled by chain for multi-chain monitoring from a single exporter. Grafana dashboard included — import and go."
      installCmd="pip install chainwatch"
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        "Prometheus-native metrics with chain labels",
        "Sync status monitoring (synced vs syncing)",
        "Block height tracking over time",
        "Peer count with health thresholds",
        "Gas price tracking in gwei",
        "Node client version reporting",
        "Multi-chain from a single exporter instance",
        "Configurable scrape intervals",
        "One-shot health checks via CLI",
        "Grafana dashboard JSON included (7 panels)",
      ]}
      quickStart={[
        {
          title: "Start the exporter",
          language: "bash",
          code: `pip install chainwatch
chainwatch exporter --chain ethereum --port 9100

# Metrics available at http://localhost:9100/metrics`,
        },
        {
          title: "Monitor multiple chains",
          language: "bash",
          code: `# Run one exporter per chain (different ports)
chainwatch exporter --chain ethereum --port 9100 &
chainwatch exporter --chain polygon --port 9101 &
chainwatch exporter --chain arbitrum --port 9102 &`,
        },
        {
          title: "One-shot health check",
          language: "bash",
          code: `chainwatch status --chain ethereum
# Checking ethereum node at https://eth.llamarpc.com...
# Node Status: OK`,
        },
        {
          title: "Prometheus scrape config",
          language: "yaml",
          code: `# prometheus.yml
scrape_configs:
  - job_name: chainwatch
    scrape_interval: 15s
    static_configs:
      - targets:
          - localhost:9100  # ethereum
          - localhost:9101  # polygon
          - localhost:9102  # arbitrum`,
        },
      ]}
      cliReference={[
        { command: "chainwatch exporter --chain ethereum --port 9100", description: "Start Prometheus metrics exporter" },
        { command: "chainwatch exporter --chain polygon --interval 30", description: "Custom scrape interval (seconds)" },
        { command: "chainwatch status --chain ethereum", description: "One-shot node health check" },
        { command: "chainwatch chains", description: "List supported blockchains" },
      ]}
      docs={[
        {
          heading: "Metrics Reference",
          content: `chainwatch_sync_status{chain="ethereum"} — 1 if synced, 0 if syncing. Use for alerting on sync regression.

chainwatch_current_block{chain="ethereum"} — Current block number. Track block height over time to detect stalls.

chainwatch_highest_block{chain="ethereum"} — Highest known block. Gap between current and highest indicates sync progress.

chainwatch_peer_count{chain="ethereum"} — Connected peers. Alert if below 3 (network isolation risk).

chainwatch_gas_price_gwei{chain="ethereum"} — Current gas price in gwei. Useful for transaction cost monitoring.

chainwatch_node{chain="ethereum", client_version="Geth/v1.13.0"} — Node client info. Track client versions across your fleet.`,
        },
        {
          heading: "Grafana Dashboard",
          content: `A pre-built Grafana dashboard is included at dashboards/node-health.json with 7 panels:

1. Sync Status (stat) — Green/red indicator
2. Current Block (stat) — Latest block number
3. Peer Count (gauge) — With red/orange/green thresholds
4. Gas Price (stat) — Current gwei
5. Block Height Over Time (timeseries)
6. Peer Count Over Time (timeseries)
7. Gas Price Over Time (timeseries)

All panels use a $chain template variable for switching between chains. Import via Grafana UI → Dashboards → Import → Upload JSON.`,
        },
        {
          heading: "Alert Rules",
          content: `Recommended Prometheus alert rules:

• Sync Lost: chainwatch_sync_status == 0 for 5m
• Low Peers: chainwatch_peer_count < 3 for 2m
• Block Stall: rate(chainwatch_current_block[5m]) == 0
• Gas Spike: chainwatch_gas_price_gwei > 100`,
        },
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainwatch"
    />
  );
}
