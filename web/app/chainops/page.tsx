import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainOps — Infrastructure-as-Code for Validators | Celara",
  description:
    "Deploy blockchain validators with a single command. Terraform and cloud-init templates for Ethereum, Solana, and Cosmos.",
};

export default function ChainOps() {
  return (
    <ProductPage
      name="ChainOps"
      tagline="Infrastructure-as-Code for validators"
      description="Deploy blockchain validators with a single command. No more manual server setup. No more copy-pasting configs from Discord. Production-grade infrastructure from day one."
      chains={["Ethereum", "Solana", "Cosmos"]}
      features={[
        "One-command validator deployment",
        "Multi-chain templates (ETH, SOL, Cosmos)",
        "Automated security hardening",
        "Cost estimation before deploy",
        "State tracking across deployments",
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainops"
    />
  );
}
