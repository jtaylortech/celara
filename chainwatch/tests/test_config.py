"""Tests for config."""

from chainwatch.config import Settings


def test_settings_defaults():
    """Test default settings."""
    settings = Settings()
    assert settings.ethereum_rpc_url == "https://eth.llamarpc.com"
    assert settings.exporter_port == 9100
    assert settings.scrape_interval == 15
