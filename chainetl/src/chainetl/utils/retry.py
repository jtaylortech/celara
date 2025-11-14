"""Retry logic with exponential backoff."""

import asyncio
import time
from typing import Any, Callable, TypeVar

import structlog

logger = structlog.get_logger()

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> T:
    """Retry a function with exponential backoff.

    Args:
        func: Callable to retry
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Multiplier for delay after each retry

    Returns:
        Result of the function call

    Raises:
        Exception: If all retries fail
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            logger.info(
                "retry_attempt",
                attempt=attempt,
                max_retries=max_retries,
            )
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                logger.warning(
                    "retry_failed_backing_off",
                    attempt=attempt,
                    delay=delay,
                    error=str(e),
                )
                time.sleep(delay)
                delay = min(delay * backoff_factor, max_delay)
            else:
                logger.error(
                    "retry_exhausted",
                    attempts=max_retries + 1,
                    error=str(e),
                )

    raise last_exception
