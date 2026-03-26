"""YAML-based persistence for proposals and votes."""

import json
from pathlib import Path

import yaml

from daoform.models import Proposal, Vote


class Store:
    """File-backed store for governance data."""

    def __init__(self, data_dir: str = ".daoform") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._proposals_file = self.data_dir / "proposals.yaml"
        self._votes_file = self.data_dir / "votes.yaml"

    def save_proposal(self, proposal: Proposal) -> None:
        proposals = self._load_proposals_raw()
        proposals[proposal.id] = json.loads(proposal.model_dump_json())
        self._proposals_file.write_text(yaml.dump(proposals))

    def load_proposal(self, proposal_id: str) -> Proposal | None:
        proposals = self._load_proposals_raw()
        data = proposals.get(proposal_id)
        if data is None:
            return None
        return Proposal(**data)

    def list_proposals(self) -> list[Proposal]:
        proposals = self._load_proposals_raw()
        return [Proposal(**v) for v in proposals.values()]

    def save_vote(self, vote: Vote) -> None:
        votes = self._load_votes_raw()
        key = f"{vote.proposal_id}:{vote.voter}"
        votes[key] = json.loads(vote.model_dump_json())
        self._votes_file.write_text(yaml.dump(votes))

    def load_votes(self, proposal_id: str) -> list[Vote]:
        votes = self._load_votes_raw()
        return [
            Vote(**v) for k, v in votes.items()
            if k.startswith(f"{proposal_id}:")
        ]

    def _load_proposals_raw(self) -> dict:
        if not self._proposals_file.exists():
            return {}
        return yaml.safe_load(self._proposals_file.read_text()) or {}

    def _load_votes_raw(self) -> dict:
        if not self._votes_file.exists():
            return {}
        return yaml.safe_load(self._votes_file.read_text()) or {}
