"""Base extractor interface."""

from abc import ABC, abstractmethod

from chainetl.models.block import Block


class BaseExtractor(ABC):
    """Base class for blockchain extractors."""

    @abstractmethod
    def extract_block(self, block_number: int) -> Block:
        """Extract a single block.

        Args:
            block_number: Block number to extract

        Returns:
            Block data
        """
        pass

    @abstractmethod
    def extract_latest_block_number(self) -> int:
        """Get the latest block number.

        Returns:
            Latest block number
        """
        pass
