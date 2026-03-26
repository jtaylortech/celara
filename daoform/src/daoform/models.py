"""Governance data models."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ProposalStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"


class VoteChoice(StrEnum):
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


class Proposal(BaseModel):
    """A governance proposal."""

    id: str = Field(..., description="Proposal identifier")
    title: str = Field(..., description="Proposal title")
    description: str = Field("", description="Proposal body (markdown)")
    author: str = Field(..., description="Author address or name")
    status: ProposalStatus = Field(default=ProposalStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.now)
    voting_start: datetime | None = Field(None)
    voting_end: datetime | None = Field(None)
    quorum: float = Field(default=0.1, description="Required participation (0-1)")
    threshold: float = Field(default=0.5, description="Pass threshold (0-1)")


class Vote(BaseModel):
    """A vote on a proposal."""

    proposal_id: str
    voter: str
    choice: VoteChoice
    weight: float = Field(default=1.0, description="Voting power")
    timestamp: datetime = Field(default_factory=datetime.now)


class DAOConfig(BaseModel):
    """DAO governance configuration."""

    name: str = Field(..., description="DAO name")
    description: str = Field("", description="DAO description")
    token_address: str | None = Field(None, description="Governance token")
    quorum: float = Field(default=0.1)
    threshold: float = Field(default=0.5)
    voting_period_days: int = Field(default=7)
    timelock_days: int = Field(default=2)
