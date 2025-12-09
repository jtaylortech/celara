"""Configuration settings."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings from environment."""

    ethereum_rpc_url: str = os.getenv("ETHEREUM_RPC_URL", "https://eth.llamarpc.com")
    exporter_port: int = int(os.getenv("EXPORTER_PORT", "9100"))
    scrape_interval: int = int(os.getenv("SCRAPE_INTERVAL", "15"))


settings = Settings()
