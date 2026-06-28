# Commitments, Nullifiers, and Public Signals

A ZK address proof should separate private witness data from public verifier
signals.

## Private Witness

Private witness material may include address graph node membership, credential
opening data, freshness proofs, revocation membership paths, and holder secrets.
It must not be stored in public fixtures or release artifacts.

## Public Signals

Public signals should be deliberately small:

- predicate id
- policy version
- commitment id
- revocation root
- freshness root
- nullifier
- result class
- disclosure scope

They should not include raw address components, recipients, precise coordinates,
private keys, witness data, or proof internals.

## Nullifier Scope

Nullifiers should be scoped to purpose and verifier class. A delivery nullifier
must not become a universal cross-service tracking identifier.
