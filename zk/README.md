# Zero-Knowledge Address Materials

This directory is the canonical reading and maintenance map for zero-knowledge
address materials in Address Morphism Theory.

The repository intentionally keeps older papers in `papers/` for traceability.
This directory answers a different question: which material should a reader use
now, and which material is theory, specification, implementation, application,
or unverified research?

## Reading Order

1. `theory/README.md`
2. `specification/README.md`
3. `implementation/README.md`
4. `applications/README.md`
5. `unverified/README.md`

## Canonical Paper

The canonical ZK paper is:

```text
papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md
```

Other ZK papers are companions, localized versions, or historical drafts. See
`paper-deduplication-map.md`.

## Rules

- Do not publish private witness material.
- Do not publish private keys.
- Do not publish proof internals as release fixtures.
- Public signals must stay small and verifier-oriented.
- Production ZK claims require circuit implementation, review, and audit.
