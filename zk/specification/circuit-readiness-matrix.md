# ZK Circuit-Readiness Matrix

This matrix classifies each ZK Address Predicate by how close it is to a real
zero-knowledge circuit. It is intentionally conservative. A predicate can be
`model-ready` while still not being an audited circuit.

## Status Vocabulary

| Status | Meaning | Safe public wording |
| --- | --- | --- |
| `model-ready` | The relation is defined and has a local executable model. | ZK-ready relation model |
| `constraint-ready` | Private inputs, public signals, and constraints are specified enough for circuit design. | circuit profile draft |
| `test-vector-ready` | Positive, negative, boundary, and redaction vectors exist. | circuit test-vector draft |
| `prototype-ready` | A circuit prototype exists but is not audited. | prototype circuit, audit required |
| `audit-required` | Cryptographic review is required before production use. | not production ZK |
| `blocked` | The relation depends on unresolved AMT state or unsafe public signals. | proof blocked |

## Required Circuit Profile Fields

Every predicate that leaves the theory layer must define:

- `relationId`
- `amtEnvelopeVersion`
- `privateInputs`
- `publicSignals`
- `constraints`
- `nullifierScope`
- `revocationModel`
- `freshnessModel`
- `anonymitySetPolicy`
- `failureReasons`
- `testVectorClasses`
- `auditStatus`

The public signal rule is strict: public signals may include commitments,
roots, policy IDs, result codes, lower bounds, and coarse classes. They must not
include private address text, private coordinates, private witness material,
private keys, or proof internals.

## Matrix

| Predicate family | Relation | Private inputs | Public signals | Main constraints | Readiness | Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| Region membership | `member(regionTree, committedReferent)` | committed referent path, AMT envelope, region path | `predicateId`, `regionRoot`, `commitmentId`, `result`, `nullifier` | Merkle membership, AMT state guard, policy scope | `constraint-ready` | production region trees and audited circuit |
| Quality threshold | `qualityScore >= threshold` | quality score, quality source path, AMT envelope | `threshold`, `qualityClass`, `commitmentId`, `result` | range proof, source version binding, hard-error exclusion | `constraint-ready` | quality calibration benchmark |
| Freshness | `issuedAt >= now - maxAge` | issued timestamp, freshness path | `freshnessRoot`, `maxAgeDays`, `freshnessClass`, `result` | range proof, root binding, replay window | `model-ready` | clock policy and source freshness roots |
| Not revoked | `commitment notin revocationSet` | non-membership witness, revocation root | `revocationRoot`, `result` | non-membership proof, root freshness | `model-ready` | revocation accumulator choice |
| Consent scope | `scope in consentSet` | consent credential, scope path | `scopeId`, `policyVersion`, `result` | scope membership, purpose binding | `constraint-ready` | issuer trust registry |
| Anonymous rate limit | `nullifier unused in scope` | secret nullifier seed, scope | `nullifier`, `scopeId`, `epoch`, `result` | scoped nullifier derivation, epoch binding | `constraint-ready` | linkability review |
| Duplicate prevention | `sameAddress -> sameNullifier(scope)` | address commitment seed, scope | `nullifier`, `scopeId`, `result` | stable scoped nullifier, no cross-scope link | `model-ready` | collision analysis and privacy review |
| Delivery-zone eligibility | `region && quality && freshness && consent && notRevoked` | composed private proofs and AMT envelope | composed result, roots, policy IDs | proof composition, failure reason minimization | `test-vector-ready` | circuit composition audit |
| Cannot-reach report | `attemptWithin(zone,timeWindow) && noPreciseLeak` | coarse route evidence, time evidence, device attestations | coarse zone, time bucket, result, receipt | coarse membership, freshness, privacy budget | `model-ready` | device trust and telemetry minimization |
| Locker / PUDO claim | `holderAuthorized(lockerPolicy)` | authorization credential, policy path | locker policy ID, result, nullifier | authorization membership, replay prevention | `model-ready` | hardware integration and QR/PIN retention policy |
| Hotel / PMS validation | `country && formatValid && consent && freshness` | credential, country path, format attestation | country class, format class, result | purpose scope, issuer trust, non-disclosure | `model-ready` | PMS connector audit |
| Web3 anchor | `rootKnown && proofOffChain` | off-chain proof bundle, registry state | root, registry ID, result | root anchoring, no address on-chain | `model-ready` | smart-contract audit and chain privacy review |

## AMT State Guard

No circuit should accept an AMT envelope unless the envelope is in an allowed
state for the predicate.

| AMT state | Proof behavior |
| --- | --- |
| `resolved` + `verified` | proof allowed if policy and anonymity set pass |
| `partial` | limited proof only; no precise eligibility claim |
| `manual_required` | proof blocked except review receipt |
| `ambiguous` | proof blocked or coarsened to non-identifying region |
| `unresolved` | proof blocked |
| `rejected` | proof blocked |
| `deprecated` | successor required |
| `disputed` | policy-dependent; must not imply neutral truth |

## Circuit Test Vector Classes

Each predicate family needs at least:

1. valid accepted vector;
2. wrong-region rejection;
3. below-threshold rejection;
4. stale credential rejection;
5. revoked credential rejection;
6. missing consent rejection;
7. singleton anonymity-set rejection;
8. malformed AMT envelope rejection;
9. deprecated or successor-required rejection;
10. public-signal redaction vector.

## Production Claim Boundary

This repository may claim a predicate is `ZK-ready` only when the relation,
private inputs, public signals, failure reasons, and test-vector classes are
defined. It must not claim production cryptographic security until a concrete
circuit, proof system configuration, trusted setup or setup-free choice,
implementation review, and external audit are complete.
