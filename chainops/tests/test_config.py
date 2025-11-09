"""Tests for configuration."""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from chainops.config import ChainOpsConfig


def test_config_creation():
    """Test creating a config."""
    config = ChainOpsConfig(
        name="test-validator",
        chain="ethereum",
        network="mainnet",
        provider="aws",
    )

    assert config.name == "test-validator"
    assert config.chain == "ethereum"
    assert config.network == "mainnet"
    assert config.provider == "aws"
    assert config.region == "us-east-1"  # default


def test_config_save_load():
    """Test saving and loading config."""
    config = ChainOpsConfig(
        name="test-validator",
        chain="ethereum",
        network="sepolia",
        provider="aws",
        region="us-west-2",
    )

    with NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_path = Path(f.name)

    try:
        config.save(config_path)
        loaded = ChainOpsConfig.load(config_path)

        assert loaded.name == config.name
        assert loaded.chain == config.chain
        assert loaded.network == config.network
        assert loaded.region == config.region
    finally:
        config_path.unlink()


def test_config_defaults():
    """Test default values."""
    config = ChainOpsConfig(
        name="test",
        chain="ethereum",
        network="mainnet",
    )

    assert config.compute.instance_type == "t3.xlarge"
    assert config.compute.storage_size == 2000
    assert config.compute.spot_instances is False
    assert config.networking.vpc_cidr == "10.0.0.0/16"
    assert config.monitoring.enabled is True


def test_config_custom_compute():
    """Test custom compute configuration."""
    config = ChainOpsConfig(
        name="test",
        chain="ethereum",
        network="mainnet",
        compute={
            "instance_type": "t3.2xlarge",
            "storage_size": 4000,
            "spot_instances": True,
        },
    )

    assert config.compute.instance_type == "t3.2xlarge"
    assert config.compute.storage_size == 4000
    assert config.compute.spot_instances is True
