"""Base loader interface."""

from abc import ABC, abstractmethod

from chainetl.models.block import Block


class BaseLoader(ABC):
    """Base class for data loaders."""

    @abstractmethod
    def load_block(self, block: Block) -> None:
        """Load a block to destination.

        Args:
            block: Block to load
        """
        pass
