# Implementation

This section tracks executable material. The current repository contains small,
dependency-free reference models, not audited circuits.

## Current Executable Model

- `src/address_morphism/predicate_dsl.py`
- `scripts/verify_predicate_dsl.py`

The model checks:

- required region
- quality threshold
- freshness window
- revocation
- consent scope
- anonymity set lower bound
- scoped nullifier output
- public-signal redaction

## Implementation Status

| Area | Status | Safe Wording |
| --- | --- | --- |
| Predicate model | local executable model | ZK-ready predicate envelope |
| Public signal policy | local verification | public-signal safety model |
| Circuit implementation | not complete here | circuit profile pending |
| Cryptographic audit | not complete here | audit required before production |

## Main Sources

- `src/address_morphism/predicate_dsl.py`
- `scripts/verify_predicate_dsl.py`
- `scripts/verify_publication_safety.py`
