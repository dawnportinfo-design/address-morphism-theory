# Theory

This section owns the theory-level claims for zero-knowledge address predicates.

## Canonical Claims

1. An address proof should prove a predicate over an address graph or credential,
   not reveal the address itself.
2. A predicate can still leak identity if the anonymity set is too small.
3. AMT can define what must be proven, but it does not by itself make a
   cryptographic proof system secure.
4. ZK address predicates are useful only when verifier purpose and disclosure
   scope are explicit.

## Core Predicate Families

- region membership
- quality threshold
- freshness and revocation
- consent scope
- duplicate prevention through nullifiers
- delivery reachability
- postal-equivalent membership

## Main Sources

- `chapters/zero-knowledge-address-predicates/01-privacy-goals-and-non-goals.md`
- `chapters/zero-knowledge-address-predicates/03-predicate-taxonomy.md`
- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md`
