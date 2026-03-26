import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "ChainOps — Infrastructure-as-Code for Validators | Celara",
  description: "Deploy blockchain validators with one command. Terraform templates for Ethereum and Solana on AWS.",
};

export default function ChainOps() {
  return (
    <ProductPage
      name="ChainOps"
      tagline="Infrastructure-as-Code for validators"
      gradient="from-yellow-400 to-amber-500"
      description="Deploy blockchain validators with a single command. ChainOps generates Terraform configurations for AWS with chain-specific defaults — instance types, storage, security groups, and monitoring. Cost estimation before you deploy."
      installCmd="pip install chainops"
      heroCode={`# Initialize Ethereum validator
$ chainops init ethereum --network mainnet --region us-east-1
✓ Configuration saved to chainops.yaml

# Estimate costs
$ chainops estimate
┌─────────────────────────────┬──────────┐
│ Component                   │     Cost │
├─────────────────────────────┼──────────┤
│ EC2 Instance (t3.xlarge)    │  $120.00 │
│ EBS Storage (2TB gp3)       │  $160.00 │
│ Data Transfer (~500GB)      │   $45.00 │
│ CloudWatch                  │   $10.00 │
│ Total                       │  $335.00 │
└─────────────────────────────┴──────────┘

# Deploy
$ chainops deploy --dry-run   # Preview first
$ chainops deploy              # Ship it`}
      stats={[
        { label: "Chains", value: "2" },
        { label: "Tests", value: "14" },
        { label: "Cloud", value: "AWS" },
        { label: "IaC", value: "Terraform" },
      ]}
      chains={["Ethereum", "Solana"]}
      features={[
        { title: "One-Command Deploy", desc: "From zero to running validator in one command. Terraform handles EC2, EBS, security groups, and monitoring." },
        { title: "Cost Estimation", desc: "See exactly what you'll pay before deploying. Spot instance pricing included for 70% savings." },
        { title: "Dry Run Mode", desc: "Preview the full Terraform plan without touching infrastructure. Review before you commit." },
        { title: "State Tracking", desc: "Track all deployments with status, IP addresses, and regions. List and manage your fleet." },
        { title: "Security Hardening", desc: "Firewall rules, SSH lockdown, and chain-specific port configuration generated automatically." },
        { title: "Chain-Specific Defaults", desc: "Ethereum gets t3.xlarge + 2TB. Solana gets r6i.2xlarge + 2TB. Right-sized from the start." },
      ]}
      docsHref="/docs/chainops"
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/chainops"
    />
  );
}
