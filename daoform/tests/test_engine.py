"""Tests for governance engine."""

import pytest

from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, ProposalStatus, Vote, VoteChoice


@pytest.fixture
def engine() -> GovernanceEngine:
    config = DAOConfig(name="TestDAO", quorum=0.1, threshold=0.5)
    return GovernanceEngine(config)


@pytest.fixture
def active_proposal(engine: GovernanceEngine) -> Proposal:
    p = engine.create_proposal(
        Proposal(id="PROP-1", title="Test", author="alice")
    )
    p.status = ProposalStatus.ACTIVE
    return p


def test_create_proposal(engine: GovernanceEngine) -> None:
    p = engine.create_proposal(
        Proposal(id="PROP-1", title="Fund dev", author="alice")
    )
    assert p.id == "PROP-1"
    assert p.status == ProposalStatus.DRAFT


def test_duplicate_proposal(engine: GovernanceEngine) -> None:
    engine.create_proposal(Proposal(id="PROP-1", title="A", author="alice"))
    with pytest.raises(ValueError, match="already exists"):
        engine.create_proposal(Proposal(id="PROP-1", title="B", author="bob"))


def test_cast_vote(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    vote = engine.cast_vote(
        Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.FOR)
    )
    assert vote.voter == "bob"


def test_duplicate_vote(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.FOR))
    with pytest.raises(ValueError, match="already voted"):
        engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.AGAINST))


def test_vote_on_draft(engine: GovernanceEngine) -> None:
    engine.create_proposal(Proposal(id="PROP-1", title="A", author="alice"))
    with pytest.raises(ValueError, match="not active"):
        engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.FOR))


def test_tally(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice", choice=VoteChoice.FOR, weight=10))
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.AGAINST, weight=3))
    tally = engine.tally("PROP-1")
    assert tally["for"] == 10
    assert tally["against"] == 3
    assert tally["total"] == 13


def test_resolve_passed(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice", choice=VoteChoice.FOR, weight=10))
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.AGAINST, weight=3))
    status = engine.resolve("PROP-1")
    assert status == ProposalStatus.PASSED


def test_resolve_rejected(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice", choice=VoteChoice.FOR, weight=2))
    engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.AGAINST, weight=10))
    status = engine.resolve("PROP-1")
    assert status == ProposalStatus.REJECTED


def test_resolve_no_quorum(engine: GovernanceEngine, active_proposal: Proposal) -> None:
    # quorum is 0.1, no votes = 0 participation
    status = engine.resolve("PROP-1")
    assert status == ProposalStatus.REJECTED


def test_list_proposals(engine: GovernanceEngine) -> None:
    engine.create_proposal(Proposal(id="P1", title="A", author="alice"))
    engine.create_proposal(Proposal(id="P2", title="B", author="bob"))
    assert len(engine.list_proposals()) == 2
