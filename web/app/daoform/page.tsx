import type { Metadata } from "next";
import { ProductPage } from "../components/product-page";

export const metadata: Metadata = {
  title: "DAOForm — Governance-as-Code | Celara",
  description:
    "Governance engine for DAOs. Create proposals, manage voting, and resolve outcomes with configurable quorum and thresholds.",
};

export default function DAOForm() {
  return (
    <ProductPage
      name="DAOForm"
      tagline="Governance-as-Code"
      description="Define your DAO's governance in YAML. Create proposals, cast weighted votes, and resolve outcomes with configurable quorum and threshold rules. Version-controlled governance that lives alongside your code."
      installCmd="pip install daoform"
      features={[
        "YAML-based DAO configuration",
        "Proposal lifecycle (draft → active → passed/rejected)",
        "Weighted voting with quorum and threshold rules",
        "Vote tallying and automatic resolution",
        "CLI for init, validate, and propose workflows",
        "Pydantic models for type-safe governance data",
      ]}
      sourceUrl="https://github.com/jtaylortech/celara-homepage/tree/main/daoform"
    />
  );
}
