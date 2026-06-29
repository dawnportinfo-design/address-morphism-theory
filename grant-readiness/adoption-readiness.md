# Adoption Readiness: Address Morphism Theory

This note explains why Address Morphism Theory (AMT) is suitable for research,
standards, and public-interest infrastructure review.

## Review Audience

- Research programs evaluating new address theory.
- Public-good funders evaluating open infrastructure.
- Protocol reviewers evaluating whether privacy proofs have a sound resolution
  layer beneath them.
- Implementers who need a conservative way to decide when an address reference
  should not become a persistent identifier.

## Core Public-Good Claim

AMT treats an address as an evidence-bound reference problem, not as a string,
label, coordinate, or postal record alone. This matters because many regions
have incomplete postal systems, multilingual names, informal settlements,
vertical locations, disputed boundaries, and changing administrative histories.

The public-good contribution is a theory and reference model for safe address
resolution, including abstention when the evidence is insufficient.

## What Is Verifiable Today

- Chapterized theory tree with formal definitions and proof-oriented sections.
- Executable formal models for morphism chains, equivalence classes, entropy,
  history graphs, unresolvability, and verification maps.
- Publication-safety checks for public repository material.
- AMT/ZK compatibility boundary with shared interop fixtures.
- S-priority risk decomposition by region, use case, source, and failure mode.

## What Is Deliberately Not Claimed

- Global completeness of candidate generation.
- A replacement for official registries or local legal authority.
- A guarantee that privacy proofs can repair a bad resolution decision.
- Production operation of country-scale data.
- External audit completion.

## Strongest Grant Fit

- NLnet Foundation: open standards, privacy-preserving public infrastructure,
  and FOSS research artifacts.
- Internet Society Foundation: trustworthy Internet infrastructure for places
  with weak addressing coverage.
- Mozilla Foundation: public-interest technology and trustworthy AI boundaries.
- Protocol Labs: content-addressed evidence, provenance, and verifiable public
  data workflows.
- Ethereum Foundation: root-only public verification for AMT/ZK predicates,
  revocation/freshness roots, verifier policy transparency, and privacy-safe
  public-good tooling that does not put addresses on-chain.

## Next Evidence to Add

1. A compact LaTeX paper that maps every central theorem to executable tests.
2. A comparison table against geocoding, postal normalization, plus-code, and
   proprietary validation approaches.
3. A small country case study for one strong-postal, one weak-postal, and one
   no-postal-code region.
4. A machine-readable claim register that marks each claim as tested,
   documented, planned, or out of scope.
5. An Ethereum root-anchor demo proving that evidence, freshness, revocation,
   issuer, schema, and policy roots can be verified without publishing raw
   address, recipient, PID, coordinate, witness, or key material.
