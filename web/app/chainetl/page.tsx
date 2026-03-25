import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainETL — Blockchain Data Pipelines | Celara",
  description:
    "Extract blockchain data and load it into your data warehouse. Multi-chain support for Ethereum, Base, Polygon, and Arbitrum.",
};

export default function ChainETL() {
  return (
    <ProductPage
      name="ChainETL"
      tagline="Blockchain data pipelines"
      description="Extract blockchain data and load it into your data warehouse. Stop writing custom indexers. Get clean, typed data direct to PostgreSQL with resumable syncs and reorg detection."
      installCmd="pip install chainetl"
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        "Extract blocks, transactions, logs, and token transfers",
        "Multi-chain support (4 EVM chains)",
        "Resumable sync with checkpointing",
        "Chain reorganization detection",
        "ERC-20 and ERC-721 token transfer parsing",
        "Type-safe Python SDK with Pydantic models",
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainetl"
    />
  );
}
