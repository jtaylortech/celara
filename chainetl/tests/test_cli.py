"""Tests for the CLI commands."""

from datetime import UTC, datetime

from typer.testing import CliRunner

from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint


def test_sync_cli_monkeypatched(monkeypatch) -> None:
    """Invoke `chainetl sync` with fake extractor and loader to test flow."""

    # Fake extractor that returns a known block
    class FakeExtractor:
        def __init__(self, rpc_url: str) -> None:
            self.rpc_url = rpc_url

        def extract_latest_block_number(self) -> int:
            return 18000000

        def extract_block(self, block_number: int) -> Block:
            return Block(
                number=block_number,
                hash="0x" + "c" * 64,
                parent_hash="0x" + "d" * 64,
                timestamp=1234567890,
                transactions=[],
            )

    # Fake loader that records the last loaded block
    class FakeLoader:
        last_loaded = None
        last_checkpoint = None

        def __init__(self, connection_string: str) -> None:
            self.connection_string = connection_string

        def load_block(self, block: Block, chain: str) -> None:
            FakeLoader.last_loaded = block

        def save_checkpoint(self, checkpoint: Checkpoint) -> None:
            FakeLoader.last_checkpoint = checkpoint

        def load_checkpoint(self, chain: str) -> Checkpoint | None:
            return None

        def detect_reorg(self, chain: str, block: Block) -> bool:
            return False

    # Monkeypatch the classes in the cli module
    monkeypatch.setattr("chainetl.cli.EthereumExtractor", FakeExtractor)
    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["sync", "--start-block", "18000000"])

    assert result.exit_code == 0
    assert "Loaded block 18000000" in result.stdout
    assert FakeLoader.last_loaded is not None
    assert FakeLoader.last_loaded.number == 18000000


def test_status_command_with_checkpoint(monkeypatch) -> None:
    """Test status command when checkpoint exists."""

    class FakeLoader:
        def __init__(self, connection_string: str) -> None:
            self.connection_string = connection_string

        def load_checkpoint(self, chain: str) -> Checkpoint:
            return Checkpoint(
                chain=chain,
                last_synced_block=18000100,
                last_synced_hash="0x" + "a" * 64,
                synced_at=datetime(2025, 11, 16, 12, 0, 0, tzinfo=UTC),
                status="active",
            )

    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["status", "--chain", "ethereum"])

    assert result.exit_code == 0
    assert "Chain: ethereum" in result.stdout
    assert "Last synced block: 18000100" in result.stdout
    assert "Status: active" in result.stdout


def test_status_command_no_checkpoint(monkeypatch) -> None:
    """Test status command when no checkpoint exists."""

    class FakeLoader:
        def __init__(self, connection_string: str) -> None:
            self.connection_string = connection_string

        def load_checkpoint(self, chain: str) -> None:
            return None

    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["status", "--chain", "base"])

    assert result.exit_code == 0
    assert "Chain: base" in result.stdout
    assert "Checkpoint: None" in result.stdout


def test_sync_with_base_chain(monkeypatch) -> None:
    """Test syncing Base L2 chain."""

    class FakeBaseExtractor:
        def __init__(self, rpc_url: str) -> None:
            self.rpc_url = rpc_url

        def extract_block(self, block_number: int) -> Block:
            return Block(
                number=block_number,
                hash="0x" + "b" * 64,
                parent_hash="0x" + "c" * 64,
                timestamp=1234567890,
                transactions=[],
            )

    class FakeLoader:
        last_loaded = None

        def __init__(self, connection_string: str) -> None:
            pass

        def load_block(self, block: Block, chain: str) -> None:
            FakeLoader.last_loaded = block

        def save_checkpoint(self, checkpoint: Checkpoint) -> None:
            pass

        def load_checkpoint(self, chain: str) -> None:
            return None

        def detect_reorg(self, chain: str, block: Block) -> bool:
            return False

    monkeypatch.setattr("chainetl.cli.BaseL2Extractor", FakeBaseExtractor)
    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["sync", "--chain", "base", "--start-block", "10000000"])

    assert result.exit_code == 0
    assert "Loaded block 10000000" in result.stdout
    assert FakeLoader.last_loaded.number == 10000000


def test_sync_with_resume(monkeypatch) -> None:
    """Test sync with resume from checkpoint."""

    class FakeExtractor:
        def __init__(self, rpc_url: str) -> None:
            pass

        def extract_block(self, block_number: int) -> Block:
            return Block(
                number=block_number,
                hash="0x" + "e" * 64,
                parent_hash="0x" + "f" * 64,
                timestamp=1234567890,
                transactions=[],
            )

    class FakeLoader:
        last_loaded = None

        def __init__(self, connection_string: str) -> None:
            pass

        def load_checkpoint(self, chain: str) -> Checkpoint:
            return Checkpoint(
                chain=chain,
                last_synced_block=18000050,
                last_synced_hash="0x" + "1" * 64,
                synced_at=datetime(2025, 11, 16, 12, 0, 0, tzinfo=UTC),
                status="active",
            )

        def load_block(self, block: Block, chain: str) -> None:
            FakeLoader.last_loaded = block

        def save_checkpoint(self, checkpoint: Checkpoint) -> None:
            pass

        def detect_reorg(self, chain: str, block: Block) -> bool:
            return False

    monkeypatch.setattr("chainetl.cli.EthereumExtractor", FakeExtractor)
    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["sync", "--chain", "ethereum", "--resume"])

    assert result.exit_code == 0
    assert "Resuming from checkpoint" in result.stdout
    assert "18000050 -> 18000051" in result.stdout
    assert FakeLoader.last_loaded.number == 18000051


def test_sync_batch_processing(monkeypatch) -> None:
    """Test syncing multiple blocks in batch."""

    class FakeExtractor:
        def __init__(self, rpc_url: str) -> None:
            pass

        def extract_blocks(self, start_block: int, end_block: int) -> list[Block]:
            return [
                Block(
                    number=i,
                    hash=f"0x{i:064x}",
                    parent_hash=f"0x{i - 1:064x}",
                    timestamp=1234567890 + i,
                    transactions=[],
                )
                for i in range(start_block, end_block + 1)
            ]

    class FakeLoader:
        loaded_blocks = []

        def __init__(self, connection_string: str) -> None:
            FakeLoader.loaded_blocks = []

        def load_checkpoint(self, chain: str) -> None:
            return None

        def load_blocks(self, blocks: list[Block], chain: str) -> None:
            FakeLoader.loaded_blocks.extend(blocks)

        def save_checkpoint(self, checkpoint: Checkpoint) -> None:
            pass

        def detect_reorg(self, chain: str, block: Block) -> bool:
            return False

    monkeypatch.setattr("chainetl.cli.EthereumExtractor", FakeExtractor)
    monkeypatch.setattr("chainetl.cli.PostgresLoader", FakeLoader)

    from chainetl.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["sync", "--start-block", "18000000", "--count", "5"])

    assert result.exit_code == 0
    assert "Loaded 5 blocks" in result.stdout
    assert len(FakeLoader.loaded_blocks) == 5
    assert FakeLoader.loaded_blocks[0].number == 18000000
    assert FakeLoader.loaded_blocks[4].number == 18000004
