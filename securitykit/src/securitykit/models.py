"""Security audit rules for blockchain nodes.

Each rule checks one specific misconfiguration. Rules are composable
and chain-agnostic where possible.
"""

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


@dataclass(frozen=True)
class Finding:
    """Result of a single security check."""

    rule_id: str
    title: str
    severity: Severity
    status: Status
    detail: str
    remediation: str = ""


@dataclass(frozen=True)
class Rule:
    """A security audit rule definition."""

    id: str
    title: str
    severity: Severity
    description: str
    remediation: str
