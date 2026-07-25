# Address Morphism Theory v2 Table Of Contents

Status: draft table of contents

## Main Paper

### 1. Why Address Registration Is Hard

Question: Why do people repeatedly type the same address, and why is that not
just a form-design problem?

Role: Defines the problem, the thesis, the reader contract, and the boundary
between addresses, maps, and identifiers.

### 2. Prior Work And The Missing Object

Question: Why do normalization, geocoding, postal codes, place IDs, and DID-like
systems not solve address identity by themselves?

Role: Turns prior work into a map of what AMT does and does not claim.

### 3. Address Objects And Registrable Entities

Question: What is the thing an address refers to?

Role: Defines referents, registrable entities, social entities, natural
geography, cultural geography, vertical units, and temporary entities.

### 4. Axioms, Notation, And Safe Abstention

Question: What minimum assumptions make address resolution computable?

Role: Gives the formal vocabulary, axiom system, refusal states, and the rule
that failed assumptions must produce abstention rather than false precision.

### 5. Candidate Generation And Evidence Policy

Question: How does a surface expression become a finite candidate set?

Role: Defines normalization, source policy, multilingual recall, candidate
sufficiency, evidence freshness, and source-coverage limits.

### 6. Structural Distance And Equivalence Classes

Question: When are two address expressions close enough to refer to the same
entity?

Role: Defines structural distance, delta-clusters, quotient maps, equivalence
classes, and counterexamples to naive string or coordinate equality.

### 7. Finite Estimation And Safe Resolution

Question: How does AMT choose, refuse, or defer?

Role: Defines finite candidate estimation, energy minimization, deterministic
tie-breaking, unresolved states, safe PID issuance, and manual review.

### 8. History Graphs, PID Conservation, And Social Continuity

Question: How can an address identifier persist through renaming, relocation,
splitting, merging, and institutional change?

Role: Defines history graphs, RPID/DPID separation, lineage transitions,
deprecation, successor identifiers, and social continuity.

### 9. Probability, Quality, Entropy, And Decision

Question: How should uncertainty, quality, and purpose-specific loss affect
address decisions?

Role: Defines Gibbs/MAP style scoring, Bayesian decision, entropy, quality
thresholds, reputation, and purpose-relative optimality.

### 10. Natural, Cultural, Vertical, And Cross-Domain References

Question: Can AMT handle places that are not ordinary street addresses?

Role: Extends AMT to seas, islands, mountains, deserts, ports, lockers, floors,
entrances, drone handoff zones, emergency shelters, and digital twins.

### 11. Protocol, Privacy, Governance, And Abuse Boundaries

Question: How can address references be used without becoming surveillance
infrastructure?

Role: Defines AMT envelopes, privacy boundaries, ZK/predicate boundaries,
governance roles, public/private projections, audit rules, and abuse controls.

### 12. Verification, Benchmarks, Limits, And Conclusion

Question: How do we know AMT is useful, and what remains unverified?

Role: Defines reproducibility, benchmarks, comparison methods, strict
non-claims, remaining S-priority risks, and the final research program.

## Appendices

### Appendix A. Core Notation

Symbols, sets, maps, states, and naming conventions.

### Appendix B. Theorem And Proof Registry

Definitions, propositions, lemmas, theorems, corollaries, and proof sketches.

### Appendix C. Counterexamples

Cases where naive address normalization, coordinate identity, postal-code
identity, or proof validity fails.

### Appendix D. Verification Map

Links from claims to fixtures, tests, executable models, and unverified items.

### Appendix E. Related Work Matrix

Comparison against normalization, geocoding, record linkage, place ID, GIS,
postal standards, DID, VC, ZK, and delivery verification systems.

### Appendix F. Implementation And Repository Map

How AMT connects to AGID, ZK Address Predicates, Address Login, postal-code
generation, country packs, ocean packs, and governance repositories.

## Decision

The v2 main paper has 12 chapters. Extra material should not become chapter 13
unless it changes the core theory. It should become an appendix, companion
paper, or executable model first.
