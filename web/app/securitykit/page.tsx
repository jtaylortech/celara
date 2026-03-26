import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "SecurityKit — Node Security Scanner | Celara",
  description: "Automated security scanning for blockchain nodes. 8 RPC-based checks. Markdown reports. CI/CD integration.",
};

export default function SecurityKit() {
  return (
    <ProductPage
      name="SecurityKit"
      tagline="Automated security for node operators"
      description="Scan your blockchain nodes for security misconfigurations via JSON-RPC. No SSH, no agents, no access keys. SecurityKit connects to your node's RPC endpoint and runs 8 security checks covering critical vulnerabilities like unlocked accounts, exposed admin APIs, and insufficient peer connectivity. Outputs text, JSON, or markdown audit reports."
      installCmd="pip install securitykit"
      features={[
        "RPC-based scanning — no SSH or agent installation required",
        "8 security checks covering critical, high, and medium severity issues",
        "Unlocked account detection (the #1 cause of validator fund loss)",
        "Admin and debug API exposure detection",
        "Peer connectivity and sync status validation",
        "Chain ID verification against known networks",
        "Markdown audit report generation for compliance",
        "JSON output for CI/CD pipeline integration",
        "Exit code 1 on failures — use as a deployment gate",
        "Extensible: add custom checks with a simple function signature",
      ]}
      quickStart={[
        {
          title: "Scan a node",
          language: "bash",
          code: `pip install securitykit

securitykit scan --rpc-url https://eth.llamarpc.com`,
        },
        {
          title: "Generate an audit report",
          language: "bash",
          code: `securitykit report --rpc-url https://eth.llamarpc.com --output audit.md

# Output: audit.md with findings table + remediation steps`,
        },
        {
          title: "CI/CD integration (JSON output + exit code)",
          language: "bash",
          code: `# In your CI pipeline:
securitykit scan --rpc-url \$NODE_RPC_URL --output json

# Exit code 0 = all checks passed
# Exit code 1 = one or more checks failed → block deployment`,
        },
        {
          title: "Custom check (Python)",
          language: "python",
          code: `from securitykit.models import Finding, Severity, Status

def check_max_peers(rpc_url: str) -> Finding:
    """Custom check: ensure peer count doesn't exceed threshold."""
    result = _rpc_call(rpc_url, "net_peerCount")
    peers = int(result.get("result", "0x0"), 16)
    if peers > 100:
        return Finding(
            rule_id="CUSTOM-001",
            title="Excessive peer count",
            severity=Severity.MEDIUM,
            status=Status.FAIL,
            detail=f"{peers} peers (max recommended: 100)",
            remediation="Configure --maxpeers flag",
        )
    return Finding(
        rule_id="CUSTOM-001", title="Peer count normal",
        severity=Severity.MEDIUM, status=Status.PASS,
        detail=f"{peers} peers",
    )`,
        },
      ]}
      cliReference={[
        { command: "securitykit scan --rpc-url <url>", description: "Run all security checks (text output)" },
        { command: "securitykit scan --rpc-url <url> --output json", description: "JSON output for CI/CD pipelines" },
        { command: "securitykit report --rpc-url <url> --output report.md", description: "Generate markdown audit report" },
      ]}
      docs={[
        {
          heading: "Security Checks",
          content: `SK-001 | RPC Reachability (Critical) — Verifies the node responds to web3_clientVersion. If unreachable, all other checks are meaningless.

SK-002 | Unlocked Accounts (Critical) — Checks eth_accounts for any unlocked accounts. This is the #1 cause of fund loss on validator nodes. An unlocked account means anyone with RPC access can sign transactions.

SK-003 | Admin API Exposure (Critical) — Tests if admin_nodeInfo is accessible. The admin namespace allows peer manipulation, data export, and node control. Must never be exposed publicly.

SK-004 | Debug API Exposure (High) — Tests if debug_traceBlockByNumber is accessible. The debug namespace can leak internal state and cause DoS via expensive trace operations.

SK-005 | Mining Status (Medium) — Checks eth_mining. Mining should be disabled unless this is an intentional miner/validator node.

SK-006 | Peer Count (High) — Verifies net_peerCount meets minimum threshold (default: 3). Low peer count indicates network isolation or firewall misconfiguration.

SK-007 | Sync Status (High) — Checks eth_syncing. A node that isn't fully synced should not be used for validation or serving RPC requests.

SK-008 | Chain ID (Medium) — Verifies eth_chainId and maps to known networks (Ethereum=1, Polygon=137, Arbitrum=42161, Base=8453). Helps catch testnet/mainnet misconfigurations.`,
        },
        {
          heading: "Report Format",
          content: `The markdown report includes:

1. Target URL and scan timestamp
2. Findings table with rule ID, check name, severity, and pass/fail status
3. Summary counts (passed, failed, skipped)
4. Remediation section listing every failed check with specific fix instructions

Reports are designed for compliance documentation — attach them to your SOC2 evidence or internal security reviews.`,
        },
        {
          heading: "Adding Custom Checks",
          content: `Every check is a function with signature: (rpc_url: str) -> Finding

To add a custom check:
1. Write a function that returns a Finding with rule_id, title, severity, status, and detail
2. Add it to the ALL_CHECKS list in checks.py
3. The audit runner and CLI will automatically pick it up

Findings have three statuses:
• PASS — check succeeded, no issue found
• FAIL — check found a security issue
• SKIP — check couldn't run (e.g., RPC method not supported)`,
        },
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/securitykit"
    />
  );
}
