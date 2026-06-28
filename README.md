# Address Morphism Theory

Independent research repository for Address Morphism Theory (AMT).

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

- **Researcher:** start with `papers/address-morphism-theory-formal-core.tex`,
  then the theorem inventory in `papers/address-morphism-theory-full-paper-en-v3.md`.
- **Developer:** run `npm run verify:model` to see the executable abstention
  model, then inspect `verification/address-morphism-executable-expectations.md`.
- **Standards / public-sector reader:** read the scope and non-goals in the
  formal core, then `verification/repository-content-gap-audit.md` for the
  trust and artifact roadmap.
- **Reviewer:** read `verification/main5-formal-additions.md` to see which
  manuscript ideas were promoted into definitions, theorems, and tests.
- **Risk reviewer:** run `npm run verify:s-priority-decomposition` and read
  `verification/s-priority-decomposition-verification.md` to see how the top
  unverified claims are split by region, use case, source, and failure mode.

## Repository Layout

- `papers/` - active English and Japanese manuscripts.
- `notes/` - chapter drafts, outlines, and research resumes.
- `verification/` - claim maps, expectation tests, audits, and verification boundaries.
- `scripts/` - local manuscript assembly and PDF generation tools.
- `output/pdf/` - generated PDFs and HTML exports. This directory is ignored by Git.

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
