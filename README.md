# Address Morphism Theory

Independent research repository for Address Morphism Theory (AMT).

AMT models address resolution as a chain of evidence-sensitive morphisms from
surface expressions to addressable physical, social, virtual, or institutional
entities. It treats ambiguity, incomplete candidates, lineage, unresolved
states, persistent identifiers, and privacy-preserving predicates as first-class
research objects.

## Repository Layout

- `papers/` - active English and Japanese manuscripts.
- `notes/` - chapter drafts, outlines, and research resumes.
- `verification/` - claim maps, expectation tests, audits, and verification boundaries.
- `scripts/` - local manuscript assembly and PDF generation tools.
- `output/pdf/` - generated PDFs and HTML exports. This directory is ignored by Git.

## Primary Manuscripts

- `papers/address-morphism-theory-full-paper-en-v3.md`
- `papers/address-morphism-theory-ja-v1-master.md`
- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md`
- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates-ja-v1.md`

## Build

```powershell
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
PDF verification writes `output/pdf/address-morphism-theory-pdf-manifest.json`
with page counts, byte sizes, and SHA-256 hashes for generated PDFs.

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
