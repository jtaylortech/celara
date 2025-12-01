"""Base L2 blockchain extractor."""

import structlog

from chainetl.extractors.base import BaseExtractor
from chainetl.models.block import Block
from chainetl.utils.rpc import RPCClient

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
        self.rpc = RPCClient(str(rpc_url))
        logger.info("base_l2_extractor_initialized", rpc_url=str(rpc_url))

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

    def close(self) -> None:
        """Close the RPC client connection."""
        self.rpc.close()
        logger.info("base_l2_extractor_closed")
