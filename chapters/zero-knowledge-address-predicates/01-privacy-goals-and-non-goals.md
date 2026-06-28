# Privacy Goals and Non-Goals

Zero-knowledge address predicates let a holder prove selected address facts
without revealing the raw address.

The goal is not to hide every operational fact. The goal is to disclose the
minimum fact required by the verifier:

- inside a delivery region
- eligible for a jurisdictional rule
- fresh credential exists
- not revoked
- consent scope is valid
- duplicate-use nullifier has not been spent

## Non-Goals

This repository does not claim a complete audited ZK system. It defines a
ZK-ready envelope and predicate taxonomy. Production circuits require separate
implementation review and cryptographic audit.
