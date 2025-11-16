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

        # Note: Base blocks may have additional L2-specific fields like:
        # - l1BlockNumber: The L1 block number when this L2 block was posted
        # - l1BatchNumber: The batch number on L1
        # For now, we use the standard Block model which works for both L1 and L2
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
