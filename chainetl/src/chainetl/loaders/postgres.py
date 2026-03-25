"""Postgres data loader."""

import json
import re
from typing import Any

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


def _sanitize_connection_string(cs: str) -> str:
    """Mask password in connection string."""
    return re.sub(r"(:)([^@:]+)(@)", r"\1***\3", cs)


# --- Table definitions ---


class BlockTable(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "blocks"
    chain = Column(String, primary_key=True)
    number = Column(BigInteger, primary_key=True)
    hash = Column(String, unique=True, nullable=False)
    parent_hash = Column(String, nullable=False)
    timestamp = Column(BigInteger, nullable=False)


class CheckpointTable(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "checkpoints"
    chain = Column(String, primary_key=True)
    last_synced_block = Column(BigInteger, nullable=False)
    last_synced_hash = Column(String, nullable=False)
    synced_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="active")


class TransactionTable(Base):  # type: ignore[misc,valid-type]
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
    __tablename__ = "logs"
    transaction_hash = Column(String, primary_key=True)
    log_index = Column(Integer, primary_key=True)
    block_number = Column(BigInteger, nullable=False, index=True)
    block_hash = Column(String, nullable=False)
    address = Column(String, nullable=False, index=True)
    data = Column(Text, nullable=False)
    topics = Column(Text, nullable=False)


class TokenTransferTable(Base):  # type: ignore[misc,valid-type]
    __tablename__ = "token_transfers"
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


# --- Model → Table row mappers ---


def _block_to_row(block: Block, chain: str) -> dict[str, Any]:
    return dict(
        chain=chain,
        number=block.number,
        hash=block.hash,
        parent_hash=block.parent_hash,
        timestamp=block.timestamp,
    )


def _tx_to_row(tx: Transaction) -> dict[str, Any]:
    return dict(
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


def _log_to_row(log: Log) -> dict[str, Any]:
    return dict(
        transaction_hash=log.transaction_hash,
        log_index=log.log_index,
        block_number=log.block_number,
        block_hash=log.block_hash,
        address=log.address,
        data=log.data,
        topics=json.dumps(log.topics),
    )


def _transfer_to_row(t: TokenTransfer) -> dict[str, Any]:
    return dict(
        transaction_hash=t.transaction_hash,
        log_index=t.log_index,
        block_number=t.block_number,
        token_address=t.token_address,
        token_standard=t.token_standard,
        from_address=t.from_address,
        to_address=t.to_address,
        value=t.value,
        token_name=t.token_name,
        token_symbol=t.token_symbol,
        token_decimals=t.token_decimals,
    )


# --- Loader ---


class PostgresLoader(BaseLoader):
    """Load blockchain data to PostgreSQL."""

    def __init__(self, connection_string: str) -> None:
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        logger.info(
            "postgres_loader_initialized",
            connection_string=_sanitize_connection_string(connection_string),
        )

    def _merge_batch(
        self, table_cls: type, rows: list[dict[str, Any]], label: str
    ) -> None:
        """Generic batch upsert."""
        if not rows:
            return
        with Session(self.engine) as session:
            for row in rows:
                session.merge(table_cls(**row))
            session.commit()
        logger.info(f"{label}_loaded", count=len(rows))

    # --- Blocks ---

    def load_block(self, block: Block, chain: str) -> None:
        self._merge_batch(
            BlockTable, [_block_to_row(block, chain)], "block"
        )

    def load_blocks(self, blocks: list[Block], chain: str) -> None:
        self._merge_batch(
            BlockTable,
            [_block_to_row(b, chain) for b in blocks],
            "blocks",
        )

    # --- Checkpoints ---

    def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        with Session(self.engine) as session:
            session.merge(CheckpointTable(
                chain=checkpoint.chain,
                last_synced_block=checkpoint.last_synced_block,
                last_synced_hash=checkpoint.last_synced_hash,
                synced_at=checkpoint.synced_at,
                status=checkpoint.status,
            ))
            session.commit()
        logger.info(
            "checkpoint_saved",
            chain=checkpoint.chain,
            block=checkpoint.last_synced_block,
        )

    def load_checkpoint(self, chain: str) -> Checkpoint | None:
        with Session(self.engine) as session:
            row = (
                session.query(CheckpointTable)
                .filter_by(chain=chain)
                .first()
            )
            if row is None:
                logger.info("no_checkpoint_found", chain=chain)
                return None
            return Checkpoint(
                chain=row.chain,  # type: ignore[arg-type]
                last_synced_block=row.last_synced_block,  # type: ignore[arg-type]
                last_synced_hash=row.last_synced_hash,  # type: ignore[arg-type]
                synced_at=row.synced_at,  # type: ignore[arg-type]
                status=row.status,  # type: ignore[arg-type]
            )

    # --- Reorg detection ---

    def get_block_by_number(
        self, chain: str, block_number: int
    ) -> Block | None:
        with Session(self.engine) as session:
            row = (
                session.query(BlockTable)
                .filter_by(chain=chain, number=block_number)
                .first()
            )
            if row is None:
                return None
            return Block(
                number=row.number,  # type: ignore[arg-type]
                hash=row.hash,  # type: ignore[arg-type]
                parent_hash=row.parent_hash,  # type: ignore[arg-type]
                timestamp=row.timestamp,  # type: ignore[arg-type]
            )

    def detect_reorg(self, chain: str, new_block: Block) -> bool:
        prev = self.get_block_by_number(chain, new_block.number - 1)
        if prev is None:
            return False
        if new_block.parent_hash != prev.hash:
            logger.warning(
                "reorg_detected",
                chain=chain,
                block_number=new_block.number,
                expected_parent=prev.hash,
                actual_parent=new_block.parent_hash,
            )
            return True
        return False

    # --- Transactions ---

    def load_transactions(self, transactions: list[Transaction]) -> None:
        self._merge_batch(
            TransactionTable,
            [_tx_to_row(tx) for tx in transactions],
            "transactions",
        )

    # --- Logs ---

    def load_logs(self, logs: list[Log]) -> None:
        self._merge_batch(
            LogTable, [_log_to_row(log) for log in logs], "logs"
        )

    # --- Token transfers ---

    def load_token_transfers(
        self, token_transfers: list[TokenTransfer]
    ) -> None:
        self._merge_batch(
            TokenTransferTable,
            [_transfer_to_row(t) for t in token_transfers],
            "token_transfers",
        )
