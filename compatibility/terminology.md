# Shared Terminology for AMT and ZK Address Predicates

This glossary aligns Address Morphism Theory, ZK Address Predicates, Postal
Code Generation Theory, and Address AI Learning Theory.

| Term | Meaning |
| --- | --- |
| `referent` | The physical, social, virtual, institutional, or natural entity an address expression is trying to denote. |
| `PID` | Persistent identifier issued only when AMT resolution is safe enough for a declared purpose. |
| `commitment` | A binding reference to hidden data used by proof or envelope layers without disclosing the underlying material. |
| `AMT envelope` | The minimal interoperable AMT output consumed by proof, postal, AI, or app layers. |
| `predicate` | A scoped claim such as membership, freshness, quality threshold, consent scope, or non-revocation. |
| `verifier policy` | The rule set that decides which issuers, predicates, purposes, and freshness bounds are accepted. |
| `public signal` | A value visible to a verifier; it must be purpose-scoped and safe. |
| `nullifier` | A domain-separated replay-control value that must not become a global tracking identifier. |
| `receipt` | A proof or transaction outcome record that confirms a workflow step without exposing private address content. |
| `alias` | A human or system-facing substitute label that may point to an address referent or envelope without revealing the full representation. |

## Rule

When terms differ across repositories, `agid-interoperability-contracts` is the
contract source for field names and state names. Papers may explain concepts in
natural language, but schemas and tests decide implementation compatibility.

