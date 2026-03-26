"""Tests for CLI commands."""

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from securitykit.cli import app
from securitykit.models import Finding, Severity, Status

runner = CliRunner()


def _mock_audit(rpc_url):
    return [
        Finding(
            rule_id="SK-001", title="RPC reachable",
            severity=Severity.INFO, status=Status.PASS, detail="OK",
        ),
        Finding(
            rule_id="SK-002", title="No unlocked accounts",
            severity=Severity.CRITICAL, status=Status.PASS, detail="OK",
        ),
    ]


def test_scan_text():
    with patch("securitykit.cli.run_audit", side_effect=_mock_audit):
        result = runner.invoke(app, ["scan", "--rpc-url", "http://test"])
    assert result.exit_code == 0
    assert "2 passed" in result.stdout


def test_scan_json():
    with patch("securitykit.cli.run_audit", side_effect=_mock_audit):
        result = runner.invoke(app, ["scan", "--rpc-url", "http://test", "--output", "json"])
    assert result.exit_code == 0
    assert "SK-001" in result.stdout


def test_report(tmp_path):
    output = str(tmp_path / "report.md")
    with patch("securitykit.cli.run_audit", side_effect=_mock_audit):
        result = runner.invoke(app, ["report", "--rpc-url", "http://test", "--output", output])
    assert result.exit_code == 0
    content = Path(output).read_text()
    assert "# SecurityKit Audit Report" in content
    assert "SK-001" in content
    assert "2 passed" in content
