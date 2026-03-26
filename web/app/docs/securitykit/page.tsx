export default function SecurityKitDocs() {
  return (
    <div className="space-y-16">
      <section>
        <h1 className="text-3xl font-bold mb-4">SecurityKit</h1>
        <p className="text-[var(--muted)] leading-relaxed">Automated security scanning for blockchain nodes via JSON-RPC. No SSH, no agents. 8 checks covering critical vulnerabilities. Markdown reports for compliance.</p>
      </section>

      <section id="quick-start">
        <h2 className="text-xl font-bold mb-4">Quick Start</h2>
        <Pre code={`pip install securitykit

# Scan a node
securitykit scan --rpc-url https://eth.llamarpc.com

# JSON output for CI/CD
securitykit scan --rpc-url $NODE_URL --output json

# Generate audit report
securitykit report --rpc-url $NODE_URL --output audit.md`} />
      </section>

      <section id="checks">
        <h2 className="text-xl font-bold mb-4">Security Checks</h2>
        <div className="border border-[var(--border)] rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">ID</th><th className="text-left px-4 py-2 font-medium">Check</th><th className="text-left px-4 py-2 font-medium">Severity</th><th className="text-left px-4 py-2 font-medium">Why It Matters</th></tr></thead>
            <tbody>
              {[
                ["SK-001", "RPC Reachability", "Critical", "If unreachable, node is down or misconfigured"],
                ["SK-002", "Unlocked Accounts", "Critical", "#1 cause of fund loss — anyone with RPC access can sign txs"],
                ["SK-003", "Admin API Exposed", "Critical", "Allows peer manipulation, data export, node control"],
                ["SK-004", "Debug API Exposed", "High", "Leaks internal state, enables DoS via expensive traces"],
                ["SK-005", "Mining Status", "Medium", "Should be disabled unless intentional miner node"],
                ["SK-006", "Peer Count", "High", "Low peers = network isolation, missed attestations"],
                ["SK-007", "Sync Status", "High", "Unsynced node should not validate or serve RPC"],
                ["SK-008", "Chain ID", "Medium", "Catches testnet/mainnet misconfigurations"],
              ].map((r) => (
                <tr key={r[0]} className="border-t border-[var(--border)]">
                  <td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td>
                  <td className="px-4 py-2 text-[var(--text)]">{r[1]}</td>
                  <td className="px-4 py-2 text-[var(--muted)]">{r[2]}</td>
                  <td className="px-4 py-2 text-[var(--muted)]">{r[3]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section id="reports">
        <h2 className="text-xl font-bold mb-4">Audit Reports</h2>
        <p className="text-sm text-[var(--muted)] mb-4">The <code className="text-emerald-400">report</code> command generates a markdown file with:</p>
        <ul className="text-sm text-[var(--muted)] space-y-1 mb-4">
          <li>• Target URL</li>
          <li>• Findings table (rule ID, check, severity, status)</li>
          <li>• Summary counts (passed, failed, skipped)</li>
          <li>• Remediation section for every failed check</li>
        </ul>
        <p className="text-sm text-[var(--muted)]">Attach to SOC2 evidence, internal security reviews, or validator onboarding checklists.</p>
      </section>

      <section id="custom">
        <h2 className="text-xl font-bold mb-4">Custom Checks</h2>
        <p className="text-sm text-[var(--muted)] mb-4">Every check is a function: <code className="text-emerald-400">(rpc_url: str) → Finding</code></p>
        <Pre code={`from securitykit.models import Finding, Severity, Status

def check_max_peers(rpc_url: str) -> Finding:
    result = _rpc_call(rpc_url, "net_peerCount")
    peers = int(result.get("result", "0x0"), 16)
    if peers > 100:
        return Finding(
            rule_id="CUSTOM-001",
            title="Excessive peer count",
            severity=Severity.MEDIUM,
            status=Status.FAIL,
            detail=f"{peers} peers (max: 100)",
            remediation="Set --maxpeers flag",
        )
    return Finding(
        rule_id="CUSTOM-001", title="Peer count normal",
        severity=Severity.MEDIUM, status=Status.PASS,
        detail=f"{peers} peers",
    )

# Add to ALL_CHECKS list in checks.py — auto-picked up by CLI`} />
      </section>

      <section id="cli">
        <h2 className="text-xl font-bold mb-4">CLI Reference</h2>
        <Table rows={[
          ["securitykit scan --rpc-url <url>", "Run all checks (text output)"],
          ["securitykit scan --rpc-url <url> --output json", "JSON for CI/CD (exit code 1 on fail)"],
          ["securitykit report --rpc-url <url> --output report.md", "Markdown audit report"],
        ]} />
      </section>
    </div>
  );
}

function Pre({ code }: { code: string }) {
  return <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto mt-4"><code className="text-emerald-400">{code}</code></pre>;
}
function Table({ rows }: { rows: string[][] }) {
  return (
    <div className="border border-[var(--border)] rounded-lg overflow-hidden">
      <table className="w-full text-sm"><thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">Command</th><th className="text-left px-4 py-2 font-medium">Description</th></tr></thead>
        <tbody>{rows.map((r) => (<tr key={r[0]} className="border-t border-[var(--border)]"><td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td><td className="px-4 py-2 text-[var(--muted)]">{r[1]}</td></tr>))}</tbody>
      </table>
    </div>
  );
}
