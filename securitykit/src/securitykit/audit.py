"""Security audit runner."""

from securitykit.checks import ALL_CHECKS
from securitykit.models import Finding


def run_audit(rpc_url: str) -> list[Finding]:
    """Run all security checks against an RPC endpoint."""
    return [check(rpc_url) for check in ALL_CHECKS]
