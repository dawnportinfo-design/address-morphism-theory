# S-Priority Decomposition Verification

Date: 2026-06-29

This note decomposes the highest-risk unverified Address Morphism Theory claims
by region, use case, data source, and failure behavior.

The goal is not to claim global empirical completion. The goal is to make every
unverified claim falsifiable, benchmarkable, and safe to fail. If a target is not
inside the candidate set, if a data source cannot be trusted, or if an external
audit has not happened, the system must abstain rather than issue a precise
verified identifier.

Machine-readable gate:

```bash
npm run verify:s-priority-decomposition
```

## Decomposition Matrix

| S item | Region slices | Use-case slices | Source slices | Required failure behavior |
| --- | --- | --- | --- | --- |
| Candidate generation completeness | Postal, weak-postal, no-postcode, island, disputed/cross-border | Delivery, checkout, field handoff, hotel/POS | Official/admin, open geo, redacted feedback | Missing candidate returns `unresolved` |
| Multilingual recall | Multi-script, transliteration, old names, cross-border naming | Search, delivery, checkout, translation | Alias packs, gazetteers, query fixtures | False merge returns `candidate-only` |
| Natural/cultural coverage | Islands, deserts, mountains, polar, heritage | Non-postal reference, marine, humanitarian, research | Open geo, gazetteers, field reports | Missing or unstable source returns `unresolved` |
| Strict GIS validation | City, island, mountain/desert, ocean/polar | Postal zones, delivery zones, grid, boundary policy | Geometry packs, admin boundaries, license registry | Hard errors block verified issuance |
| Commercial API comparison | Strong postal, weak postal, no-postcode, island/cross-border | Validation, KYC, shipping, checkout | Rights-cleared benchmark, provider APIs, aggregate metrics | No terms approval means no live benchmark |
| ZK circuit safety | Small anonymity set, dense formal, cross-border, single-building risk | Region proof, eligibility proof, freshness, rate limit | Toy commitments, circuit implementation, crypto audit | No audited circuit means `ZK-ready` only |
| AGID/AOID production security | All regions, offline, connector-heavy, privacy-risk | Registration, QR, POS, hotel, field handoff | Local gates, redacted audit logs, external audit | Private material risk blocks release |

## Safe Claim Boundary

AMT can currently claim a conservative model:

- partial morphisms, abstention, ambiguous states, and unresolved states are
  first-class outputs;
- candidate generation is source-bound;
- multilingual expansion is a recall layer, not an identity proof;
- natural and cultural places require declared source coverage;
- commercial comparisons require explicit terms and network approval;
- ZK is proof-ready until circuits and audits exist;
- AGID/AOID production security belongs to implementation and external review.

## Forbidden Claims

The theory repository must not claim:

- every global addressable object is always found;
- translation proves address identity;
- all natural and cultural names are recognized worldwide;
- strict global GIS validation is complete;
- AMT beats all commercial address APIs;
- complete zero-knowledge address proofs are finished;
- AGID/AOID are production secure because AMT is defined.

## How To Use This In The Paper

Use the decomposition as the bridge between theorem statements and empirical
work. A theorem can say what follows when the candidate set, context, and gates
are valid. The decomposition says how to test whether those preconditions are
credible for a region, use case, and data source.

This makes the paper stronger because it turns the most dangerous overclaims
into explicit experimental programs.
