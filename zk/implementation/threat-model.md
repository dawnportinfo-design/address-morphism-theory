# ZK Address Predicate Threat Model

This threat model covers ZK-ready Address Predicate materials that depend on
Address Morphism Theory (AMT). It focuses on privacy, correctness, linkability,
and unsafe production claims. It does not certify any circuit as audited.

## Assets

| Asset | Why it matters | Protection goal |
| --- | --- | --- |
| AMT envelope | Binds proof use to resolved or non-final AMT state | integrity, freshness |
| Referent commitment | Represents the private address referent without exposing it | hiding, binding |
| PID commitment | Allows durable reference without public PID disclosure | hiding, scope control |
| Nullifier | Prevents replay or duplicate use within a scope | unlinkability outside scope |
| Revocation root | Blocks revoked credentials | integrity, freshness |
| Freshness root | Prevents stale proofs | freshness |
| Consent scope | Limits proof use to an allowed purpose | purpose limitation |
| Public signals | Verifier-facing proof metadata | redaction, minimization |
| Witness material | Private circuit inputs | non-disclosure |
| Issuer registry | Defines trusted credential issuers | integrity, governance |

## Trust Boundaries

```text
AMT resolver -> AMT envelope -> proof request -> prover -> verifier -> application
```

The most important boundary is between AMT resolution and ZK proof generation.
If AMT selects the wrong referent, ZK can only prove predicates over that wrong
selection. ZK does not repair resolution quality.

## Adversaries

- malicious verifier trying to extract private address material;
- malicious prover trying to prove a false predicate;
- curious application operator trying to link proofs across contexts;
- compromised issuer publishing stale or false roots;
- network observer correlating proof timing and scope;
- data maintainer accidentally publishing unsafe fixtures;
- implementer overstating `ZK-ready` as audited production ZK.

## Threat Matrix

| Threat | Attack path | Impact | Required control | Readiness |
| --- | --- | --- | --- | --- |
| Public-signal leakage | address-like fields added to verifier metadata | private location exposure | allowlist public signals and deny unsafe keys | `model-ready` |
| Singleton proof set | predicate uniquely identifies referent | de-anonymization | minimum anonymity set and coarsening policy | `model-ready` |
| Cross-scope linkability | same nullifier reused across merchants or apps | tracking | scoped nullifier domain separation | `constraint-ready` |
| Replay | old proof reused after policy window | stale authorization | freshness root, epoch, max-age constraint | `model-ready` |
| Revoked credential accepted | stale revocation root used | unauthorized proof | root freshness and non-membership proof | `model-ready` |
| Bad AMT resolution | wrong referent committed before proof | false eligibility | AMT state guard and source lineage audit | `formal-boundary` |
| Ambiguous state proven as final | unresolved or ambiguous envelope accepted | false precision | reject non-final AMT states | `constraint-ready` |
| Consent confusion | proof for one purpose used for another | policy violation | purpose-bound consent scope | `constraint-ready` |
| Issuer confusion | verifier trusts unknown credential issuer | false credential | issuer trust registry and policy pinning | `model-ready` |
| Side-channel timing | proof request timing reveals sensitive workflow | correlation | batching, coarse epochs, delayed sync | `research-target` |
| Cannot-reach over-precision | field report reveals precise route or location | private movement exposure | coarse zone and time-bucket policy | `research-target` |
| On-chain leakage | address-derived data anchored directly on-chain | permanent privacy loss | root-only anchoring and off-chain proofs | `model-ready` |
| Unsafe fixtures | examples include private material | publication risk | publication safety scan and synthetic fixtures | `model-ready` |
| Unreviewed circuit | prototype treated as secure | cryptographic failure | external audit before production claim | `audit-required` |

## Security Invariants

1. Public signals are allowlisted and minimal.
2. No proof is accepted for `unresolved`, `ambiguous`, `rejected`, or
   `deprecated` AMT states unless the proof is explicitly a review receipt.
3. A predicate with a singleton anonymity set must be rejected or coarsened.
4. Nullifiers must be scoped by verifier policy, purpose, and epoch when
   linkability is not intended.
5. Revocation and freshness roots must be pinned to a policy version.
6. Issuer trust must be explicit; unknown issuers fail closed.
7. On-chain integrations must anchor only roots or registry pointers, never
   address-derived private material.
8. Publication examples must be synthetic or redacted.

## Failure Behavior

| Failure | Safe result |
| --- | --- |
| missing AMT envelope | reject |
| non-final AMT state | reject or review-only |
| malformed public signal | reject |
| stale freshness root | reject |
| unknown issuer | reject |
| anonymity set too small | reject or coarsen |
| circuit audit missing | block production wording |
| root mismatch | reject |
| verifier policy mismatch | reject |

## Open Security Work

- choose concrete proof system and circuit language;
- design non-membership revocation proof;
- define issuer trust registry governance;
- produce circuit test vectors for each predicate family;
- review nullifier linkability across applications;
- define side-channel budget for mobile, POS, field, hotel, locker, and Web3;
- complete independent cryptographic audit before production claims.

## Safe Claim

The safe current claim is:

> AMT defines ZK-ready address predicate relations, public-signal rules, and
> threat boundaries. Production ZK security requires concrete circuits,
> test vectors, implementation review, and external cryptographic audit.
