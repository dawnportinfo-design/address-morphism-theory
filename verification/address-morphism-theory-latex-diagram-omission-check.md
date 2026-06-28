# Address Morphism Theory LaTeX diagram and omission check

Date: 2026-06-27

## Verdict

Address Morphism Theory is structurally strong enough to be presented as a
theory of address semantics and safe resolution. The core manuscript already
contains the main ingredients:

- addressable entities and surface expressions;
- observation and normalization;
- impossibility under non-injective observation;
- candidate generation;
- structural dissimilarity and clustering;
- non-emitting states;
- PID issuance gates;
- lineage graphs;
- context-relative optimality;
- natural geography and vertical reference;
- security and ZK boundaries.

The main missing element was not another theorem. The missing element was a
small set of explicit LaTeX-ready diagrams that explain what is expected to
commute, what is partial, and where AMT stops before AGID/AOID and ZK protocol
details begin.

## Required additions made

The following additions were made to the active manuscripts:

- English full paper:
  - `papers/address-morphism-theory-full-paper-en-v3.md`
  - Added `Appendix P.6 LaTeX Diagram Set for the Final Version`.
- Japanese master paper:
  - `papers/address-morphism-theory-ja-v1-master.md`
  - Added `G.8 最終LaTeX版に必須の可換図式`.

The added diagram set covers:

1. AMT morphism chain.
2. Observation, normalization, and partial inversion.
3. Certified PID issuance gate.
4. AMT / AGID / AOID / ZK boundary.
5. Natural feature, display point, access point, and handoff point.

## Protocol-paper assessment

AMT can be called a protocol-adjacent theory or a semantic foundation for
address protocols. It should not be described as the full AGID/AOID protocol by
itself. The strongest framing is:

> AMT defines the semantic and safety model for address resolution. AGID/AOID,
> Secure Address QR, resolver APIs, SDK conformance, and ZK proof bundles are
> protocol layers built on top of AMT.

This framing is safer than calling AMT alone a complete protocol, because AMT
does not fully specify wire formats, API endpoints, replay protection,
credential roots, nullifiers, revocation, freshness, or conformance vectors.

## ZK placement

Zero-knowledge proof material should remain a companion paper. The AMT paper
should include only:

- address attributes as semantic inputs to predicates;
- a boundary diagram showing how AMT outputs feed proof systems;
- a warning that ZK does not prove address truth unless AMT gates, source
  freshness, lineage, and issuer policy are also represented or audited.

The ZK paper should own:

- circuits;
- witnesses;
- public statements;
- nullifiers;
- scope/domain separation;
- freshness and revocation roots;
- anonymity-set analysis;
- proof-bundle compatibility;
- cryptographic security assumptions and audits.

## Remaining recommended checks

Before final PDF publication:

- Confirm every diagram says whether it is total, partial, or conditional.
- Add captions near the first appearance of each diagram in the body, not only
  in appendices.
- Ensure the LaTeX build includes `tikz-cd` or convert diagrams to ordinary
  figure graphics.
- Keep raw address examples out of public proof and QR sections.
- Keep AMT, AGID/AOID, and ZK claims separated in the abstract and conclusion.

