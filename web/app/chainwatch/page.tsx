import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainWatch — Blockchain Observability | Celara",
  description:
    "Prometheus metrics exporter for EVM nodes. Monitor sync status, peer count, gas prices, and node health.",
};

export default function ChainWatch() {
  return (
    <ProductPage
      name="ChainWatch"
      tagline="Observability for decentralized systems"
      description="Prometheus metrics exporter for blockchain nodes. Monitor sync status, peer count, gas prices, and node health in real-time. Plug into your existing Grafana stack."
      installCmd="pip install chainwatch"
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        "Prometheus-native metrics with chain labels",
        "Sync status, peer count, gas price, client version",
        "Multi-chain monitoring from a single exporter",
        "Configurable scrape intervals",
        "One-shot health checks via CLI",
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainwatch"
    />
  );
}
