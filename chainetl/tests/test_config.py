"""Tests for configuration settings."""

import importlib


def test_settings_env_override(monkeypatch, tmp_path, capsys) -> None:
    """Settings should pick up environment variable overrides when module is reloaded."""

    monkeypatch.setenv("ETHEREUM_RPC_URL", "http://localhost:8545")

    # Reload the config module to re-evaluate Settings() which is created at import time
    import chainetl.config as config_module

    importlib.reload(config_module)

    assert config_module.settings.ethereum_rpc_url == "http://localhost:8545"
