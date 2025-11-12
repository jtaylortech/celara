"""Tests for loaders."""

from chainetl.loaders.postgres import PostgresLoader, BlockTable
from chainetl.models.block import Block
from sqlalchemy.orm import Session


def test_postgres_loader_with_sqlite() -> None:
    """PostgresLoader should create the table and insert a block using SQLite in-memory DB."""

    loader = PostgresLoader("sqlite:///:memory:")

    block = Block(
        number=42,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
        transactions=[],
    )

    loader.load_block(block)

    # Verify inserted row exists
    with Session(loader.engine) as session:
        db_block = session.get(BlockTable, 42)
        assert db_block is not None
        assert db_block.hash == block.hash
