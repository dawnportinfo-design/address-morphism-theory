# Compatibility with ZK Address Predicates

Address Morphism Theory (AMT) is the resolution layer. ZK Address Predicates is
the privacy proof layer. The two repositories are compatible only when this
boundary is kept explicit.

AMT answers:

- what kind of entity may be addressed;
- whether a surface expression has enough evidence to resolve;
- which candidate, cluster, lineage, source set, and quality state support the
  referent;
- whether a persistent identifier may be issued, withheld, replaced, or
  revoked.

ZK Address Predicates answers:

- which predicate can be proved about an AMT-compatible referent;
- which public signals are safe to reveal;
- which verifier policy accepts the proof;
- whether freshness, revocation, consent scope, and nullifier scope are valid.

## Boundary Rule

A ZK proof must not repair an AMT resolution failure. If AMT cannot produce a
safe referent, ZK may only prove conservative non-precise facts or must refuse
the proof request.

```text
surface expression + evidence
  -> AMT resolution state
  -> AMT envelope
  -> ZK predicate request
  -> proof bundle or refusal
```

## AMT Envelope

The minimum cross-repository object is the AMT envelope. It is not a raw address
record. It is a scoped, evidence-bound reference to the result of AMT resolution.

```ts
type AMTEnvelope = {
  schemaVersion: "amt-envelope-v0.1";
  referentCommitment: string;
  pidCommitment: string;
  resolutionState:
    | "verified"
    | "partial"
    | "ambiguous"
    | "unresolved"
    | "rejected"
    | "deprecated"
    | "disputed";
  qualityState: "verified" | "partial" | "manual_required";
  sourceSetVersion: string;
  lineageRoot: string;
  freshnessRoot: string;
  revocationRoot?: string;
  allowedPredicates: string[];
};
```

## Compatibility Matrix

The machine-readable matrix is stored in
`compatibility/amt-zk-compatibility-matrix.json`.

The key rule is monotonic safety: worse AMT states may reduce or block ZK
capability, but must not unlock stronger claims.

## Required Cross-Repo Test Vectors

The required vectors are stored in `compatibility/test-vectors.json`.

- verified referent: region, quality, consent, freshness, and non-revocation
  predicates may be requested.
- partial referent: only limited quality or low-precision membership predicates
  may be requested.
- ambiguous referent: precise region and deliverability predicates are blocked.
- unresolved or rejected referent: no proof bundle is issued.
- deprecated referent: a successor or freshness update is required.
- disputed referent: verifier policy must choose the applicable source policy.

## Non-Claims

This compatibility layer does not claim:

- global candidate generation is complete;
- a ZK circuit has been audited;
- source data is correct merely because a proof verifies;
- address data can be placed on chain safely;
- a proof should reveal raw address text, recipient identity, witness material,
  or precise private coordinates.
