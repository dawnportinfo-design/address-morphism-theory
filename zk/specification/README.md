# Specification

This section owns the public verifier contract for ZK-ready address materials.

## Objects

- `commitmentId`
- `predicateId`
- `policyVersion`
- `revocationRoot`
- `freshnessRoot`
- `nullifier`
- `disclosureScope`
- `result`
- `reasonCode`

## Public Signal Rule

Public signals are verifier-facing metadata. They must not contain address
components, recipient data, precise high-risk coordinates, private keys,
witnesses, or proof internals.

## Proof Bundle Lifecycle

```text
draft -> locally verified -> externally reviewed -> audited -> deprecated
```

## Main Sources

- `chapters/zero-knowledge-address-predicates/02-commitments-nullifiers-and-public-signals.md`
- `chapters/zero-knowledge-address-predicates/04-proof-bundle-lifecycle.md`
- `src/address_morphism/predicate_dsl.py`
