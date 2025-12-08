"""State management for tracking deployments."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

STATE_DIR = Path.home() / ".chainops"
STATE_FILE = STATE_DIR / "state.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Deployment(BaseModel):
    """Single deployment record."""

    name: str
    chain: str
    network: str
    provider: str
    region: str
    status: Literal["deploying", "running", "stopped", "destroyed", "failed"]
    instance_id: str | None = None
    public_ip: str | None = None
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)
    work_dir: str | None = None


class State(BaseModel):
    """Global state tracking all deployments."""

    deployments: dict[str, Deployment] = Field(default_factory=dict)

    @classmethod
    def load(cls) -> "State":
        """Load state from disk."""
        if not STATE_FILE.exists():
            return cls()
        with open(STATE_FILE) as f:
            return cls(**json.load(f))

    def save(self) -> None:
        """Save state to disk."""
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(self.model_dump(), f, indent=2)

    def add(self, deployment: Deployment) -> None:
        """Add or update a deployment."""
        deployment.updated_at = _now_iso()
        self.deployments[deployment.name] = deployment
        self.save()

    def get(self, name: str) -> Deployment | None:
        """Get deployment by name."""
        return self.deployments.get(name)

    def remove(self, name: str) -> None:
        """Remove a deployment."""
        if name in self.deployments:
            del self.deployments[name]
            self.save()

    def list_all(self) -> list[Deployment]:
        """List all deployments."""
        return list(self.deployments.values())

    def update_status(
        self,
        name: str,
        status: Literal["deploying", "running", "stopped", "destroyed", "failed"],
        instance_id: str | None = None,
        public_ip: str | None = None,
    ) -> None:
        """Update deployment status."""
        if name in self.deployments:
            self.deployments[name].status = status
            self.deployments[name].updated_at = _now_iso()
            if instance_id:
                self.deployments[name].instance_id = instance_id
            if public_ip:
                self.deployments[name].public_ip = public_ip
            self.save()
