# Governance Model

## Concepts

### DAO Config (`dao.yaml`)
The constitution of your DAO. Defines the rules that govern all proposals.

```yaml
name: MyDAO
description: Community-governed protocol
quorum: 0.1              # 10% of total voting power must participate
threshold: 0.5            # 50% of votes (excluding abstain) must be FOR
voting_period_days: 7
timelock_days: 2
token_address: null       # Optional governance token contract
```

### Proposals
A proposal is a formal request for the DAO to take action.

**Lifecycle**: `DRAFT` → `ACTIVE` → `PASSED` or `REJECTED` → `EXECUTED`

- **DRAFT**: Created but not yet open for voting
- **ACTIVE**: Open for voting
- **PASSED**: Met quorum and threshold
- **REJECTED**: Failed quorum or threshold
- **EXECUTED**: Action was carried out

### Votes
Each vote has a **choice** and a **weight**:

- **Choices**: `FOR`, `AGAINST`, `ABSTAIN`
- **Weight**: Voting power (e.g., token balance). Default: 1.0
- **Duplicate prevention**: Each voter can only vote once per proposal

### Resolution
When voting ends, the engine resolves the proposal:

1. **Quorum check**: Is `total_weight >= quorum`? If not → REJECTED
2. **Threshold check**: Is `for_weight / (for_weight + against_weight) >= threshold`? If yes → PASSED, else → REJECTED

Abstain votes count toward quorum but not toward the threshold calculation.

## Python SDK

```python
from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, ProposalStatus, Vote, VoteChoice

# Initialize
config = DAOConfig(name="MyDAO", quorum=0.1, threshold=0.5)
engine = GovernanceEngine(config)

# Create proposal
p = engine.create_proposal(Proposal(id="PROP-1", title="Fund dev", author="alice.eth"))
p.status = ProposalStatus.ACTIVE

# Vote
engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice.eth", choice=VoteChoice.FOR, weight=10))
engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob.eth", choice=VoteChoice.AGAINST, weight=3))

# Tally
tally = engine.tally("PROP-1")
# {'for': 10.0, 'against': 3.0, 'abstain': 0.0, 'total': 13.0}

# Resolve
status = engine.resolve("PROP-1")  # PASSED (76.9% > 50%)
```

## Persistence

Proposals and votes are stored as YAML in `.daoform/`:

```python
from daoform.store import Store

store = Store(".daoform")
store.save_proposal(proposal)
store.save_vote(vote)

# Later
proposal = store.load_proposal("PROP-1")
votes = store.load_votes("PROP-1")
all_proposals = store.list_proposals()
```

The Store interface is designed to be swappable — implement the same methods with PostgreSQL, SQLite, or on-chain storage.
