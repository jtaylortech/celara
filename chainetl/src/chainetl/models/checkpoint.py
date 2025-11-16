"""Checkpoint model for tracking sync progress."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Checkpoint(BaseModel):
    """Sync checkpoint for resuming from last known block."""

    chain: str = Field(..., description="Blockchain name (e.g., ethereum, base)")
    last_synced_block: int = Field(..., description="Last block successfully synced")
    last_synced_hash: str = Field(..., description="Hash of last synced block")
    synced_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Timestamp of last sync"
    )
    status: str = Field(default="active", description="Checkpoint status (active, paused, error)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "chain": "ethereum",
                "last_synced_block": 18000000,
                "last_synced_hash": (
                    "0x95b198e154acbfc64109dfd22d8224fe927fd8dfdedfae01587674482ba4baf3"
                ),
                "synced_at": "2025-11-14T12:00:00",
                "status": "active",
            }
        }
    }
