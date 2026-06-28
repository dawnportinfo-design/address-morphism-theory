# Zero-Knowledge Address Predicates Table of Contents

Predicate theory for proving address properties without exposing address text, recipients, or precise private location material.

## Chapters

1. [Privacy Goals and Non-Goals](01-privacy-goals-and-non-goals.md)
   - Defines what can be safely proven and what a ZK-ready model does not solve.
   - Model: [01-privacy-goals-and-non-goals.model.py](models/01-privacy-goals-and-non-goals.model.py)
   - Fixtures: [01-privacy-goals-and-non-goals.model-tests.json](models/01-privacy-goals-and-non-goals.model-tests.json)
2. [Commitments, Nullifiers, and Public Signals](02-commitments-nullifiers-and-public-signals.md)
   - Separates commitments, nullifiers, public signals, roots, scopes, and verifier policy.
   - Model: [02-commitments-nullifiers-and-public-signals.model.py](models/02-commitments-nullifiers-and-public-signals.model.py)
   - Fixtures: [02-commitments-nullifiers-and-public-signals.model-tests.json](models/02-commitments-nullifiers-and-public-signals.model-tests.json)
3. [Predicate Taxonomy](03-predicate-taxonomy.md)
   - Defines region, quality, freshness, consent, revocation, and rate-limit predicates.
   - Model: [03-predicate-taxonomy.model.py](models/03-predicate-taxonomy.model.py)
   - Fixtures: [03-predicate-taxonomy.model-tests.json](models/03-predicate-taxonomy.model-tests.json)
4. [Proof Bundle Lifecycle](04-proof-bundle-lifecycle.md)
   - Models proof issuance, use, replay prevention, expiry, revocation, and audit boundaries.
   - Model: [04-proof-bundle-lifecycle.model.py](models/04-proof-bundle-lifecycle.model.py)
   - Fixtures: [04-proof-bundle-lifecycle.model-tests.json](models/04-proof-bundle-lifecycle.model-tests.json)
5. [Applications and Safety Boundaries](05-applications-and-safety-boundaries.md)
   - Connects proof-only sharing to wallet, QR, POS, hotel, field, locker, and drone workflows.
   - Model: [05-applications-and-safety-boundaries.model.py](models/05-applications-and-safety-boundaries.model.py)
   - Fixtures: [05-applications-and-safety-boundaries.model-tests.json](models/05-applications-and-safety-boundaries.model-tests.json)

## Source Paper

- `papers/address-morphism-theory-ii-zero-knowledge-address-predicates.md`
