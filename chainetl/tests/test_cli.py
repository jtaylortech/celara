"""Tests for the CLI commands."""

from typer.testing import CliRunner

from chainetl.models.block import Block


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

        def __init__(self, connection_string: str) -> None:
            self.connection_string = connection_string

        def load_block(self, block: Block) -> None:
            FakeLoader.last_loaded = block

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
