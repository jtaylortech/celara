"""Tests for retry logic."""

import pytest

from chainetl.utils.retry import retry_with_backoff


def test_retry_succeeds_on_first_attempt() -> None:
    """Retry should return result on first successful call."""
    call_count = 0

    def succeeds() -> int:
        nonlocal call_count
        call_count += 1
        return 42

    result = retry_with_backoff(succeeds, max_retries=3)
    assert result == 42
    assert call_count == 1


def test_retry_succeeds_after_failures() -> None:
    """Retry should succeed if function succeeds after a few failures."""
    call_count = 0

    def fails_then_succeeds() -> int:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Not yet")
        return 99

    result = retry_with_backoff(fails_then_succeeds, max_retries=3, initial_delay=0.01)
    assert result == 99
    assert call_count == 3


def test_retry_exhausted() -> None:
    """Retry should raise exception after max retries exhausted."""

    def always_fails() -> None:
        raise RuntimeError("Always fails")

    with pytest.raises(RuntimeError, match="Always fails"):
        retry_with_backoff(always_fails, max_retries=2, initial_delay=0.01)
