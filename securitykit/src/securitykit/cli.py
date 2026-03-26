"""Command-line interface."""

import json

import typer

from securitykit.audit import run_audit
from securitykit.models import Status

app = typer.Typer(help="SecurityKit - Automated security for node operators")

_STATUS_ICON = {
    Status.PASS: "✅",
    Status.FAIL: "❌",
    Status.SKIP: "⏭️",
}


@app.command()
def scan(
    rpc_url: str = typer.Option(..., help="Node RPC endpoint to audit"),
    output: str = typer.Option("text", help="Output format (text, json)"),
) -> None:
    """Scan a node for security misconfigurations."""
    typer.echo(f"Scanning {rpc_url}...\n")

    findings = run_audit(rpc_url)

    if output == "json":
        data = [
            {
                "rule_id": f.rule_id,
                "title": f.title,
                "severity": f.severity.value,
                "status": f.status.value,
                "detail": f.detail,
                "remediation": f.remediation,
            }
            for f in findings
        ]
        typer.echo(json.dumps(data, indent=2))
        return

    # Text output
    for f in findings:
        icon = _STATUS_ICON[f.status]
        typer.echo(f"  {icon} [{f.rule_id}] {f.title}")
        typer.echo(f"     {f.detail}")
        if f.status == Status.FAIL and f.remediation:
            typer.echo(f"     → {f.remediation}")
        typer.echo()

    passed = sum(1 for f in findings if f.status == Status.PASS)
    failed = sum(1 for f in findings if f.status == Status.FAIL)
    skipped = sum(1 for f in findings if f.status == Status.SKIP)
    typer.echo(f"Results: {passed} passed, {failed} failed, {skipped} skipped")

    if failed > 0:
        raise typer.Exit(1)


@app.command()
def report(
    rpc_url: str = typer.Option(..., help="Node RPC endpoint to audit"),
    output: str = typer.Option("report.md", help="Output file"),
) -> None:
    """Generate a markdown security audit report."""
    findings = run_audit(rpc_url)

    lines = [
        "# SecurityKit Audit Report\n",
        f"**Target**: `{rpc_url}`\n",
        "| Rule | Check | Severity | Status |",
        "|------|-------|----------|--------|",
    ]
    for f in findings:
        icon = _STATUS_ICON[f.status]
        lines.append(
            f"| {f.rule_id} | {f.title} | {f.severity.value} "
            f"| {icon} {f.status.value} |"
        )

    passed = sum(1 for f in findings if f.status == Status.PASS)
    failed = sum(1 for f in findings if f.status == Status.FAIL)
    lines.append(f"\n**Results**: {passed} passed, {failed} failed\n")

    # Remediation section
    failures = [f for f in findings if f.status == Status.FAIL]
    if failures:
        lines.append("## Remediation Required\n")
        for f in failures:
            lines.append(f"- **{f.rule_id}**: {f.remediation}")

    text = "\n".join(lines) + "\n"
    with open(output, "w") as fh:
        fh.write(text)
    typer.echo(f"Report written to {output}")


if __name__ == "__main__":
    app()
