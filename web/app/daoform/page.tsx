import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "DAOForm — Governance-as-Code | Celara",
  description: "Governance engine for DAOs. YAML config, proposals, weighted voting, quorum rules.",
};

export default function DAOForm() {
  return (
    <ProductPage
      name="DAOForm"
      tagline="Governance-as-Code"
      description="Define your DAO's governance rules in a YAML config file. Create proposals, cast weighted votes, and resolve outcomes with configurable quorum and threshold rules. Everything is version-controlled, auditable, and reproducible. Includes a Python SDK for building governance UIs and a YAML-backed persistence layer so proposals survive restarts."
      installCmd="pip install daoform"
      features={[
        "YAML-based DAO configuration (quorum, threshold, voting period, timelock)",
        "Proposal lifecycle management (draft → active → passed/rejected → executed)",
        "Weighted voting with duplicate vote prevention",
        "Automatic resolution based on quorum and threshold rules",
        "YAML file persistence — proposals and votes survive restarts",
        "Python SDK with GovernanceEngine class for building UIs",
        "CLI for init, validate, and propose workflows",
        "Pydantic models for type-safe governance data",
      ]}
      quickStart={[
        {
          title: "Initialize a DAO",
          language: "bash",
          code: `pip install daoform

daoform init --name "MyDAO"
# Creates dao.yaml with default governance rules`,
        },
        {
          title: "dao.yaml configuration",
          language: "yaml",
          code: `# dao.yaml — your DAO's governance constitution
name: MyDAO
description: Community-governed protocol
quorum: 0.1              # 10% of voting power must participate
threshold: 0.5            # 50% approval required to pass
voting_period_days: 7     # Proposals open for 7 days
timelock_days: 2          # 2-day delay before execution
token_address: null       # Optional: governance token contract`,
        },
        {
          title: "Python SDK — full governance flow",
          language: "python",
          code: `from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, ProposalStatus, Vote, VoteChoice

# Load config
config = DAOConfig(name="MyDAO", quorum=0.1, threshold=0.5)
engine = GovernanceEngine(config)

# Create a proposal
proposal = engine.create_proposal(
    Proposal(id="PROP-1", title="Fund core development", author="alice.eth")
)
proposal.status = ProposalStatus.ACTIVE

# Cast weighted votes
engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice.eth", choice=VoteChoice.FOR, weight=10))
engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob.eth", choice=VoteChoice.AGAINST, weight=3))
engine.cast_vote(Vote(proposal_id="PROP-1", voter="carol.eth", choice=VoteChoice.ABSTAIN, weight=2))

# Tally and resolve
tally = engine.tally("PROP-1")
# {'for': 10.0, 'against': 3.0, 'abstain': 2.0, 'total': 15.0}

status = engine.resolve("PROP-1")
# ProposalStatus.PASSED (10/13 = 76.9% > 50% threshold)`,
        },
        {
          title: "Persistence — proposals survive restarts",
          language: "python",
          code: `from daoform.store import Store
from daoform.models import Proposal, Vote, VoteChoice

store = Store(".daoform")  # YAML files in .daoform/

# Save a proposal
store.save_proposal(Proposal(id="PROP-1", title="Fund dev", author="alice.eth"))

# Save votes
store.save_vote(Vote(proposal_id="PROP-1", voter="bob.eth", choice=VoteChoice.FOR, weight=5))

# Load later
proposal = store.load_proposal("PROP-1")
votes = store.load_votes("PROP-1")`,
        },
      ]}
      cliReference={[
        { command: "daoform init --name MyDAO", description: "Create a new dao.yaml governance config" },
        { command: "daoform validate --config-file dao.yaml", description: "Validate governance config" },
        { command: "daoform propose --id PROP-1 --title \"Fund dev\" --author alice", description: "Create a new proposal" },
      ]}
      docs={[
        {
          heading: "Governance Model",
          content: `DAOForm implements a simple but complete governance model:

1. Configuration: Define quorum (minimum participation) and threshold (approval percentage) in YAML
2. Proposals: Anyone can create a proposal. Proposals start as DRAFT and must be moved to ACTIVE before voting
3. Voting: Voters cast weighted votes (FOR, AGAINST, ABSTAIN). Each voter can only vote once per proposal
4. Resolution: When voting ends, the engine checks quorum first (did enough people vote?), then threshold (did enough vote FOR?)
5. Execution: Passed proposals move to EXECUTED status (on-chain execution is planned for v0.2)

The weight parameter represents voting power — in a token-weighted DAO, this would be the voter's token balance.`,
        },
        {
          heading: "Data Storage",
          content: `DAOForm uses YAML files for persistence:

.daoform/proposals.yaml — all proposals keyed by ID
.daoform/votes.yaml — all votes keyed by "proposal_id:voter"

This is intentionally simple. For production DAOs, you'd want a database backend. The Store class is designed to be swappable — implement the same interface with PostgreSQL, SQLite, or on-chain storage.`,
        },
        {
          heading: "Roadmap",
          content: `v0.1 (current): Core governance engine, YAML persistence, CLI
v0.2 (planned): Snapshot integration for off-chain voting
v0.3 (planned): Gnosis Safe integration for on-chain execution
v0.4 (planned): Discord/Slack notifications for proposal lifecycle events`,
        },
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/daoform"
    />
  );
}
