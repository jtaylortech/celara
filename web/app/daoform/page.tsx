import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "DAOForm — Governance-as-Code | Celara",
  description: "Governance engine for DAOs. YAML config, proposals, weighted voting, quorum rules, persistence.",
};

export default function DAOForm() {
  return (
    <ProductPage
      name="DAOForm"
      tagline="Governance-as-Code"
      gradient="from-teal-400 to-blue-500"
      description="Define your DAO's governance in YAML. Create proposals, cast weighted votes, and resolve outcomes with configurable quorum and threshold rules. Version-controlled, auditable, reproducible. Python SDK for building governance UIs."
      installCmd="pip install daoform"
      heroCode={`$ daoform init --name "MyDAO"
Created dao.yaml for 'MyDAO'
  Quorum: 10.0%
  Threshold: 50.0%
  Voting period: 7 days

$ cat dao.yaml
name: MyDAO
quorum: 0.1
threshold: 0.5
voting_period_days: 7
timelock_days: 2

$ daoform validate
✅ Valid config for 'MyDAO'

$ daoform propose --id PROP-1 --title "Fund core development" --author alice.eth
Created proposal: PROP-1
  Title: Fund core development
  Status: draft`}
      stats={[
        { label: "Tests", value: "18" },
        { label: "Vote Types", value: "3" },
        { label: "Storage", value: "YAML" },
        { label: "Models", value: "Pydantic" },
      ]}
      features={[
        { title: "YAML Configuration", desc: "Define quorum, threshold, voting period, and timelock in a version-controlled YAML file." },
        { title: "Proposal Lifecycle", desc: "Draft → Active → Passed/Rejected → Executed. Full state machine with validation at each transition." },
        { title: "Weighted Voting", desc: "FOR, AGAINST, ABSTAIN with configurable weight per voter. Duplicate vote prevention built in." },
        { title: "Automatic Resolution", desc: "Engine checks quorum first (did enough vote?), then threshold (did enough vote FOR?). Deterministic." },
        { title: "YAML Persistence", desc: "Proposals and votes stored as YAML files. Survive restarts. Swappable for PostgreSQL or on-chain." },
        { title: "Python SDK", desc: "GovernanceEngine class for building UIs. create_proposal(), cast_vote(), tally(), resolve()." },
      ]}
      docsHref="/docs/daoform"
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/daoform"
    />
  );
}
