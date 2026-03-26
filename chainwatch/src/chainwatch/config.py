"""Configuration settings."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings from environment."""

    ethereum_rpc_url: str = os.getenv(
        "ETHEREUM_RPC_URL", "https://eth.llamarpc.com"
    )
    base_rpc_url: str = os.getenv(
        "BASE_RPC_URL", "https://mainnet.base.org"
    )
    polygon_rpc_url: str = os.getenv(
        "POLYGON_RPC_URL", "https://polygon-rpc.com"
    )
    arbitrum_rpc_url: str = os.getenv(
        "ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc"
    )
    exporter_port: int = int(os.getenv("EXPORTER_PORT", "9100"))
    scrape_interval: int = int(os.getenv("SCRAPE_INTERVAL", "15"))


# Chain name → RPC URL attribute name
SUPPORTED_CHAINS: dict[str, str] = {
    "ethereum": "ethereum_rpc_url",
    "base": "base_rpc_url",
    "polygon": "polygon_rpc_url",
    "arbitrum": "arbitrum_rpc_url",
}

settings = Settings()
