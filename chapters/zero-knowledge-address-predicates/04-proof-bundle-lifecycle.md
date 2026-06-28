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
