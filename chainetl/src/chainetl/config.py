"""Configuration management."""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # RPC endpoints
    ethereum_rpc_url: str = "https://eth.llamarpc.com"
    base_rpc_url: str = "https://mainnet.base.org"

    # Database
    database_url: str = "postgresql://localhost/chainetl_dev"

    # Logging
    log_level: str = "INFO"

    # Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
