# 28. AMT Envelope and ZK Predicate Boundary

Address Morphism Theory (AMT) is the referent and resolution layer. ZK Address
Predicates is the privacy proof layer. This chapter defines the boundary between
them so that implementation repositories do not confuse a valid proof with a
valid address resolution.

## 28.1 Boundary Statement

AMT may emit an envelope only after it has decided the current resolution state
of a surface expression, candidate set, source set, lineage, and quality state.
ZK Address Predicates may prove only scoped facts over that envelope.

```text
surface expression + place evidence
  -> AMT candidate generation
  -> AMT resolution state
  -> AMT envelope
  -> proof request
  -> proof bundle or refusal
```

The proof layer must not upgrade the resolution layer. A proof over a weak,
ambiguous, unresolved, deprecated, or disputed envelope inherits those limits.

## 28.2 AMT Envelope

The interoperable AMT envelope is defined by
`agid-interoperability-contracts/schemas/amt-envelope.schema.json`.

The envelope carries commitments, state, quality, source version, lineage,
freshness, revocation root, and allowed predicate names. It intentionally does
not carry private address content, recipient records, proof witnesses, or
precise private coordinates.

## 28.3 State Guard

The following guard is normative for AMT-to-ZK compatibility.

```text
verified      -> predicate may be requested if the envelope allow-list includes it
partial       -> only limited predicates
ambiguous     -> precise predicates blocked or routed to manual review
unresolved    -> no proof bundle
rejected      -> no proof bundle
deprecated    -> successor or freshness update required
disputed      -> verifier policy and source policy decide
manual_review -> no automatic purpose proof
```

## 28.4 Theorem: Proof Validity Does Not Repair Resolution Failure

**Theorem.** Let `E` be an AMT envelope and `P` a ZK predicate proof over `E`.
If the AMT resolution state of `E` is not sufficient for a purpose `u`, then a
valid proof for a narrower predicate does not make `E` sufficient for `u`.

**Proof sketch.** The ZK proof system checks a relation over committed witness
data and public signals. It does not expand the AMT candidate set, improve the
source set, resolve ambiguity, select a successor PID, or settle a disputed
source policy. Therefore proof validity is monotone with respect to the AMT
state: it may preserve or restrict what can be claimed, but it cannot improve
the underlying resolution state.

## 28.5 Corollary: Candidate Completeness Is Outside ZK

If the true referent is absent from the candidate set, a proof over the selected
candidate may still verify. This is not a ZK failure; it is an AMT candidate
generation or source-coverage failure. The repository must state this as a
non-claim.

## 28.6 From PID to Proof Request

A proof request may be generated only from a purpose-scoped envelope:

```text
PID commitment
  + referent commitment
  + quality state
  + lineage root
  + freshness root
  + revocation root
  + allowed predicate list
  -> proof request
```

The proof request must name the verifier policy, predicate, purpose, and request
time. It must not include private address content.

## 28.7 Payment-Like Address Transaction Connection

The address payment rails model gives AMT a transaction vocabulary:

```text
authorize -> capture -> settle -> receipt
```

The ZK boundary supplies a privacy-preserving authorization step:

```text
proof request -> proof bundle -> policy decision -> address-use authorization
```

This permits a merchant, hotel, locker, or field handoff system to accept a
delivery or eligibility claim without seeing the underlying address content.

## 28.8 Shared Contract

The shared schemas, TypeScript types, and cross-layer test vectors are maintained
in `agid-interoperability-contracts`. AMT should treat that repository as the
contract source for envelope field names, state names, predicate names, and
fixture expectations.
