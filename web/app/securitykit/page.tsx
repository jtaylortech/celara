import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "SecurityKit — Node Security Scanner | Celara",
  description: "8 automated security checks for blockchain nodes via RPC. Markdown audit reports. CI/CD integration.",
};

export default function SecurityKit() {
  return (
    <ProductPage
      name="SecurityKit"
      tagline="Automated security for node operators"
      gradient="from-pink-500 to-amber-500"
      description="Scan your blockchain nodes for security misconfigurations via JSON-RPC. No SSH, no agents. 8 checks covering unlocked accounts, exposed admin APIs, peer connectivity, and sync status. Markdown reports for compliance. JSON output for CI/CD."
      installCmd="pip install securitykit"
      screenshotSrc="/screenshots/securitykit-scan.png"
      demoGif="/recordings/securitykit-demo.gif"
      screenshotAlt="SecurityKit scanning a node for vulnerabilities"
      stats={[
        { label: "Security Checks", value: "8" },
        { label: "Tests", value: "21" },
        { label: "Output Formats", value: "3" },
        { label: "Setup Required", value: "0" },
      ]}
      features={[
        { title: "Zero Setup", desc: "No SSH keys, no agents, no access tokens. Just point at an RPC URL and scan." },
        { title: "Critical Checks", desc: "Unlocked accounts (#1 cause of fund loss), admin API exposure, debug API exposure." },
        { title: "Audit Reports", desc: "Generate markdown reports with findings table and remediation steps. Attach to SOC2 evidence." },
        { title: "CI/CD Ready", desc: "JSON output + exit code 1 on failures. Use as a deployment gate in your pipeline." },
        { title: "Extensible", desc: "Add custom checks with a simple function signature: (rpc_url) → Finding. Auto-picked up by CLI." },
        { title: "Chain ID Verification", desc: "Catches testnet/mainnet misconfigurations. Maps to known networks (ETH=1, Polygon=137, etc)." },
      ]}
      docsHref="/docs/securitykit"
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/securitykit"
    />
  );
}
