"""Configuration management."""

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # RPC endpoints
    ethereum_rpc_url: HttpUrl = HttpUrl("https://eth.llamarpc.com")  # type: ignore[assignment]
    base_rpc_url: HttpUrl = HttpUrl("https://mainnet.base.org")  # type: ignore[assignment]
    polygon_rpc_url: HttpUrl = HttpUrl("https://polygon-rpc.com")  # type: ignore[assignment]
    arbitrum_rpc_url: HttpUrl = HttpUrl("https://arb1.arbitrum.io/rpc")  # type: ignore[assignment]

    # Database
    database_url: str = "postgresql://localhost/chainetl_dev"

    # Logging
    log_level: str = "INFO"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got {v}")
        return v.upper()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
