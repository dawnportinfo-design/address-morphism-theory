# ZK Paper Deduplication Map

This map prevents the ZK material from looking like five competing papers.

## Canonical Source

| Role | File | Action |
| --- | --- | --- |
| Canonical English paper | `papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md` | Keep as the main source. |

## Supporting Sources

| Role | File | Action |
| --- | --- | --- |
| Japanese localized paper | `papers/address-morphism-theory-ii-zero-knowledge-address-predicates-ja-v1.md` | Keep aligned with the canonical paper. |
| Companion explainer | `papers/zk-address-predicate-paper-en-v1.md` | Keep as supplemental explanation only. |
| Japanese derived explainer | `papers/zero-knowledge-address-proofs-from-address-morphism-theory-ja.md` | Keep for Japanese readers, but do not treat as canonical. |
| Historical draft | `papers/zk-address-proofs-and-address-morphism-theory-paper-draft.md` | Keep for traceability; do not cite as current. |

## Consolidation Rule

New ZK claims should first land in `zk/` or `chapters/zero-knowledge-address-predicates/`.
They should move into the canonical paper only after:

1. the category is known,
2. the safety wording is checked,
3. the claim is linked to verification or marked unverified,
4. duplicate wording is removed from companion drafts.

## What To Cite

- For theory: cite the canonical paper.
- For specification: cite `zk/specification/README.md`.
- For executable behavior: cite `src/address_morphism/predicate_dsl.py`.
- For product examples: cite `zk/applications/README.md`.
- For limitations: cite `zk/unverified/README.md`.
