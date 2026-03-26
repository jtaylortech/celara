export default function DAOFormDocs() {
  return (
    <div className="space-y-16">
      <section>
        <h1 className="text-3xl font-bold mb-4">DAOForm</h1>
        <p className="text-[var(--muted)] leading-relaxed">Governance-as-Code for DAOs. Define governance in YAML, manage proposals in code, resolve votes with configurable quorum and threshold rules.</p>
      </section>

      <section id="quick-start">
        <h2 className="text-xl font-bold mb-4">Quick Start</h2>
        <Pre code={`pip install daoform

# Initialize governance config
daoform init --name "MyDAO"

# Validate config
daoform validate

# Create a proposal
daoform propose --id PROP-1 --title "Fund development" --author alice.eth`} />
      </section>

      <section id="governance">
        <h2 className="text-xl font-bold mb-4">Governance Model</h2>
        <Pre code={`# dao.yaml — your DAO's constitution
name: MyDAO
description: Community-governed protocol
quorum: 0.1              # 10% participation required
threshold: 0.5            # 50% approval to pass
voting_period_days: 7     # Proposals open for 7 days
timelock_days: 2          # 2-day delay before execution
token_address: null       # Governance token (optional)`} />
        <div className="mt-6 text-sm text-[var(--muted)] space-y-2">
          <p><strong className="text-[var(--text)]">Proposal lifecycle:</strong> DRAFT → ACTIVE → PASSED/REJECTED → EXECUTED</p>
          <p><strong className="text-[var(--text)]">Quorum:</strong> Minimum total voting weight required. If not met, proposal is rejected regardless of vote split.</p>
          <p><strong className="text-[var(--text)]">Threshold:</strong> Percentage of FOR votes (excluding abstain) needed to pass. 0.5 = simple majority.</p>
          <p><strong className="text-[var(--text)]">Weight:</strong> Each vote has a weight representing voting power (e.g., token balance).</p>
        </div>
      </section>

      <section id="sdk">
        <h2 className="text-xl font-bold mb-4">Python SDK</h2>
        <Pre code={`from daoform.engine import GovernanceEngine
from daoform.models import DAOConfig, Proposal, ProposalStatus, Vote, VoteChoice

config = DAOConfig(name="MyDAO", quorum=0.1, threshold=0.5)
engine = GovernanceEngine(config)

# Create and activate proposal
p = engine.create_proposal(
    Proposal(id="PROP-1", title="Fund core dev", author="alice.eth")
)
p.status = ProposalStatus.ACTIVE

# Cast votes
engine.cast_vote(Vote(proposal_id="PROP-1", voter="alice.eth", choice=VoteChoice.FOR, weight=10))
engine.cast_vote(Vote(proposal_id="PROP-1", voter="bob.eth", choice=VoteChoice.AGAINST, weight=3))

# Tally
tally = engine.tally("PROP-1")
# {'for': 10.0, 'against': 3.0, 'abstain': 0.0, 'total': 13.0}

# Resolve
status = engine.resolve("PROP-1")  # PASSED (76.9% > 50%)`} />
      </section>

      <section id="storage">
        <h2 className="text-xl font-bold mb-4">Persistence</h2>
        <p className="text-sm text-[var(--muted)] mb-4">Proposals and votes are stored as YAML files in <code className="text-emerald-400">.daoform/</code>:</p>
        <Pre code={`from daoform.store import Store

store = Store(".daoform")

# Save
store.save_proposal(proposal)
store.save_vote(vote)

# Load
proposal = store.load_proposal("PROP-1")
votes = store.load_votes("PROP-1")
all_proposals = store.list_proposals()`} />
        <p className="text-sm text-[var(--muted)] mt-4">The Store class is designed to be swappable — implement the same interface with PostgreSQL, SQLite, or on-chain storage for production.</p>
      </section>

      <section id="cli">
        <h2 className="text-xl font-bold mb-4">CLI Reference</h2>
        <Table rows={[
          ["daoform init --name MyDAO", "Create dao.yaml governance config"],
          ["daoform validate --config-file dao.yaml", "Validate config"],
          ["daoform propose --id PROP-1 --title \"...\" --author alice", "Create proposal"],
        ]} />
      </section>
    </div>
  );
}

function Pre({ code }: { code: string }) {
  return <pre className="p-4 bg-[var(--bg)] border border-[var(--border)] rounded-lg text-sm overflow-x-auto mt-4"><code className="text-emerald-400">{code}</code></pre>;
}
function Table({ rows }: { rows: string[][] }) {
  return (
    <div className="border border-[var(--border)] rounded-lg overflow-hidden">
      <table className="w-full text-sm"><thead><tr className="bg-[var(--bg)]"><th className="text-left px-4 py-2 font-medium">Command</th><th className="text-left px-4 py-2 font-medium">Description</th></tr></thead>
        <tbody>{rows.map((r) => (<tr key={r[0]} className="border-t border-[var(--border)]"><td className="px-4 py-2"><code className="text-emerald-400 text-xs">{r[0]}</code></td><td className="px-4 py-2 text-[var(--muted)]">{r[1]}</td></tr>))}</tbody>
      </table>
    </div>
  );
}
