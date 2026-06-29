# Address Morphism Theory

Independent research repository for Address Morphism Theory (AMT).

**New to AMT? Start with [`RESUME.md`](RESUME.md).** It explains why address
reference needs a theory, what is innovative, where AMT is competitive, and how
researchers, developers, standards readers, and AGID implementers can use it.

AMT models address resolution as a chain of evidence-sensitive morphisms from
surface expressions to addressable physical, social, virtual, or institutional
entities. It treats ambiguity, incomplete candidates, lineage, unresolved
states, persistent identifiers, and privacy-preserving predicates as first-class
research objects.

## Why This Is Different

AMT does not treat an address as only a string, coordinate, postal-code record,
or formatted label. It treats an address as a context-indexed, evidence-bound
partial morphism from surface expressions to typed referents.

The core claim is deliberately conservative: a responsible address resolver must
know when not to emit a precise identifier. Ambiguous, unresolved, and rejected
states are part of the theory, not implementation failures.

## Reader Paths

- **First-time reader:** read `RESUME.md` before the formal material. It gives a
  non-specialist map of the problem, innovation, use cases, and current limits.
- **Researcher:** start with `chapters/README.md`, then read the chapterized
  core theory under `chapters/address-morphism-theory/`. Use
  `papers/address-morphism-theory-formal-core.tex` as the compact formal source.
- **Developer:** run `npm run verify:model` to see the executable abstention
  model, then inspect `verification/address-morphism-executable-expectations.md`.
  For privacy predicates, run `npm run verify:predicate-dsl` and inspect
  `src/address_morphism/predicate_dsl.py`.
- **ZK reviewer:** start with `zk/README.md`. It splits ZK materials into
  theory, specification, implementation, applications, and unverified claims,
  and explains which paper is canonical.
- **Standards / public-sector reader:** read the scope and non-goals in the
  formal core, then `verification/repository-content-gap-audit.md` for the
  trust and artifact roadmap.
- **Reviewer:** read `verification/main5-formal-additions.md` to see which
  manuscript ideas were promoted into definitions, theorems, and tests.
- **Risk reviewer:** run `npm run verify:s-priority-decomposition` and read
  `verification/s-priority-decomposition-verification.md` to see how the top
  unverified claims are split by region, use case, source, and failure mode.

## Repository Layout

- `chapters/` - chapterized reader paths split by theory type and paper series.
- `zk/` - canonical ZK material map, specification notes, app notes, and
  duplicate-paper cleanup guidance.
- `papers/` - active English and Japanese manuscripts.
- `notes/` - chapter drafts, outlines, and research resumes.
- `verification/` - claim maps, expectation tests, audits, and verification boundaries.
- `src/` - small dependency-free executable reference models.
- `scripts/` - local manuscript assembly and PDF generation tools.
- `output/pdf/` - generated PDFs and HTML exports. This directory is ignored by Git.

## Chapterized Reading Paths

- Cross-series table of contents: `chapters/table-of-contents.md`
- Core AMT: `chapters/address-morphism-theory/`
- Zero-knowledge address predicates: `chapters/zero-knowledge-address-predicates/`
- ZK material map: `zk/README.md`
- Address translation theory: `chapters/address-translation-theory/`
- Address machine translation theory: `chapters/address-machine-translation-theory/`
- Postal-zone generation theory: `chapters/postal-zone-generation-theory/`

The chapter index is machine-checked by `npm run verify:chapters`.
The ZK material map is machine-checked by `npm run verify:zk-materials`.
Each chapter now has a paired executable mathematical model under the chapter
series' `models/` directory, plus a `*.model-tests.json` fixture. These models
are small local references for claims, not production systems.

## Primary Manuscripts

- `papers/address-morphism-theory-formal-core.tex`
- `papers/address-morphism-theory-full-paper-en-v3.md`
- `papers/address-morphism-theory-ja-v1-master.md`
- `papers/address-morphism-theory-protocol-expansion-ja-v1.md`
- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md`
- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates-ja-v1.md`

## Companion Theory Papers

- `papers/address-translation-theory-ja-v1.md` - address translation as
  purpose-specific restructuring, not literal language translation.
- `papers/address-machine-translation-theory-ja-v1.md` - guarded machine
  translation for address structures.
- `papers/address-morphism-theory-protocol-expansion-ja-v1.md` - private
  delivery objects, role-based views, delivery predicates, paperless handoff,
  and AGID/AOID protocol boundaries over AMT.

## Build

```powershell
npm run verify:model
npm run verify:chapters
npm run verify:predicate-dsl
npm run verify:zk-materials
npm run build:full-pdfs
npm run build:bilingual
npm run verify
```

The build is local-only. It does not call external services.
Generated PDF and HTML files are written to `output/pdf/`, which is ignored by Git.

`npm run verify` checks the repository layout and verifies that the generated
PDFs have expected page counts, sizes, and extractable text. It also runs a
local publication-safety scan for secret keys, token-like strings, and witness
or proof material that should never be published.
`npm run verify:model` runs a small executable AMT model covering normalization
collision, missing candidates, gate rejection, no-postcode AGID-first handling,
relational lineage, context-relative optimality, entropy reduction, abstention
monotonicity, and predicate anonymity-set checks.
`npm run verify:predicate-dsl` runs a small zero-knowledge-ready predicate model
that evaluates region, quality, freshness, consent, revocation, nullifier, and
anonymity-set rules without exposing raw address material in public signals.
`npm run verify:zk-materials` verifies that ZK materials are separated into
theory, specification, implementation, applications, and unverified claims, and
that exactly one ZK paper is marked canonical.
`npm run verify:s-priority-decomposition` verifies that the highest-risk
unverified claims are decomposed by region, use case, data source, metrics, and
failure behavior, and that failure states block precise verified issuance.
PDF verification writes `output/pdf/address-morphism-theory-pdf-manifest.json`
with page counts, byte sizes, and SHA-256 hashes for generated PDFs.

## Trust Model

Claims in this repository should be classified as one of:

- `formal`
- `executable-model`
- `empirical-target`
- `implementation-test`
- `speculative`
- `out-of-scope`

The project should not present empirical coverage, production AGID behavior,
or zero-knowledge proof security as solved by the AMT paper alone. The formal
paper defines the address reference model; companion work must validate global
data coverage, operational security, and cryptographic proof systems.

## Boundary With AGID

This repository owns the theory, papers, and verification notes.

AGID should treat AMT as an external research dependency:

- AGID implements address IDs, QR, resolver, SDK, and operational workflows.
- AMT defines the formal model, impossibility boundaries, unresolved states,
  lineage semantics, and privacy-preserving predicate theory.

## Release Rules

- Do not publish raw personal addresses, recipient data, witnesses, private keys,
  or proof material.
- Keep empirical claims tied to `verification/` notes.
- Separate theory claims from AGID product or protocol implementation claims.

## License

- Papers, notes, and verification documents: CC BY 4.0. See `LICENSE-PAPERS.md`.
- Build and verification scripts: MIT. See `LICENSE`.
