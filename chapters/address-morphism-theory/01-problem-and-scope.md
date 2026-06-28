# Problem and Scope

Address Morphism Theory begins from a practical failure: address systems often
act as if a written address, a coordinate, a postal-code record, and a delivery
handoff point were the same object. They are not.

The theory treats an address as a context-indexed reference process. A surface
expression may refer to a building, a unit, a delivery entrance, a reception
desk, a locker, a port, a natural feature, or an institutional jurisdiction.
The correct referent depends on purpose, evidence, authority, and acceptable
risk.

## Core Scope

AMT covers:

- surface expressions and multilingual labels
- candidate generation and candidate omission
- evidence gates and unresolved states
- address lineage and administrative change
- purpose-relative resolution
- AGID/AOID-compatible persistent identifiers
- privacy-preserving predicates over address structures

AMT does not claim that every address in the world is already covered by data.
It gives the model for responsible reference and states when a resolver must
abstain.

## Main Safety Principle

A resolver is allowed to emit a precise identifier only when the candidate set,
evidence gate, purpose context, and disclosure policy all support that emission.
Otherwise it must return a non-final state such as `unresolved`, `ambiguous`,
`conditional`, or `rejected`.
