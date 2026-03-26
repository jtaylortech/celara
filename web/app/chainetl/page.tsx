import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainETL — Blockchain Data Pipelines | Celara",
  description: "Extract blockchain data from 4 EVM chains into PostgreSQL or JSON Lines. 66 tests, 89% coverage.",
};

export default function ChainETL() {
  return (
    <ProductPage
      name="ChainETL"
      tagline="Blockchain data pipelines for EVM chains"
      gradient="from-purple-500 to-pink-500"
      description="Extract blocks, transactions, logs, and token transfers from any EVM chain. Load into PostgreSQL for analytics or JSON Lines for local processing with jq, DuckDB, or pandas. Resumable syncs, reorg detection, and ERC-20/721 token parsing."
      installCmd="pip install chainetl"
      screenshotSrc="/screenshots/chainetl-sync.png"
      screenshotAlt="ChainETL syncing Ethereum blocks to JSON Lines"
      stats={[
        { label: "EVM Chains", value: "4" },
        { label: "Tests", value: "66" },
        { label: "Coverage", value: "89%" },
        { label: "Output Formats", value: "2" },
      ]}
      chains={["Ethereum", "Base", "Polygon", "Arbitrum"]}
      features={[
        { title: "Multi-Chain", desc: "Ethereum, Base, Polygon, Arbitrum. Adding a new EVM chain is a 3-line Python file." },
        { title: "Two Output Formats", desc: "PostgreSQL for analytics dashboards. JSON Lines for local processing with jq, DuckDB, or pandas." },
        { title: "Resumable Syncs", desc: "Automatic checkpointing. Stop and resume anytime. Never re-sync blocks you already have." },
        { title: "Reorg Detection", desc: "Catches chain reorganizations by comparing parent hashes. Logs warnings and overwrites stale data." },
        { title: "Token Transfer Parsing", desc: "ERC-20 and ERC-721 Transfer events parsed from transaction logs. Fungible and NFT transfers." },
        { title: "Type-Safe SDK", desc: "Pydantic models for Block, Transaction, Log, TokenTransfer. Full type hints, mypy strict." },
      ]}
      docsHref="/docs/chainetl"
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainetl"
    />
  );
}
