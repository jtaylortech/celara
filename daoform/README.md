# DAOForm

Governance-as-Code for DAOs. Define governance in YAML, manage proposals in code.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## What it does

Define your DAO's governance rules in a YAML config. Create proposals, cast weighted votes, and resolve outcomes with configurable quorum and threshold rules. Version-controlled governance that lives alongside your code.

## Quick Start

```bash
cd daoform
uv sync

# Initialize a DAO config
uv run daoform init --name "MyDAO"

# Validate config
uv run daoform validate

# Create a proposal
uv run daoform propose --id PROP-1 --title "Fund development" --author alice
```

## DAO Config (`dao.yaml`)

```yaml
name: MyDAO
description: Community governance
quorum: 0.1          # 10% participation required
threshold: 0.5       # 50% approval to pass
voting_period_days: 7
timelock_days: 2
```

## Python SDK

```python
from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, Vote, VoteChoice

config = DAOConfig(name="MyDAO", quorum=0.1, threshold=0.5)
engine = GovernanceEngine(config)

# Create and activate a proposal
p = engine.create_proposal(
    Proposal(id="PROP-1", title="Fund dev", author="alice")
)
p.status = ProposalStatus.ACTIVE

# Cast votes
engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice", choice=VoteChoice.FOR, weight=10))
engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob", choice=VoteChoice.AGAINST, weight=3))

# Resolve
status = engine.resolve("PROP-1")  # → ProposalStatus.PASSED
```

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

Part of [Celara](https://celara.dev) — open-source DevOps tooling for decentralized systems.
