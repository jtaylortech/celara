"""Postgres data loader."""

import re

import structlog
from sqlalchemy import BigInteger, Column, DateTime, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from chainetl.loaders.base import BaseLoader
from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint

logger = structlog.get_logger()
Base = declarative_base()


def _sanitize_connection_string(connection_string: str) -> str:
    """Sanitize database connection string by masking the password.

    Args:
        connection_string: Database connection string

    Returns:
        Sanitized connection string with password masked
    """
    # Mask password in connection string (postgresql://user:PASSWORD@host/db)
    return re.sub(r"(:)([^@:]+)(@)", r"\1***\3", connection_string)


class BlockTable(Base):  # type: ignore[misc,valid-type]
    """Blocks table."""

    __tablename__ = "blocks"

    chain = Column(String, primary_key=True)
    number = Column(BigInteger, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    parent_hash = Column(String, nullable=False)
    timestamp = Column(BigInteger, nullable=False)


class CheckpointTable(Base):  # type: ignore[misc,valid-type]
    """Checkpoints table for tracking sync progress."""

    __tablename__ = "checkpoints"

    chain = Column(String, primary_key=True)
    last_synced_block = Column(BigInteger, nullable=False)
    last_synced_hash = Column(String, nullable=False)
    synced_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="active")


class PostgresLoader(BaseLoader):
    """Load data to Postgres."""

    def __init__(self, connection_string: str) -> None:
        """Initialize Postgres loader.

        Args:
            connection_string: Postgres connection string
        """
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        logger.info(
            "postgres_loader_initialized",
            connection_string=_sanitize_connection_string(connection_string),
        )

    def load_block(self, block: Block, chain: str) -> None:
        """Load a block to Postgres.

        Args:
            block: Block to load
            chain: Chain identifier (e.g., "ethereum", "base")
        """
        with Session(self.engine) as session:
            db_block = BlockTable(
                chain=chain,
                number=block.number,
                hash=block.hash,
                parent_hash=block.parent_hash,
                timestamp=block.timestamp,
            )
            session.merge(db_block)  # Insert or update
            session.commit()
            logger.info("block_loaded", chain=chain, block_number=block.number)

    def load_blocks(self, blocks: list[Block], chain: str) -> None:
        """Load multiple blocks to Postgres in a batch.

        Args:
            blocks: List of blocks to load
            chain: Chain identifier (e.g., "ethereum", "base")
        """
        if not blocks:
            logger.warning("load_blocks_called_with_empty_list")
            return

        with Session(self.engine) as session:
            for block in blocks:
                db_block = BlockTable(
                    chain=chain,
                    number=block.number,
                    hash=block.hash,
                    parent_hash=block.parent_hash,
                    timestamp=block.timestamp,
                )
                session.merge(db_block)  # Insert or update

            session.commit()
            logger.info("blocks_loaded", chain=chain, count=len(blocks))

    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        """Save a checkpoint to track sync progress.

        Args:
            checkpoint: Checkpoint to save
        """
        with Session(self.engine) as session:
            db_checkpoint = CheckpointTable(
                chain=checkpoint.chain,
                last_synced_block=checkpoint.last_synced_block,
                last_synced_hash=checkpoint.last_synced_hash,
                synced_at=checkpoint.synced_at,
                status=checkpoint.status,
            )
            session.merge(db_checkpoint)  # Insert or update
            session.commit()
            logger.info(
                "checkpoint_saved",
                chain=checkpoint.chain,
                block=checkpoint.last_synced_block,
            )

    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        """Load the latest checkpoint for a chain.

        Args:
            chain: Chain name (e.g., "ethereum", "base")

        Returns:
            Checkpoint if exists, None otherwise
        """
        with Session(self.engine) as session:
            db_checkpoint = session.query(CheckpointTable).filter_by(chain=chain).first()
            if db_checkpoint is None:
                logger.info("no_checkpoint_found", chain=chain)
                return None

            checkpoint = Checkpoint(
                chain=db_checkpoint.chain,  # type: ignore[arg-type]
                last_synced_block=db_checkpoint.last_synced_block,  # type: ignore[arg-type]
                last_synced_hash=db_checkpoint.last_synced_hash,  # type: ignore[arg-type]
                synced_at=db_checkpoint.synced_at,  # type: ignore[arg-type]
                status=db_checkpoint.status,  # type: ignore[arg-type]
            )
            logger.info(
                "checkpoint_loaded",
                chain=chain,
                block=checkpoint.last_synced_block,
            )
            return checkpoint

    def get_block_by_number(self, chain: str, block_number: int) -> Block | None:
        """Get a block from the database by its number.

        Args:
            chain: Chain identifier (e.g., "ethereum", "base")
            block_number: Block number to retrieve

        Returns:
            Block if found, None otherwise
        """
        with Session(self.engine) as session:
            db_block = (
                session.query(BlockTable)
                .filter_by(chain=chain, number=block_number)
                .first()
            )
            if db_block is None:
                return None

            return Block(
                number=db_block.number,  # type: ignore[arg-type]
                hash=db_block.hash,  # type: ignore[arg-type]
                parent_hash=db_block.parent_hash,  # type: ignore[arg-type]
                timestamp=db_block.timestamp,  # type: ignore[arg-type]
            )

    def detect_reorg(self, chain: str, new_block: Block) -> bool:
        """Detect if a block indicates a chain reorganization.

        Args:
            chain: Chain identifier (e.g., "ethereum", "base")
            new_block: The new block to check

        Returns:
            True if a reorg is detected, False otherwise
        """
        # Get the previous block from the database
        prev_block = self.get_block_by_number(chain, new_block.number - 1)

        if prev_block is None:
            # No previous block in DB, can't detect reorg
            return False

        # Check if the new block's parent_hash matches the previous block's hash
        if new_block.parent_hash != prev_block.hash:
            logger.warning(
                "reorg_detected",
                chain=chain,
                block_number=new_block.number,
                expected_parent=prev_block.hash,
                actual_parent=new_block.parent_hash,
            )
            return True

        return False
