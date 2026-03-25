"""EVM-compatible blockchain extractor.

Consolidates all EVM chain extraction logic into a single class.
Ethereum, Base, Polygon, Arbitrum — they all speak the same RPC.
"""

import structlog

from chainetl.extractors.base import BaseExtractor
from chainetl.models.block import Block
from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer
from chainetl.models.transaction import Transaction
from chainetl.utils.rpc import RPCClient
from chainetl.utils.token_parser import parse_token_transfers_from_logs

logger = structlog.get_logger()

# Type alias for full block extraction result
FullBlockData = tuple[Block, list[Transaction], list[Log], list[TokenTransfer]]


class EVMExtractor(BaseExtractor):
    """Extract data from any EVM-compatible blockchain."""

    def __init__(self, rpc_url: str, chain: str) -> None:
        self.rpc = RPCClient(rpc_url)
        self._chain = chain
        logger.info("extractor_initialized", chain=chain, rpc_url=rpc_url)

    @property
    def chain_name(self) -> str:
        return self._chain

    def close(self) -> None:
        self.rpc.close()

    # --- Block extraction ---

    def extract_block(self, block_number: int) -> Block:
        logger.info("extracting_block", block_number=block_number, chain=self._chain)
        data = self.rpc.call("eth_getBlockByNumber", [hex(block_number), False])
        if data is None:
            raise ValueError(f"Block {block_number} not found on {self._chain}")
        return Block.from_rpc(data)

    def extract_blocks(self, start_block: int, end_block: int) -> list[Block]:
        if start_block > end_block:
            raise ValueError(
                f"start_block ({start_block}) must be <= end_block ({end_block})"
            )
        logger.info(
            "extracting_blocks",
            start_block=start_block,
            end_block=end_block,
            chain=self._chain,
        )
        blocks = [self.extract_block(n) for n in range(start_block, end_block + 1)]
        logger.info("blocks_extracted", count=len(blocks), chain=self._chain)
        return blocks

    def extract_latest_block_number(self) -> int:
        result = self.rpc.call("eth_blockNumber", [])
        return int(result, 16)

    # --- Transaction extraction ---

    def extract_block_with_transactions(
        self, block_number: int
    ) -> tuple[Block, list[Transaction]]:
        logger.info(
            "extracting_block_with_transactions",
            block_number=block_number,
            chain=self._chain,
        )
        data = self.rpc.call("eth_getBlockByNumber", [hex(block_number), True])
        if data is None:
            raise ValueError(f"Block {block_number} not found on {self._chain}")

        block = Block.from_rpc(data)
        transactions = []
        for tx_data in data.get("transactions", []):
            try:
                transactions.append(Transaction.from_rpc(tx_data))
            except Exception as e:
                logger.warning(
                    "failed_to_parse_transaction",
                    error=str(e),
                    tx_hash=tx_data.get("hash"),
                    chain=self._chain,
                )

        logger.info(
            "block_with_transactions_extracted",
            block_number=block_number,
            transaction_count=len(transactions),
            chain=self._chain,
        )
        return block, transactions

    def extract_transaction_receipt(self, tx_hash: str) -> dict:
        logger.debug(
            "extracting_receipt", transaction_hash=tx_hash, chain=self._chain
        )
        receipt = self.rpc.call("eth_getTransactionReceipt", [tx_hash])
        if receipt is None:
            raise ValueError(f"Receipt {tx_hash} not found on {self._chain}")
        return receipt

    # --- Log extraction ---

    def extract_logs_from_receipt(self, receipt: dict) -> list[Log]:
        logs = []
        for log_data in receipt.get("logs", []):
            try:
                logs.append(Log.from_rpc(log_data))
            except Exception as e:
                logger.warning(
                    "failed_to_parse_log",
                    error=str(e),
                    tx_hash=receipt.get("transactionHash"),
                    chain=self._chain,
                )
        return logs

    # --- Composite extraction ---

    def extract_transaction_with_logs(
        self, tx_hash: str
    ) -> tuple[dict, list[Log], list[TokenTransfer]]:
        logger.info(
            "extracting_transaction_with_logs",
            transaction_hash=tx_hash,
            chain=self._chain,
        )
        receipt = self.extract_transaction_receipt(tx_hash)
        logs = self.extract_logs_from_receipt(receipt)
        block_number = int(receipt.get("blockNumber", "0x0"), 16)
        transfers = parse_token_transfers_from_logs(logs, tx_hash, block_number)
        logger.info(
            "transaction_with_logs_extracted",
            transaction_hash=tx_hash,
            log_count=len(logs),
            transfer_count=len(transfers),
            chain=self._chain,
        )
        return receipt, logs, transfers

    def extract_block_with_full_data(
        self, block_number: int
    ) -> FullBlockData:
        logger.info(
            "extracting_block_with_full_data",
            block_number=block_number,
            chain=self._chain,
        )
        block, transactions = self.extract_block_with_transactions(block_number)
        all_logs: list[Log] = []
        all_transfers: list[TokenTransfer] = []

        for tx in transactions:
            try:
                _, logs, transfers = self.extract_transaction_with_logs(tx.hash)
                all_logs.extend(logs)
                all_transfers.extend(transfers)
            except Exception as e:
                logger.warning(
                    "failed_to_extract_tx_logs",
                    error=str(e),
                    tx_hash=tx.hash,
                    chain=self._chain,
                )

        logger.info(
            "block_with_full_data_extracted",
            block_number=block_number,
            tx_count=len(transactions),
            log_count=len(all_logs),
            transfer_count=len(all_transfers),
            chain=self._chain,
        )
        return block, transactions, all_logs, all_transfers
