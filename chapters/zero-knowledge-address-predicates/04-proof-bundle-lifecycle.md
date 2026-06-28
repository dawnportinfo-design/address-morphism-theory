# Proof Bundle Lifecycle

A proof bundle should have a versioned lifecycle:

```text
draft -> locally verified -> externally reviewed -> audited -> deprecated
```

Bundle metadata should include:

- bundle id
- predicate family
- circuit profile or non-circuit profile
- public signal schema
- verifier policy
- supported failure states
- audit status
- deprecation and successor fields

This avoids treating toy envelopes, TypeScript compatibility tests, and audited
circuits as the same artifact.

## Executable Model

- Model: [04-proof-bundle-lifecycle.model.py](models/04-proof-bundle-lifecycle.model.py)
- Fixture: [04-proof-bundle-lifecycle.model-tests.json](models/04-proof-bundle-lifecycle.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
