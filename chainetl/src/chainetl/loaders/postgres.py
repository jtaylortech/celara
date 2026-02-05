"""Postgres data loader."""

import re

import structlog
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base

from chainetl.loaders.base import BaseLoader
from chainetl.models.block import Block
from chainetl.models.checkpoint import Checkpoint
from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer
from chainetl.models.transaction import Transaction

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


class TransactionTable(Base):  # type: ignore[misc,valid-type]
    """Transactions table."""

    __tablename__ = "transactions"

    hash = Column(String, primary_key=True)
    block_number = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(String, nullable=False)
    transaction_index = Column(Integer, nullable=False)
    from_address = Column(String, nullable=False, index=True)
    to_address = Column(String, nullable=True, index=True)
    value = Column(BigInteger, nullable=False)
    input = Column(Text, nullable=False, default="0x")
    gas = Column(BigInteger, nullable=False)
    gas_price = Column(BigInteger, nullable=True)
    max_fee_per_gas = Column(BigInteger, nullable=True)
    max_priority_fee_per_gas = Column(BigInteger, nullable=True)
    nonce = Column(BigInteger, nullable=False)
    transaction_type = Column(Integer, nullable=True)
    chain_id = Column(Integer, nullable=True)
    v = Column(String, nullable=True)
    r = Column(String, nullable=True)
    s = Column(String, nullable=True)


class LogTable(Base):  # type: ignore[misc,valid-type]
    """Logs table for smart contract events."""

    __tablename__ = "logs"

    # Composite primary key: (transaction_hash, log_index)
    transaction_hash = Column(String, primary_key=True)
    log_index = Column(Integer, primary_key=True)
    block_number = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(String, nullable=False)
    address = Column(String, nullable=False, index=True)
    data = Column(Text, nullable=False)
    topics = Column(Text, nullable=False)  # Stored as JSON array


class TokenTransferTable(Base):  # type: ignore[misc,valid-type]
    """Token transfers table for ERC-20, ERC-721, ERC-1155 events."""

    __tablename__ = "token_transfers"

    # Composite primary key: (transaction_hash, log_index)
    transaction_hash = Column(String, primary_key=True)
    log_index = Column(Integer, primary_key=True)
    block_number = Column(BigInteger, nullable=False, index=True)
    token_address = Column(String, nullable=False, index=True)
    token_standard = Column(String, nullable=False)
    from_address = Column(String, nullable=False, index=True)
    to_address = Column(String, nullable=False, index=True)
    value = Column(String, nullable=False)
    token_name = Column(String, nullable=True)
    token_symbol = Column(String, nullable=True)
    token_decimals = Column(Integer, nullable=True)


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

    def load_transaction(self, transaction: Transaction) -> None:
        """Load a transaction to Postgres.

        Args:
            transaction: Transaction to load
        """
        with Session(self.engine) as session:
            db_tx = TransactionTable(
                hash=transaction.hash,
                block_number=transaction.block_number,
                block_hash=transaction.block_hash,
                transaction_index=transaction.transaction_index,
                from_address=transaction.from_address,
                to_address=transaction.to_address,
                value=transaction.value,
                input=transaction.input,
                gas=transaction.gas,
                gas_price=transaction.gas_price,
                max_fee_per_gas=transaction.max_fee_per_gas,
                max_priority_fee_per_gas=transaction.max_priority_fee_per_gas,
                nonce=transaction.nonce,
                transaction_type=transaction.transaction_type,
                chain_id=transaction.chain_id,
                v=transaction.v,
                r=transaction.r,
                s=transaction.s,
            )
            session.merge(db_tx)
            session.commit()
            logger.debug("transaction_loaded", transaction_hash=transaction.hash)

    def load_transactions(self, transactions: list[Transaction]) -> None:
        """Load multiple transactions to Postgres in a batch.

        Args:
            transactions: List of transactions to load
        """
        if not transactions:
            return

        with Session(self.engine) as session:
            for tx in transactions:
                db_tx = TransactionTable(
                    hash=tx.hash,
                    block_number=tx.block_number,
                    block_hash=tx.block_hash,
                    transaction_index=tx.transaction_index,
                    from_address=tx.from_address,
                    to_address=tx.to_address,
                    value=tx.value,
                    input=tx.input,
                    gas=tx.gas,
                    gas_price=tx.gas_price,
                    max_fee_per_gas=tx.max_fee_per_gas,
                    max_priority_fee_per_gas=tx.max_priority_fee_per_gas,
                    nonce=tx.nonce,
                    transaction_type=tx.transaction_type,
                    chain_id=tx.chain_id,
                    v=tx.v,
                    r=tx.r,
                    s=tx.s,
                )
                session.merge(db_tx)

            session.commit()
            logger.info("transactions_loaded", count=len(transactions))

    def load_log(self, log: Log) -> None:
        """Load a log to Postgres.

        Args:
            log: Log to load
        """
        import json

        with Session(self.engine) as session:
            db_log = LogTable(
                transaction_hash=log.transaction_hash,
                log_index=log.log_index,
                block_number=log.block_number,
                block_hash=log.block_hash,
                address=log.address,
                data=log.data,
                topics=json.dumps(log.topics),  # Convert list to JSON string
            )
            session.merge(db_log)
            session.commit()
            logger.debug(
                "log_loaded", transaction_hash=log.transaction_hash, log_index=log.log_index
            )

    def load_logs(self, logs: list[Log]) -> None:
        """Load multiple logs to Postgres in a batch.

        Args:
            logs: List of logs to load
        """
        if not logs:
            return

        import json

        with Session(self.engine) as session:
            for log in logs:
                db_log = LogTable(
                    transaction_hash=log.transaction_hash,
                    log_index=log.log_index,
                    block_number=log.block_number,
                    block_hash=log.block_hash,
                    address=log.address,
                    data=log.data,
                    topics=json.dumps(log.topics),
                )
                session.merge(db_log)

            session.commit()
            logger.info("logs_loaded", count=len(logs))

    def load_token_transfer(self, token_transfer: TokenTransfer) -> None:
        """Load a token transfer to Postgres.

        Args:
            token_transfer: TokenTransfer to load
        """
        with Session(self.engine) as session:
            db_transfer = TokenTransferTable(
                transaction_hash=token_transfer.transaction_hash,
                log_index=token_transfer.log_index,
                block_number=token_transfer.block_number,
                token_address=token_transfer.token_address,
                token_standard=token_transfer.token_standard,
                from_address=token_transfer.from_address,
                to_address=token_transfer.to_address,
                value=token_transfer.value,
                token_name=token_transfer.token_name,
                token_symbol=token_transfer.token_symbol,
                token_decimals=token_transfer.token_decimals,
            )
            session.merge(db_transfer)
            session.commit()
            logger.debug(
                "token_transfer_loaded",
                transaction_hash=token_transfer.transaction_hash,
                log_index=token_transfer.log_index,
            )

    def load_token_transfers(self, token_transfers: list[TokenTransfer]) -> None:
        """Load multiple token transfers to Postgres in a batch.

        Args:
            token_transfers: List of token transfers to load
        """
        if not token_transfers:
            return

        with Session(self.engine) as session:
            for transfer in token_transfers:
                db_transfer = TokenTransferTable(
                    transaction_hash=transfer.transaction_hash,
                    log_index=transfer.log_index,
                    block_number=transfer.block_number,
                    token_address=transfer.token_address,
                    token_standard=transfer.token_standard,
                    from_address=transfer.from_address,
                    to_address=transfer.to_address,
                    value=transfer.value,
                    token_name=transfer.token_name,
                    token_symbol=transfer.token_symbol,
                    token_decimals=transfer.token_decimals,
                )
                session.merge(db_transfer)

            session.commit()
            logger.info("token_transfers_loaded", count=len(token_transfers))
