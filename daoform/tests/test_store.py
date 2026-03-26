"""Tests for YAML store."""

from daoform.models import Proposal, Vote, VoteChoice
from daoform.store import Store


def test_save_load_proposal(tmp_path) -> None:
    store = Store(str(tmp_path))
    p = Proposal(id="P1", title="Fund dev", author="alice")
    store.save_proposal(p)

    loaded = store.load_proposal("P1")
    assert loaded is not None
    assert loaded.id == "P1"
    assert loaded.title == "Fund dev"


def test_load_missing_proposal(tmp_path) -> None:
    store = Store(str(tmp_path))
    assert store.load_proposal("NOPE") is None


def test_list_proposals(tmp_path) -> None:
    store = Store(str(tmp_path))
    store.save_proposal(Proposal(id="P1", title="A", author="alice"))
    store.save_proposal(Proposal(id="P2", title="B", author="bob"))
    assert len(store.list_proposals()) == 2


def test_save_load_votes(tmp_path) -> None:
    store = Store(str(tmp_path))
    store.save_vote(Vote(
        proposal_id="P1", voter="alice", choice=VoteChoice.FOR, weight=10
    ))
    store.save_vote(Vote(
        proposal_id="P1", voter="bob", choice=VoteChoice.AGAINST, weight=3
    ))
    store.save_vote(Vote(
        proposal_id="P2", voter="alice", choice=VoteChoice.FOR
    ))

    p1_votes = store.load_votes("P1")
    assert len(p1_votes) == 2

    p2_votes = store.load_votes("P2")
    assert len(p2_votes) == 1


def test_empty_votes(tmp_path) -> None:
    store = Store(str(tmp_path))
    assert store.load_votes("P1") == []
