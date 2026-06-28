# Protocol Boundaries and Applications

AMT can support protocols, but the theory itself is not a production protocol.
It defines the reference semantics that protocols can rely on.

Protocol-facing outputs include:

- AGID or AOID identifiers
- alias handles
- redacted receipts
- proof commitments
- candidate-set non-final states
- quality scores
- evidence summaries
- disclosure scopes

## Applications

AMT can inform:

- private address QR
- paperless delivery handoff
- POS delivery acceptance
- hotel and PMS address checks
- locker and PUDO pickup
- drone reachability reports
- postal-zone design
- cross-border address translation
- zero-knowledge address predicates

Each application must define its own threat model, verifier policy, and failure
behavior.

## Executable Model

- Model: [05-protocol-boundaries-and-applications.model.py](models/05-protocol-boundaries-and-applications.model.py)
- Fixture: [05-protocol-boundaries-and-applications.model-tests.json](models/05-protocol-boundaries-and-applications.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
