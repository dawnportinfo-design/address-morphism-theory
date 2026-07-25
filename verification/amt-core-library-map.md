# AMT Core Library Map

This note maps Address Morphism Theory concepts to executable code. It is meant
for reviewers who want to see where the theory stops being prose and becomes a
small runnable model.

## Main Module

`src/address_morphism/core.py` is the shared AMT core library. It is
dependency-free and intentionally small enough to inspect by hand.

## Concept To Code Map

| Theory concept | Code object | Verification |
| --- | --- | --- |
| Surface normalization | `normalize_surface`, `token_set` | `scripts/verify_amt_core_library.py` |
| Content-addressed evidence | `EvidenceArtifact`, `content_digest` | `run_core_checks` |
| Evidence bundle root | `EvidenceBundle.root` | `run_core_checks` |
| Transform accountability | `TransformRecord`, `EvidenceBundle.transform_chain_valid` | chapter 08 model |
| License and publication gate | `EvidenceArtifact.license_state`, `EvidenceBundle.gate` | `run_core_checks` |
| Evidence state | `EvidenceState` | `resolve_candidates` |
| Typed referent | `Referent` | `Candidate`, `Resolution` |
| Candidate ranking | `Candidate`, `rank_candidates` | `run_core_checks` |
| Partial resolver | `resolve_candidates` | `verify:model`, `verify:core-library` |
| Non-final state | `ResolutionState` | `resolve_candidates` |
| Quality state | `QualityState` | `Candidate.quality_state` |
| History graph | `HistoryGraph`, `HistoryEdge` | `run_core_checks` |
| PID issuance boundary | `issue_pid` | `run_core_checks` |
| AMT envelope | `AMTEnvelope`, `build_envelope` | `run_core_checks` |
| ZK proof boundary | `AMTEnvelope.proof_allowed` | `verify:core-library`, `verify:zk-circuit-readiness` |
| Equivalence classes | `equivalence_class` | `run_core_checks` |
| Benchmark readiness | `benchmark_plan_ready` | `run_core_checks` |

## What This Code Claims

The code claims that AMT can be represented as a reproducible local reference
model for:

- evidence-root-bound candidate resolution;
- non-final states instead of false precise identifiers;
- context-relative referent selection;
- content-addressed source bundles;
- history-graph validation;
- PID issuance only after final quality and lineage gates;
- proof eligibility only after the PID boundary;
- benchmark plans that include evidence roots and failure behavior.

## What This Code Does Not Claim

The code does not claim:

- global candidate-generation completeness;
- production address resolution accuracy;
- legal validity of any source license;
- cryptographic security of any ZK circuit;
- superiority over commercial address verification APIs;
- readiness to publish private address fixtures.

## Review Commands

```powershell
npm run verify:core-library
npm run verify:chapters
npm run verify:zk-circuit-readiness
npm run verify:publication-safety
```

`npm run verify` runs these checks as part of the full repository gate.
