"""Base L2 blockchain extractor."""

import structlog

from chainetl.extractors.base import BaseExtractor
from chainetl.models.block import Block
from chainetl.models.log import Log
from chainetl.models.token_transfer import TokenTransfer
from chainetl.models.transaction import Transaction
from chainetl.utils.rpc import RPCClient
from chainetl.utils.token_parser import parse_token_transfers_from_logs

logger = structlog.get_logger()


class BaseL2Extractor(BaseExtractor):
    """Extract data from Base L2 blockchain.

    Base is an Optimistic Rollup (Layer 2) built on Ethereum. It uses the same
    RPC interface as Ethereum (EVM-compatible) but may have additional L2-specific
    fields in blocks.
    """

    def __init__(self, rpc_url: str) -> None:
        """Initialize Base L2 extractor.

        Args:
            rpc_url: Base L2 RPC endpoint URL
        """
        self.rpc = RPCClient(rpc_url)
        logger.info("base_l2_extractor_initialized", rpc_url=rpc_url)

    @property
    def chain_name(self) -> str:
        """Get the name of the blockchain.

        Returns:
            "base"
        """
        return "base"

    def extract_block(self, block_number: int) -> Block:
        """Extract a single block from Base L2.

        Args:
            block_number: Block number to extract

        Returns:
            Block data

        Raises:
            ValueError: If block not found
        """
        logger.info("extracting_block", block_number=block_number, chain="base")

        # Base uses the same RPC interface as Ethereum (EVM-compatible)
        data = self.rpc.call("eth_getBlockByNumber", [hex(block_number), False])

        if data is None:
            raise ValueError(f"Block {block_number} not found on Base L2")

        # L2-Specific Fields Documentation:
        # Base blocks may contain additional fields not present in Ethereum L1:
        #
        # - l1BlockNumber: The Ethereum L1 block number when this L2 block was posted
        # - l1BatchNumber: The batch number on L1 (for rollup compression)
        # - l1Timestamp: The L1 block timestamp
        # - sequenceNumber: The sequence number within the batch
        #
        # Special Transaction Types:
        # - Deposit transactions: L1 → L2 transfers (from Ethereum to Base)
        # - Withdrawal transactions: L2 → L1 transfers (from Base to Ethereum)
        #
        # Current Implementation:
        # We use the standard Block model which captures the core fields (number, hash,
        # timestamp, parent_hash) that are common to both L1 and L2. The L2-specific
        # fields are available in the RPC response but not yet persisted to the database.
        #
        # Future Enhancement:
        # A future version may extend the Block model to include L2-specific fields
        # and handle deposit/withdrawal transactions separately.
        return Block.from_rpc(data)

    def extract_blocks(self, start_block: int, end_block: int) -> list[Block]:
        """Extract a range of blocks from Base L2.

        Args:
            start_block: Starting block number (inclusive)
            end_block: Ending block number (inclusive)

        Returns:
            List of blocks

        Raises:
            ValueError: If start_block > end_block or if any block not found
        """
        if start_block > end_block:
            raise ValueError(f"start_block ({start_block}) must be <= end_block ({end_block})")

        logger.info(
            "extracting_blocks",
            start_block=start_block,
            end_block=end_block,
            chain="base",
        )

        blocks = []
        for block_number in range(start_block, end_block + 1):
            block = self.extract_block(block_number)
            blocks.append(block)

        logger.info("blocks_extracted", count=len(blocks), chain="base")
        return blocks

    def extract_latest_block_number(self) -> int:
        """Get the latest block number from Base L2.

        Returns:
            Latest block number

        Raises:
            ValueError: If unable to fetch latest block number
        """
        result = self.rpc.call("eth_blockNumber", [])
        return int(result, 16)

    def extract_block_with_transactions(self, block_number: int) -> tuple[Block, list[Transaction]]:
        """Extract a block with full transaction data from Base L2.

        Args:
            block_number: Block number to extract

        Returns:
            Tuple of (Block, list of Transactions)

        Raises:
            ValueError: If block not found
        """
        logger.info("extracting_block_with_transactions", block_number=block_number, chain="base")

        # Request block with full transaction objects (True parameter)
        data = self.rpc.call("eth_getBlockByNumber", [hex(block_number), True])

        if data is None:
            raise ValueError(f"Block {block_number} not found on Base L2")

        # Parse block metadata
        block = Block.from_rpc(data)

        # Parse transactions
        transactions = []
        tx_list = data.get("transactions", [])

        for tx_data in tx_list:
            try:
                transaction = Transaction.from_rpc(tx_data)
                transactions.append(transaction)
            except Exception as e:
                logger.warning(
                    "failed_to_parse_transaction",
                    error=str(e),
                    tx_hash=tx_data.get("hash"),
                    block_number=block_number,
                    chain="base",
                )

        logger.info(
            "block_with_transactions_extracted",
            block_number=block_number,
            transaction_count=len(transactions),
            chain="base",
        )

        return block, transactions

    def extract_transaction_receipt(self, transaction_hash: str) -> dict:
        """Extract transaction receipt from Base L2.

        Args:
            transaction_hash: Transaction hash

        Returns:
            Transaction receipt data

        Raises:
            ValueError: If receipt not found
        """
        logger.debug(
            "extracting_transaction_receipt", transaction_hash=transaction_hash, chain="base"
        )

        receipt = self.rpc.call("eth_getTransactionReceipt", [transaction_hash])

        if receipt is None:
            raise ValueError(f"Transaction receipt {transaction_hash} not found on Base L2")

        return receipt

    def extract_logs_from_receipt(self, receipt: dict) -> list[Log]:
        """Extract logs from a Base L2 transaction receipt.

        Args:
            receipt: Transaction receipt data

        Returns:
            List of Log objects
        """
        logs = []
        raw_logs = receipt.get("logs", [])

        for log_data in raw_logs:
            try:
                log = Log.from_rpc(log_data)
                logs.append(log)
            except Exception as e:
                logger.warning(
                    "failed_to_parse_log",
                    error=str(e),
                    transaction_hash=receipt.get("transactionHash"),
                    chain="base",
                )

        return logs

    def extract_transaction_with_logs(
        self, transaction_hash: str
    ) -> tuple[dict, list[Log], list[TokenTransfer]]:
        """Extract a transaction with its logs and parsed token transfers from Base L2.

        Args:
            transaction_hash: Transaction hash

        Returns:
            Tuple of (receipt, logs, token_transfers)

        Raises:
            ValueError: If receipt not found
        """
        logger.info(
            "extracting_transaction_with_logs", transaction_hash=transaction_hash, chain="base"
        )

        # Get receipt
        receipt = self.extract_transaction_receipt(transaction_hash)

        # Extract logs
        logs = self.extract_logs_from_receipt(receipt)

        # Parse token transfers
        block_number = int(receipt.get("blockNumber", "0x0"), 16)
        token_transfers = parse_token_transfers_from_logs(logs, transaction_hash, block_number)

        logger.info(
            "transaction_with_logs_extracted",
            transaction_hash=transaction_hash,
            log_count=len(logs),
            token_transfer_count=len(token_transfers),
            chain="base",
        )

        return receipt, logs, token_transfers

    def extract_block_with_full_data(
        self, block_number: int
    ) -> tuple[Block, list[Transaction], list[Log], list[TokenTransfer]]:
        """Extract a block with transactions, logs, and token transfers from Base L2.

        This is the most comprehensive extraction method that fetches:
        - Block metadata
        - All transactions in the block
        - All logs from all transactions
        - All parsed token transfers (ERC-20, ERC-721)

        Args:
            block_number: Block number to extract

        Returns:
            Tuple of (block, transactions, logs, token_transfers)

        Raises:
            ValueError: If block not found
        """
        logger.info("extracting_block_with_full_data", block_number=block_number, chain="base")

        # Extract block and transactions
        block, transactions = self.extract_block_with_transactions(block_number)

        # Extract logs and token transfers for each transaction
        all_logs = []
        all_token_transfers = []

        for tx in transactions:
            try:
                receipt, logs, token_transfers = self.extract_transaction_with_logs(tx.hash)
                all_logs.extend(logs)
                all_token_transfers.extend(token_transfers)
            except Exception as e:
                logger.warning(
                    "failed_to_extract_transaction_logs",
                    error=str(e),
                    transaction_hash=tx.hash,
                    block_number=block_number,
                    chain="base",
                )

        logger.info(
            "block_with_full_data_extracted",
            block_number=block_number,
            transaction_count=len(transactions),
            log_count=len(all_logs),
            token_transfer_count=len(all_token_transfers),
            chain="base",
        )

        return block, transactions, all_logs, all_token_transfers
