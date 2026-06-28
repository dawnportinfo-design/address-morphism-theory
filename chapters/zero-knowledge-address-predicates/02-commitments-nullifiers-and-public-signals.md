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

## Executable Model

- Model: [02-commitments-nullifiers-and-public-signals.model.py](models/02-commitments-nullifiers-and-public-signals.model.py)
- Fixture: [02-commitments-nullifiers-and-public-signals.model-tests.json](models/02-commitments-nullifiers-and-public-signals.model-tests.json)

The model is a local mathematical reference for this chapter's claims. It is not a production resolver, postal engine, or audited cryptographic circuit.
