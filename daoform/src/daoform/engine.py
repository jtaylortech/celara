"""Governance engine — proposal lifecycle and vote tallying."""

from daoform.models import DAOConfig, Proposal, ProposalStatus, Vote, VoteChoice


class GovernanceEngine:
    """Manages proposals and voting."""

    def __init__(self, config: DAOConfig) -> None:
        self.config = config
        self._proposals: dict[str, Proposal] = {}
        self._votes: dict[str, list[Vote]] = {}

    def create_proposal(self, proposal: Proposal) -> Proposal:
        """Register a new proposal."""
        if proposal.id in self._proposals:
            raise ValueError(f"Proposal {proposal.id} already exists")
        proposal.quorum = self.config.quorum
        proposal.threshold = self.config.threshold
        self._proposals[proposal.id] = proposal
        self._votes[proposal.id] = []
        return proposal

    def cast_vote(self, vote: Vote) -> Vote:
        """Cast a vote on a proposal."""
        if vote.proposal_id not in self._proposals:
            raise ValueError(f"Proposal {vote.proposal_id} not found")
        proposal = self._proposals[vote.proposal_id]
        if proposal.status != ProposalStatus.ACTIVE:
            raise ValueError(f"Proposal {vote.proposal_id} is not active")
        # Check for duplicate votes
        existing = [
            v for v in self._votes[vote.proposal_id] if v.voter == vote.voter
        ]
        if existing:
            raise ValueError(f"Voter {vote.voter} already voted")
        self._votes[vote.proposal_id].append(vote)
        return vote

    def tally(self, proposal_id: str) -> dict[str, float]:
        """Tally votes for a proposal."""
        if proposal_id not in self._votes:
            raise ValueError(f"Proposal {proposal_id} not found")
        votes = self._votes[proposal_id]
        result = {"for": 0.0, "against": 0.0, "abstain": 0.0}
        for v in votes:
            result[v.choice.value] += v.weight
        total = sum(result.values())
        result["total"] = total
        result["participation"] = total  # Simplified; real impl uses token supply
        return result

    def resolve(self, proposal_id: str) -> ProposalStatus:
        """Resolve a proposal based on votes."""
        proposal = self._proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        tally = self.tally(proposal_id)
        total = tally["total"]
        if total < proposal.quorum:
            proposal.status = ProposalStatus.REJECTED
        elif total > 0 and tally["for"] / total >= proposal.threshold:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.REJECTED
        return proposal.status

    def get_proposal(self, proposal_id: str) -> Proposal | None:
        return self._proposals.get(proposal_id)

    def list_proposals(self) -> list[Proposal]:
        return list(self._proposals.values())
