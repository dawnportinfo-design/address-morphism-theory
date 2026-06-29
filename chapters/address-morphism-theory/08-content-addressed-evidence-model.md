# Content-Addressed Evidence Model

Address Morphism Theory (AMT) needs evidence that can be reviewed, reproduced,
and challenged without trusting mutable file names, web URLs, API responses, or
database row IDs as stable truth. The content-addressed evidence model gives
each evidence artifact an identifier derived from its canonical content and
binds that artifact to source, license, time, transform, and safety metadata.

This chapter defines how AMT evidence should be addressed, bundled, versioned,
and gated before it can influence candidate generation, quality state, PID
issuance, or ZK predicate eligibility.

## Problem

Naive evidence references are brittle:

- a URL can change while its string remains the same;
- a CSV file can be re-exported with silently changed rows;
- a source can be copied without its license or observation time;
- a transformed dataset can lose its parent provenance;
- a resolver can cite a source name without proving which content was used.

AMT treats this as a formal risk. A resolver result is not reviewable unless the
evidence state can be reconstructed or independently challenged.

## Core Objects

Let:

- `B` be canonical byte strings.
- `h: B -> H` be a collision-resistant digest function for the evidence model.
- `A` be evidence artifacts.
- `M` be metadata records.
- `T` be transform records.
- `G` be evidence bundles.

An evidence artifact is:

```text
a = (digest, media_type, byte_length, source_hint, observed_at, license_id, safety_class)
```

The digest is computed over canonical bytes:

```text
digest(a) = h(canonical_bytes(a))
```

The `source_hint` can be a URL, file name, database table, package version, or
institutional citation, but it is not the artifact identity. The digest is the
artifact identity.

## Canonicalization Rule

For text-like sources, canonicalization must define:

1. encoding;
2. line ending normalization;
3. key ordering for JSON-like data;
4. insignificant whitespace policy;
5. numeric formatting policy;
6. redaction policy for non-public fixtures.

For binary sources, canonicalization can be identity bytes, but metadata must
record the media type, size, and source policy.

## Evidence Bundle

An evidence bundle is an ordered-independent set:

```text
G = {a_1, ..., a_n}
root(G) = h(sort(digest(a_i)) concatenated)
```

The root is stable under file order. It changes if any artifact content changes.
The root must be included in AMT envelopes, benchmark reports, and PID issuance
audit records.

## Transform Chain

Derived artifacts must preserve parent links:

```text
derived = transform(parent_digest_set, transform_id, transform_version, params_digest)
```

A derived artifact is valid only if every parent digest is present in the
evidence graph or explicitly marked as externally pinned.

Transform metadata must include:

- `transform_id`
- `transform_version`
- `parent_digests`
- `params_digest`
- `output_digest`
- `lossiness`
- `redaction_class`

Lossy transforms can support search and preview, but they cannot by themselves
support final PID issuance unless a policy explicitly allows that source class.

## Evidence States

AMT evidence states should be content-addressed:

```text
e = (bundle_root, source_policy, gate_version, license_state, freshness_state, safety_state)
```

The same surface expression under two different evidence roots can produce
different candidate sets. This is expected and must be visible:

```text
C_e1(s) != C_e2(s)
```

## Axioms

### Axiom CE1: Content Identity

If two public evidence references have the same canonical bytes, they have the
same digest regardless of file name, URL, or storage location.

### Axiom CE2: Tamper Sensitivity

If canonical bytes differ, the digest must differ except with negligible
collision probability.

### Axiom CE3: Order-Independent Bundling

An evidence bundle root is independent of artifact listing order.

### Axiom CE4: Source Hint Non-Authority

A source hint is not evidence identity. It is only a retrieval or citation hint.

### Axiom CE5: Transform Accountability

A derived artifact is not admissible unless its parent digests and transform
metadata are known.

### Axiom CE6: Safety Gate Before Publication

Artifacts marked as private, unsafe, or unredacted cannot be used as public
fixtures, public examples, public signals, or downloadable packs.

### Axiom CE7: License Gate Before PID Issuance

Evidence whose license state is unknown or incompatible cannot support final
PID issuance in a public registry. It may support private review or local-only
experiments.

### Axiom CE8: Evidence Root Binding

Every PID issuance decision, benchmark result, and ZK-ready AMT envelope must
bind to an evidence bundle root.

## PID Issuance Implications

Before PID issuance, the resolver must verify:

1. all required artifacts have content digests;
2. the evidence bundle root is stable;
3. no artifact in the public path is unsafe or unredacted;
4. license state is compatible with the registry policy;
5. derived artifacts have valid parent links;
6. source freshness is within policy;
7. hard errors from evidence gates are zero.

If these fail, AMT can produce `manual_required`, `blocked`, or
`policy_dependent`, but not a final PID.

## ZK Boundary

ZK proofs should not expose evidence artifacts. They should expose only roots,
policy identifiers, and verifier-safe result codes:

```text
public: evidenceRoot, freshnessRoot, revocationRoot, policyVersion, result
private: committed referent, membership path, evidence paths, issuer material
```

The evidence root lets a verifier know which source set and transform chain the
proof refers to without publishing private address evidence.

## Counterexamples

| Counterexample | Failure if ignored | AMT response |
| --- | --- | --- |
| Same URL, changed body | review cannot reproduce a result | digest changes; source hint is not identity |
| Same data, different file order | false source-set change | sorted bundle root |
| Derived file without parent | unverifiable lineage | reject derived artifact |
| Unknown license | public registry risk | block final PID issuance |
| Unredacted private fixture | privacy leak | block publication and downloads |
| Stale snapshot | obsolete referent selection | freshness gate or successor review |
| API-only evidence | response cannot be audited later | persist digest and response metadata |
| Binary map tile only | insufficient semantic review | require metadata and source policy |

## Verification Map

| Claim | Artifact | Verification type |
| --- | --- | --- |
| same content produces same digest | chapter model | executable-model |
| tampering changes digest | chapter model | executable-model |
| bundle root is order independent | chapter model | executable-model |
| missing transform parent is rejected | chapter model | executable-model |
| unsafe public artifact blocks publication | chapter model | executable-model |
| unknown license blocks PID | chapter model | executable-model |
| evidence root appears in AMT envelope | AMT envelope checks | executable-model |
| collision resistance | digest function assumption | cryptographic assumption |

## Benchmark Method

Benchmarks using evidence must publish:

- evidence bundle root;
- artifact count by source class;
- license state distribution;
- freshness policy;
- redaction policy;
- transform chain depth;
- number of excluded unsafe artifacts;
- number of blocked unknown-license artifacts;
- PID issuance decisions by evidence gate outcome.

The benchmark should report both positive coverage and abstention quality. A
dataset that resolves more addresses by ignoring evidence provenance is not
better; it is less reviewable.

## Executable Model

- Model: [08-content-addressed-evidence-model.model.py](models/08-content-addressed-evidence-model.model.py)
- Fixture: [08-content-addressed-evidence-model.model-tests.json](models/08-content-addressed-evidence-model.model-tests.json)

The model is a local reference for content addressing, bundle roots, transform
accountability, publication safety, and PID evidence gates. It is not a global
source registry or production data pipeline.
