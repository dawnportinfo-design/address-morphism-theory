# Address Morphism Theory Repository Content Gap Audit

Date: 2026-06-29

## Purpose

This audit records what the Address Morphism Theory repository should contain
to become credible as an open research artifact rather than a collection of
large informal drafts.

The current repository already contains long manuscripts, verification notes,
PDF build scripts, and publication-safety checks. Its weak point is not volume.
Its weak point is that a new reader cannot immediately see:

- what is mathematically novel;
- which claims are formal, empirical, implementation-level, or speculative;
- what can be executed locally;
- where the counterexamples are;
- how AMT differs from ordinary geocoding, postal formatting, or address
  standardization.

## External Quality Anchors

The repository should align with four external expectations.

| Anchor | Repository implication |
| --- | --- |
| FAIR data principles | Claims, datasets, examples, and generated artifacts should be findable, versioned, interoperable, and reusable. |
| ACM artifact badging norms | The repo should contain runnable artifacts, not only prose. Commands should produce verifiable output locally. |
| Postal/addressing standards such as UPU S42 and ISO 19160 family | AMT must explain whether it complements or replaces address component standards. The safe answer is complement. |
| IETF/RFC specification style | Security considerations, privacy considerations, non-goals, error states, and interoperability boundaries should be explicit. |

Reference links:

- ACM Artifact Review and Badging:
  <https://www.acm.org/publications/policies/artifact-review-badging>
- FAIR Principles:
  <https://www.go-fair.org/fair-principles/>
- UPU Addressing S42 standard:
  <https://www.upu.int/en/postal-solutions/programmes-services/addressing-solutions>
- UPU / address.post S42 and ISO 19160 note:
  <https://www.address.post/home/Addressstandard>

## What To Add

### 1. A formal core paper

Add a short LaTeX paper that exposes the mathematical center of AMT:

- addressable entities as typed referents;
- surface expressions as compressed observations;
- morphism chain from surface expression to candidates to outcomes;
- explicit non-emission states;
- gate-controlled identifier issuance;
- lineage as a relation, not a function;
- conditional commutative diagrams;
- impossibility and abstention theorems.

This should be shorter than the full manuscript and should be readable as the
"minimum formal model" of AMT.

### 2. Executable reference model

Add a small local script that demonstrates the theory without external data:

- collision creates ambiguity;
- missing candidate creates unresolved;
- low-quality evidence blocks issuance;
- lineage split is not a function;
- no-postcode regions can still be modeled with AGID-first evidence;
- public/private role views do not need to expose raw address material.

This is more persuasive than another paragraph claiming that AMT is rigorous.

### 3. Claim status table

Each important claim should carry one of the following statuses:

```text
formal
executable-model
empirical-target
implementation-test
speculative
out-of-scope
```

The most important trust improvement is to avoid mixing these categories.

### 4. Counterexample catalog

The repository should promote counterexamples instead of hiding them:

- same normalized address string, multiple units;
- same coordinate, multiple floors;
- postal code covers many deliverable units;
- official source unavailable or stale;
- renamed place with surviving old references;
- split/merge administrative lineage;
- natural feature with vague boundary;
- disputed or multi-claim region;
- role conflict between delivery, emergency, tax, and property contexts.

AMT becomes more interesting when it says "a responsible resolver must abstain"
instead of pretending to solve every case.

### 5. Reader path

The README should guide three readers:

- Researcher: start with the formal core and theorem inventory.
- Developer: run the executable model and conformance checks.
- Standardization or public-sector reader: read scope, non-goals, source
  governance, privacy, and compatibility with existing address standards.

## Innovation Statement

The repository should state AMT's novelty in one paragraph:

> Address Morphism Theory treats an address as a context-indexed, evidence-bound
> partial morphism from surface expressions to typed referents, not as a string,
> coordinate, or postal component list. Its central innovation is the formal
> elevation of ambiguity, unresolved states, lineage, role-specific views, and
> gated identifier issuance into the core model. This makes false precision a
> first-class failure mode rather than an implementation bug.

## Minimum Release Bar

Before advertising AMT as serious open research, the repository should satisfy:

1. A short formal core paper exists in LaTeX.
2. At least one local executable model verifies the main negative cases.
3. README explains novelty, non-goals, and how to run checks in under one minute.
4. Publication-safety scan covers Markdown, code, JSON, and TeX.
5. Claim status is explicit for major mathematical, empirical, and protocol claims.

## Decision

This audit recommends adding:

- `papers/address-morphism-theory-formal-core.tex`
- `scripts/verify_amt_executable_model.py`
- `npm run verify:model`

Those additions make the repository more credible without over-claiming global
coverage, full ZK safety, or production AGID readiness.
