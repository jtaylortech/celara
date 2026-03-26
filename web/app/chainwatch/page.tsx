import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainWatch — Blockchain Observability | Celara",
  description: "Prometheus metrics exporter for EVM nodes. Grafana dashboards included. 4 chains.",
};

export default function ChainWatch() {
  return (
    <ProductPage
      name="ChainWatch"
      tagline="Observability for decentralized systems"
      gradient="from-blue-500 to-purple-500"
      description="Prometheus metrics exporter for blockchain nodes. Monitor sync status, peer count, gas prices, and client version across multiple EVM chains. All metrics labeled by chain. Grafana dashboard with 7 panels included."
      installCmd="pip install chainwatch"
      screenshotSrc="/screenshots/chainwatch-metrics.png"
      demoGif="/recordings/chainwatch-demo.gif"
      screenshotAlt="ChainWatch Prometheus metrics output"
      stats={[
        { label: "EVM Chains", value: "4" },
        { label: "Metrics", value: "6" },
        { label: "Grafana Panels", value: "7" },
        { label: "Tests", value: "9" },
      ]}
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        { title: "Prometheus Native", desc: "Standard Prometheus gauges and info metrics. Scrape with any Prometheus-compatible system." },
        { title: "Chain Labels", desc: "Every metric labeled with chain name. Filter and aggregate across your multi-chain fleet." },
        { title: "Grafana Dashboard", desc: "7-panel dashboard included. Sync status, block height, peer count, gas price — all with chain selector." },
        { title: "Alert Rules", desc: "Recommended alerts: sync lost, low peers, block stall, gas spike. Copy-paste into your alertmanager." },
        { title: "One-Shot Checks", desc: "chainwatch status for quick health checks without running a persistent exporter." },
        { title: "Multi-Chain", desc: "Run one exporter per chain on different ports. Or monitor all from a single Grafana dashboard." },
      ]}
      docsHref="/docs/chainwatch"
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainwatch"
    />
  );
}
