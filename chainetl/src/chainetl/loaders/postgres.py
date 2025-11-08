"""Postgres data loader."""

import structlog
from sqlalchemy import BigInteger, Column, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from chainetl.loaders.base import BaseLoader
from chainetl.models.block import Block

logger = structlog.get_logger()
Base = declarative_base()


class BlockTable(Base):
    """Blocks table."""

    __tablename__ = "blocks"

    number = Column(BigInteger, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    parent_hash = Column(String, nullable=False)
    timestamp = Column(BigInteger, nullable=False)


class PostgresLoader(BaseLoader):
    """Load data to Postgres."""

    def __init__(self, connection_string: str) -> None:
        """Initialize Postgres loader.

        Args:
            connection_string: Postgres connection string
        """
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        logger.info("postgres_loader_initialized", connection_string=connection_string)

    def load_block(self, block: Block) -> None:
        """Load a block to Postgres.

        Args:
            block: Block to load
        """
        with Session(self.engine) as session:
            db_block = BlockTable(
                number=block.number,
                hash=block.hash,
                parent_hash=block.parent_hash,
                timestamp=block.timestamp,
            )
            session.merge(db_block)  # Insert or update
            session.commit()
            logger.info("block_loaded", block_number=block.number)
