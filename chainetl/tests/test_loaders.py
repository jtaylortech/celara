"""Tests for loaders."""

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from chainetl.loaders.postgres import BlockTable, CheckpointTable, PostgresLoader
from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint


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

    loader.load_block(block, "ethereum")

    # Verify inserted row exists
    with Session(loader.engine) as session:
        db_block = session.query(BlockTable).filter_by(chain="ethereum", number=42).first()
        assert db_block is not None
        assert db_block.hash == block.hash

    # Dispose the engine to close any open connections and avoid ResourceWarning
    loader.engine.dispose()


def test_checkpoint_save_and_load() -> None:
    """Test saving and loading checkpoints."""

    loader = PostgresLoader("sqlite:///:memory:")

    # Create and save a checkpoint
    checkpoint = Checkpoint(
        chain="ethereum",
        last_synced_block=100,
        last_synced_hash="0x" + "f" * 64,
        synced_at=datetime.now(UTC),
        status="active",
    )
    loader.save_checkpoint(checkpoint)

    # Load the checkpoint
    loaded = loader.load_checkpoint("ethereum")
    assert loaded is not None
    assert loaded.chain == "ethereum"
    assert loaded.last_synced_block == 100
    assert loaded.last_synced_hash == "0x" + "f" * 64
    assert loaded.status == "active"

    # Load non-existent checkpoint
    none_checkpoint = loader.load_checkpoint("base")
    assert none_checkpoint is None

    loader.engine.dispose()


def test_checkpoint_update() -> None:
    """Test updating an existing checkpoint."""

    loader = PostgresLoader("sqlite:///:memory:")

    # Save initial checkpoint
    checkpoint1 = Checkpoint(
        chain="ethereum",
        last_synced_block=100,
        last_synced_hash="0x" + "a" * 64,
        synced_at=datetime.now(UTC),
        status="active",
    )
    loader.save_checkpoint(checkpoint1)

    # Update checkpoint
    checkpoint2 = Checkpoint(
        chain="ethereum",
        last_synced_block=200,
        last_synced_hash="0x" + "b" * 64,
        synced_at=datetime.now(UTC),
        status="active",
    )
    loader.save_checkpoint(checkpoint2)

    # Verify it was updated, not inserted as new row
    loaded = loader.load_checkpoint("ethereum")
    assert loaded is not None
    assert loaded.last_synced_block == 200
    assert loaded.last_synced_hash == "0x" + "b" * 64

    # Verify only one checkpoint exists in DB
    with Session(loader.engine) as session:
        count = session.query(CheckpointTable).count()
        assert count == 1

    loader.engine.dispose()


def test_batch_load_blocks() -> None:
    """Test loading multiple blocks in a batch."""

    loader = PostgresLoader("sqlite:///:memory:")

    blocks = [
        Block(
            number=i,
            hash=f"0x{i:064x}",
            parent_hash=f"0x{i - 1:064x}",
            timestamp=1234567890 + i,
            transactions=[],
        )
        for i in range(1, 11)
    ]

    loader.load_blocks(blocks, "ethereum")

    # Verify all blocks were inserted
    with Session(loader.engine) as session:
        count = session.query(BlockTable).filter_by(chain="ethereum").count()
        assert count == 10

        # Check first and last block
        first = session.query(BlockTable).filter_by(chain="ethereum", number=1).first()
        assert first is not None
        assert first.hash == "0x" + "1".zfill(64)

        last = session.query(BlockTable).filter_by(chain="ethereum", number=10).first()
        assert last is not None
        assert last.hash == "0x" + "a".zfill(64)

    loader.engine.dispose()


def test_batch_load_empty_list() -> None:
    """Test loading an empty list of blocks doesn't error."""

    loader = PostgresLoader("sqlite:///:memory:")
    loader.load_blocks([], "ethereum")  # Should not raise

    # Verify no blocks were inserted
    with Session(loader.engine) as session:
        count = session.query(BlockTable).count()
        assert count == 0

    loader.engine.dispose()


def test_reorg_detection_no_previous_block() -> None:
    """Test reorg detection when there's no previous block."""

    loader = PostgresLoader("sqlite:///:memory:")

    block = Block(
        number=100,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
        transactions=[],
    )

    # Should return False (no reorg) when there's no previous block
    assert loader.detect_reorg("ethereum", block) is False

    loader.engine.dispose()


def test_reorg_detection_valid_chain() -> None:
    """Test reorg detection with a valid chain (no reorg)."""

    loader = PostgresLoader("sqlite:///:memory:")

    # Load block 99
    block99 = Block(
        number=99,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
        transactions=[],
    )
    loader.load_block(block99, "ethereum")

    # Load block 100 with correct parent_hash
    block100 = Block(
        number=100,
        hash="0x" + "c" * 64,
        parent_hash="0x" + "a" * 64,  # Matches block99.hash
        timestamp=1234567891,
        transactions=[],
    )

    # Should return False (no reorg)
    assert loader.detect_reorg("ethereum", block100) is False

    loader.engine.dispose()


def test_reorg_detection_invalid_chain() -> None:
    """Test reorg detection when parent hash doesn't match (reorg detected)."""

    loader = PostgresLoader("sqlite:///:memory:")

    # Load block 99
    block99 = Block(
        number=99,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
        transactions=[],
    )
    loader.load_block(block99, "ethereum")

    # Load block 100 with INCORRECT parent_hash
    block100 = Block(
        number=100,
        hash="0x" + "c" * 64,
        parent_hash="0x" + "d" * 64,  # Does NOT match block99.hash
        timestamp=1234567891,
        transactions=[],
    )

    # Should return True (reorg detected)
    assert loader.detect_reorg("ethereum", block100) is True

    loader.engine.dispose()


def test_get_block_by_number() -> None:
    """Test retrieving a block by its number."""

    loader = PostgresLoader("sqlite:///:memory:")

    # Load a block
    block = Block(
        number=42,
        hash="0x" + "a" * 64,
        parent_hash="0x" + "b" * 64,
        timestamp=1234567890,
        transactions=[],
    )
    loader.load_block(block, "ethereum")

    # Retrieve it
    retrieved = loader.get_block_by_number("ethereum", 42)
    assert retrieved is not None
    assert retrieved.number == 42
    assert retrieved.hash == "0x" + "a" * 64

    # Try to get non-existent block
    none_block = loader.get_block_by_number("ethereum", 999)
    assert none_block is None

    loader.engine.dispose()
