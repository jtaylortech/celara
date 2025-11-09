"""Terraform deployment wrapper."""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from chainops.config import ChainOpsConfig


class DeploymentError(Exception):
    """Raised when deployment fails."""

    pass


class Deployer:
    """Handles Terraform deployments."""

    def __init__(self, config: ChainOpsConfig) -> None:
        """Initialize deployer with configuration."""
        self.config = config
        self.template_dir = self._get_template_dir()
        self.work_dir = Path.cwd() / ".chainops" / config.name
        self._validate_prerequisites()

    def _validate_prerequisites(self) -> None:
        """Validate that required tools are installed."""
        if not shutil.which("terraform"):
            raise DeploymentError(
                "Terraform not found. Install it: brew install terraform"
            )

        # Check template directory exists
        if not self.template_dir.exists():
            raise DeploymentError(
                f"Template directory not found: {self.template_dir}\n"
                f"Chain '{self.config.chain}' may not be supported yet."
            )

        # Check required template files exist
        required_files = ["main.tf", "variables.tf", "outputs.tf"]
        for filename in required_files:
            if not (self.template_dir / filename).exists():
                raise DeploymentError(f"Missing template file: {filename}")

    def _get_template_dir(self) -> Path:
        """Get Terraform template directory for chain."""
        base_dir = Path(__file__).parent.parent.parent / "templates"
        return base_dir / self.config.chain

    def _ensure_work_dir(self) -> None:
        """Ensure working directory exists."""
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def _run_terraform(self, *args: str) -> subprocess.CompletedProcess:
        """Run Terraform command."""
        self._ensure_work_dir()

        # Copy template files to work directory
        if not (self.work_dir / "main.tf").exists():
            for file in self.template_dir.glob("*.tf"):
                shutil.copy(file, self.work_dir)
            for file in self.template_dir.glob("*.yaml"):
                shutil.copy(file, self.work_dir)

        # Create tfvars file
        tfvars = {
            "validator_name": self.config.name,
            "region": self.config.region,
            "instance_type": self.config.compute.instance_type,
            "storage_size": self.config.compute.storage_size,
            "vpc_cidr": self.config.networking.vpc_cidr,
            "allowed_ssh_cidrs": self.config.networking.allowed_ssh_cidrs,
        }

        tfvars_file = self.work_dir / "terraform.tfvars.json"
        with open(tfvars_file, "w") as f:
            json.dump(tfvars, f, indent=2)

        # Run terraform
        cmd = ["terraform", *args]
        try:
            return subprocess.run(cmd, cwd=self.work_dir, check=True)
        except subprocess.CalledProcessError as e:
            raise DeploymentError(f"Terraform command failed: {' '.join(cmd)}") from e

    def plan(self) -> None:
        """Show Terraform plan."""
        self._run_terraform("init")
        self._run_terraform("plan")

    def deploy(self) -> None:
        """Deploy infrastructure."""
        self._run_terraform("init")
        self._run_terraform("apply", "-auto-approve")

    def destroy(self) -> None:
        """Destroy infrastructure."""
        self._run_terraform("destroy", "-auto-approve")

    def status(self) -> dict[str, Any]:
        """Get deployment status."""
        try:
            result = subprocess.run(
                ["terraform", "output", "-json"],
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            outputs = json.loads(result.stdout)

            return {
                "Status": "Running",
                "Instance ID": outputs.get("instance_id", {}).get("value", "N/A"),
                "Public IP": outputs.get("public_ip", {}).get("value", "N/A"),
                "SSH Command": outputs.get("ssh_command", {}).get("value", "N/A"),
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "Status": "Not deployed",
                "Instance ID": "N/A",
                "Public IP": "N/A",
                "SSH Command": "N/A",
            }
