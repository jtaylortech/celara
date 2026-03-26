import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "SecurityKit — Node Security Scanner | Celara",
  description:
    "Automated security scanning for blockchain nodes. Detect unlocked accounts, misconfigurations, and vulnerabilities.",
};

export default function SecurityKit() {
  return (
    <ProductPage
      name="SecurityKit"
      tagline="Automated security for node operators"
      description="Scan your blockchain nodes for security misconfigurations. No SSH required — SecurityKit audits via RPC and reports findings with severity levels and remediation steps."
      installCmd="pip install securitykit"
      features={[
        "RPC-based scanning — no SSH or agent required",
        "Unlocked account detection (critical vulnerability)",
        "Mining/minting status verification",
        "Peer connectivity health checks",
        "Sync status validation",
        "JSON output for CI/CD integration",
        "Exit code 1 on failures for pipeline gating",
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/securitykit"
    />
  );
}
