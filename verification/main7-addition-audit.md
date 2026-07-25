# Main 7 PDF Addition Audit

Source reviewed: `C:/Users/kitau/Downloads/main (7).pdf`

This audit records what should be newly written or migrated from the 152-page
Japanese AMT PDF into the current split Address Morphism Theory repository.

## Verdict

Yes, there are important additions. The PDF should not create a second competing
paper structure. Its strongest material should be folded into the current
29-chapter canonical paper as mathematical density, proof structure, and
implementation fixtures.

The PDF is organized as a 16-chapter formal manuscript:

1. Introduction
2. Related research
3. Central claim
4. Address ontology and mathematical structure
5. Axiom system
6. Normalization map and candidate generation
7. Structural distance and cluster construction
8. Candidate clusters and finite estimation
9. History and time structure
10. Probabilistic model
11. Optimal decision
12. Integrated structure and commutative diagrams
13. Main theorem
14. Implementation connection
15. Natural geography, terrain manifolds, and state compression
16. Vertical reference layer

## High-Value Additions

### 1. Related Research Chapter Or Appendix

Current repository gap: the split paper has no strong, standalone related
research section.

Add:

- address normalization and record linkage limitations
- geocoding limitations
- place ID and DID limitations
- geographic ontology limitations
- postal code and coordinate model limitations

Target:

- `paper/02-address-basics-reference-compression-communication-history.md`
- or a new appendix `appendices/I-related-work-map.md`

Executable artifact:

- machine-readable comparison matrix of prior methods and AMT claims

### 2. Axiom Dependency Map

Current repository gap: chapter 29 has axioms, but the PDF contains a stronger
axiomatic spine with finite candidate, structural distance, equivalence,
ordering, history, and safe abstention dependencies.

Add:

- numbered axiom table
- dependency graph from axioms to lemmas and theorems
- explicit "axiom fails -> AMT abstains" policy

Target:

- `paper/05-formal-preliminaries.md`
- `paper/29-mathematical-model-core.md`
- `appendices/B-definitions-propositions-lemmas-theorems-corollaries.md`
- `appendices/H-proof-appendix-basic-propositions.md`

Executable artifact:

- axiom-to-theorem verification map

### 3. Structural Distance And Delta-Cluster Core

Current repository gap: chapter 9 is conceptually right but too short.

Add:

- structural distance `D_t`
- threshold `delta`
- graph `G_{delta,t}`
- maximal bounded clusters
- quotient map from normalized candidates to equivalence classes
- tie-breaking order for deterministic cluster choice

Target:

- `paper/09-clusters-and-address-equivalence-classes.md`
- `paper/29-mathematical-model-core.md`
- `formal/equivalence-classes.ts`

Executable artifact:

- deterministic cluster construction fixture
- counterexample for transitive-near-but-not-diameter-bounded grouping

### 4. Finite Estimation And Energy Minimization

Current repository gap: safe resolution exists, but the PDF's finite estimation
and energy-minimization framing is stronger.

Add:

- candidate set `Phi_t(u)`
- compressed candidate class set
- bottom/refusal candidate
- energy function `E_t`
- finite argmin existence
- deterministic tie-break uniqueness

Target:

- `paper/08-candidate-generation-and-source-policy.md`
- `paper/11-safe-resolution-and-pid-issuance.md`
- `paper/14-conflict-relative-optimality.md`
- `paper/29-mathematical-model-core.md`

Executable artifact:

- finite candidate estimator test vector

### 5. Probabilistic And Bayesian Decision Layer

Current repository gap: chapter 17 covers quality and reputation, but the PDF's
probabilistic model deserves explicit formal treatment.

Add:

- Gibbs distribution over candidates
- MAP estimator
- temperature schedule
- Bayesian decision rule
- purpose-relative loss function
- uncertainty-driven abstention

Target:

- `paper/14-conflict-relative-optimality.md`
- `paper/17-evaluation-quality-and-reputation.md`
- `paper/29-mathematical-model-core.md`

Executable artifact:

- probability-to-decision fixture with abstention cases

### 6. RPID / DPID / History Conservation

Current repository gap: history and PID boundaries exist, but the PDF's
separation between theoretical persistent identifiers and deployable hash IDs
should be clearer.

Add:

- RPID as referent persistence layer
- DPID as deployable identifier layer
- lineage transitions for merge, split, rename, deprecation, and successor
- collision risk note for implementation IDs

Target:

- `paper/12-history-graph-and-address-conservation.md`
- `paper/19-pid-and-application-identifier-boundary.md`
- `paper/29-mathematical-model-core.md`

Executable artifact:

- lineage ledger fixture for split/merge/deprecation

### 7. Main Theorem Map

Current repository gap: the current chapter 29 has existence and uniqueness, but
the PDF has a broader theorem program: existence, uniqueness, stability,
convergence, conditional completeness, and impossibility.

Add:

- theorem dependency map
- explicit statement of conditional completeness
- impossibility theorem for unconditional perfect address resolution
- proof sketches linked to model tests

Target:

- `paper/29-mathematical-model-core.md`
- `appendices/B-definitions-propositions-lemmas-theorems-corollaries.md`
- `appendices/H-proof-appendix-basic-propositions.md`

Executable artifact:

- theorem registry JSON

### 8. Natural Geography And Vertical Reference Expansion

Current repository gap: chapter 16 names the topic, but the PDF gives stronger
theory around terrain manifold, natural referents, state compression, and
vertical reachability.

Add:

- natural/cultural referent taxonomy
- terrain manifold model
- non-building addressable entities
- vertical unit, entrance, locker, floor, and drone handoff references
- privacy-separating vertical reference rule

Target:

- `paper/16-natural-cultural-geography-and-vertical-reference.md`
- proposed chapter 30 governance/ethics

Executable artifact:

- vertical reachability fixture that does not expose room-level private data

## Additions Not Yet Strong In The PDF

The PDF only lightly touches these areas, so they should be written as new
material rather than migrated:

- zero-knowledge address predicates
- governance and ethical framework
- distributed registry consensus
- machine-learned parameter optimization
- XR and cross-domain address equivalence
- threat model and privacy proof boundaries

These correspond well to proposed chapters 30-33 and ZK-specific repositories.

## Formatting And Publication Fixes

The extracted PDF shows repeated glyph artifacts in headings such as duplicated
"第" and repeated Japanese title characters. Before publication:

- normalize LaTeX heading macros
- regenerate the table of contents
- ensure chapter numbers render once
- check Japanese glyph embedding
- add a bibliography section with stable references
- make theorem/definition numbering stable across chapters

## Recommended Next Work Order

1. Update `SUMMARY.md` because it currently lists fewer chapters than the
   canonical chapter inventory.
2. Expand chapter 29 with the PDF's formal theorem map.
3. Expand chapter 9 with structural distance and delta-cluster construction.
4. Expand chapter 11/14/17 with finite estimation and Bayesian decision.
5. Expand chapter 16 with natural geography and vertical reference models.
6. Add theorem registry and model fixtures.
7. Only after these are stable, promote proposed chapters 30-33.

## Non-Claims To Preserve

- AMT does not guarantee perfect global resolution without source coverage.
- ZK proofs do not repair bad address resolution.
- ML optimization must not override hard safety gates.
- Public PIDs must not expose private vertical attributes.
- Virtual or XR referents must not be confused with legal title or official
  administrative claims.
