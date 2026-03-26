"""Tests for config."""

from chainwatch.config import SUPPORTED_CHAINS, Settings


def test_settings_defaults():
    s = Settings()
    assert s.ethereum_rpc_url == "https://eth.llamarpc.com"
    assert s.base_rpc_url == "https://mainnet.base.org"
    assert s.polygon_rpc_url == "https://polygon-rpc.com"
    assert s.arbitrum_rpc_url == "https://arb1.arbitrum.io/rpc"
    assert s.exporter_port == 9100
    assert s.scrape_interval == 15


def test_supported_chains():
    assert "ethereum" in SUPPORTED_CHAINS
    assert "base" in SUPPORTED_CHAINS
    assert "polygon" in SUPPORTED_CHAINS
    assert "arbitrum" in SUPPORTED_CHAINS
