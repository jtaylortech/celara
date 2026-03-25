"""Tests for the CLI commands."""

from datetime import UTC, datetime

from typer.testing import CliRunner

from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint

FAKE_HASH = "0x" + "c" * 64
FAKE_PARENT = "0x" + "d" * 64


def _make_block(number: int) -> Block:
    return Block(
        number=number,
        hash=f"0x{number:064x}",
        parent_hash=f"0x{number - 1:064x}",
        timestamp=1234567890 + number,
        transactions=[],
    )


class FakeExtractor:
    """Reusable fake extractor for CLI tests."""

    def __init__(self, rpc_url: str) -> None:
        pass

    def extract_block(self, block_number: int) -> Block:
        return _make_block(block_number)

    def extract_blocks(
        self, start_block: int, end_block: int
    ) -> list[Block]:
        return [_make_block(i) for i in range(start_block, end_block + 1)]

    def close(self) -> None:
        pass


class FakeLoader:
    """Reusable fake loader for CLI tests."""

    last_loaded: Block | None = None
    loaded_blocks: list[Block] = []
    _checkpoint: Checkpoint | None = None

    def __init__(self, connection_string: str) -> None:
        FakeLoader.last_loaded = None
        FakeLoader.loaded_blocks = []

    def load_block(self, block: Block, chain: str) -> None:
        FakeLoader.last_loaded = block

    def load_blocks(self, blocks: list[Block], chain: str) -> None:
        FakeLoader.loaded_blocks.extend(blocks)

    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        pass

    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        return FakeLoader._checkpoint

    def detect_reorg(self, chain: str, block: Block) -> bool:
        return False


def _patch(monkeypatch, checkpoint=None) -> None:
    """Wire up fakes for CLI tests."""
    FakeLoader._checkpoint = checkpoint
    monkeypatch.setattr("chainetl.cli.SUPPORTED_CHAINS", {
        "ethereum": (
            lambda rpc_url: FakeExtractor(rpc_url), "http://fake"
        ),
        "base": (
            lambda rpc_url: FakeExtractor(rpc_url), "http://fake"
        ),
        "polygon": (
            lambda rpc_url: FakeExtractor(rpc_url), "http://fake"
        ),
        "arbitrum": (
            lambda rpc_url: FakeExtractor(rpc_url), "http://fake"
        ),
    })
    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)


def test_sync_single_block(monkeypatch) -> None:
    _patch(monkeypatch)
    from chainetl.cli import app

    result = CliRunner().invoke(app, ["sync", "--start-block", "18000000"])
    assert result.exit_code == 0, result.stdout
    assert "Loaded block 18000000" in result.stdout
    assert FakeLoader.last_loaded is not None
    assert FakeLoader.last_loaded.number == 18000000


def test_sync_base_chain(monkeypatch) -> None:
    _patch(monkeypatch)
    from chainetl.cli import app

    result = CliRunner().invoke(
        app, ["sync", "--chain", "base", "--start-block", "10000000"]
    )
    assert result.exit_code == 0, result.stdout
    assert "Loaded block 10000000" in result.stdout


def test_sync_resume(monkeypatch) -> None:
    checkpoint = Checkpoint(
        chain="ethereum",
        last_synced_block=18000050,
        last_synced_hash="0x" + "1" * 64,
        synced_at=datetime(2025, 11, 16, 12, 0, 0, tzinfo=UTC),
        status="active",
    )
    _patch(monkeypatch, checkpoint=checkpoint)
    from chainetl.cli import app

    result = CliRunner().invoke(
        app, ["sync", "--chain", "ethereum", "--resume"]
    )
    assert result.exit_code == 0, result.stdout
    assert "Resuming from checkpoint" in result.stdout
    assert "18000050 -> 18000051" in result.stdout
    assert FakeLoader.last_loaded.number == 18000051


def test_sync_batch(monkeypatch) -> None:
    _patch(monkeypatch)
    from chainetl.cli import app

    result = CliRunner().invoke(
        app, ["sync", "--start-block", "18000000", "--count", "5"]
    )
    assert result.exit_code == 0, result.stdout
    assert "Loaded 5 blocks" in result.stdout
    assert len(FakeLoader.loaded_blocks) == 5
    assert FakeLoader.loaded_blocks[0].number == 18000000
    assert FakeLoader.loaded_blocks[4].number == 18000004


def test_sync_unsupported_chain() -> None:
    from chainetl.cli import app

    result = CliRunner().invoke(
        app, ["sync", "--chain", "solana", "--start-block", "1"]
    )
    assert result.exit_code == 1
    assert "Unsupported chain" in result.output


def test_status_with_checkpoint(monkeypatch) -> None:
    checkpoint = Checkpoint(
        chain="ethereum",
        last_synced_block=18000100,
        last_synced_hash="0x" + "a" * 64,
        synced_at=datetime(2025, 11, 16, 12, 0, 0, tzinfo=UTC),
        status="active",
    )
    _patch(monkeypatch, checkpoint=checkpoint)
    from chainetl.cli import app

    result = CliRunner().invoke(app, ["status", "--chain", "ethereum"])
    assert result.exit_code == 0
    assert "Chain: ethereum" in result.stdout
    assert "Last synced block: 18000100" in result.stdout
    assert "Status: active" in result.stdout


def test_status_no_checkpoint(monkeypatch) -> None:
    _patch(monkeypatch)
    from chainetl.cli import app

    result = CliRunner().invoke(app, ["status", "--chain", "base"])
    assert result.exit_code == 0
    assert "Chain: base" in result.stdout
    assert "Checkpoint: None" in result.stdout


def test_chains_command() -> None:
    from chainetl.cli import app

    result = CliRunner().invoke(app, ["chains"])
    assert result.exit_code == 0
    assert "ethereum" in result.stdout
    assert "base" in result.stdout
    assert "polygon" in result.stdout
    assert "arbitrum" in result.stdout
