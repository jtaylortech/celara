"""Configuration management for ChainOps."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class ComputeConfig(BaseModel):
    """Compute instance configuration."""

    instance_type: str = Field(default="t3.xlarge", description="Instance type")
    storage_size: int = Field(default=2000, description="Storage size in GB")
    spot_instances: bool = Field(default=False, description="Use spot instances")


class NetworkingConfig(BaseModel):
    """Networking configuration."""

    vpc_cidr: str = Field(default="10.0.0.0/16", description="VPC CIDR block")
    public_ip: bool = Field(default=True, description="Assign public IP")
    allowed_ssh_cidrs: list[str] = Field(
        default=["0.0.0.0/0"], description="Allowed SSH CIDR blocks"
    )


class MonitoringConfig(BaseModel):
    """Monitoring configuration."""

    enabled: bool = Field(default=True, description="Enable monitoring")
    metrics_port: int = Field(default=9090, description="Metrics port")


class ChainOpsConfig(BaseModel):
    """Main ChainOps configuration."""

    name: str = Field(..., description="Validator name")
    chain: Literal["ethereum", "solana"] = Field(..., description="Blockchain")
    network: Literal["mainnet", "testnet", "sepolia", "devnet"] = Field(
        ..., description="Network"
    )
    provider: Literal["aws", "gcp", "azure"] = Field(default="aws", description="Cloud provider")
    region: str = Field(default="us-east-1", description="Cloud region")

    compute: ComputeConfig = Field(default_factory=ComputeConfig)
    networking: NetworkingConfig = Field(default_factory=NetworkingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)

    def save(self, path: Path) -> None:
        """Save configuration to YAML file."""
        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, path: Path) -> "ChainOpsConfig":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
