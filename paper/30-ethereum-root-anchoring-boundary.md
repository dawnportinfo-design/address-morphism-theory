# 30. Ethereum Root Anchoring Boundary

This chapter defines the Ethereum-facing boundary for Address Morphism Theory
(AMT). The purpose is not to put addresses on Ethereum. The purpose is to let
Ethereum-compatible systems verify public roots, verifier policies, and
revocation or freshness state while all private address material remains
off-chain.

## 30.1 Public-Good Motivation

Address infrastructure needs neutral verifiability without creating a permanent
public registry of where people live, receive goods, or move. AMT can use
Ethereum as a public coordination layer only for commitments, roots, and policy
identifiers.

The Ethereum layer may help with:

- anchoring evidence bundle roots;
- anchoring issuer registry roots;
- anchoring revocation and freshness roots;
- publishing verifier policy identifiers;
- making proof verification policies auditable.

It must not carry raw address content, recipient records, PID values, precise
private coordinates, proof witnesses, or private keys.

## 30.2 Boundary Definition

An Ethereum root anchor is a tuple:

\[
A_{eth} = (v, chain, epoch, r_E, r_I, r_F, r_R, h_S, policy)
\]

where \(r_E\) is an evidence root, \(r_I\) is an issuer registry root,
\(r_F\) is a freshness root, \(r_R\) is a revocation root, \(h_S\) is a schema
hash, and \(policy\) is a verifier policy identifier.

Every component is public metadata or a digest. None is an address, a PID, a
recipient, a coordinate, a witness, or a secret.

## 30.3 Theorem: Root Anchoring Does Not Disclose Address Content

**Theorem.** If an Ethereum anchor is restricted to root-like digests, epoch,
chain ID, schema hash, and policy ID, and if the hash preimage is kept
off-chain, then the anchor does not by itself disclose the underlying address
content.

**Proof sketch.** The anchor contains only digests and public policy metadata.
Recovering address content would require access to the off-chain preimage or an
external side channel. The anchor may reveal that a root exists for a policy and
epoch, but it does not encode the address string or referent directly.

## 30.4 Non-Claim: Anchors Do Not Prove Good Resolution

An Ethereum root can show that a commitment was published under a policy. It
cannot prove that AMT generated a complete candidate set, selected the correct
referent, or used high-quality local source data. Those claims remain in AMT,
source policy, and benchmark evidence.

## 30.5 Verifier Policy

A verifier policy must name:

- proof system;
- circuit or profile identifier;
- allowed predicates;
- freshness window;
- minimum anonymity set;
- explicit refusal to disclose raw address material;
- explicit refusal to disclose precise private coordinates.

The policy is not a circuit audit. It is an auditable declaration of what a
proof verifier is allowed to accept.

## 30.6 Failure Modes

The Ethereum boundary must reject:

- address-shaped fields;
- recipient-shaped fields;
- PID values and PID commitments that could become persistent public trackers;
- latitude, longitude, or precise private coordinates;
- witnesses, proof material, private keys, or secret fields;
- arbitrary memo fields that can smuggle private material.

## 30.7 Model Hook

Model hook:

The executable model is `formal/ethereum-root-anchoring.ts`.

The tests are `tests/ethereum-root-anchoring.test.ts`.

They verify that:

1. a synthetic root-only anchor is accepted;
2. raw-address and witness-shaped fields are rejected;
3. non-root values are rejected;
4. verifier policies require concrete proof systems and privacy-deny defaults;
5. the readiness checklist states the root-only public-good boundary.

## 30.8 Grant-Facing Deliverable

This boundary turns AMT into an Ethereum-compatible public-good package without
requiring an on-chain address registry. A grant-ready implementation can be
scoped as:

1. publish AMT envelope schema and root-anchor schema;
2. publish ZK predicate profile and test vectors;
3. implement verifier policy fixtures;
4. add local proof-circuit prototypes;
5. audit the circuit boundary and no-private-material publication gate;
6. demonstrate a no-postcode-region proof path from AGID region to
   postal-equivalent predicate to verifier policy decision.
