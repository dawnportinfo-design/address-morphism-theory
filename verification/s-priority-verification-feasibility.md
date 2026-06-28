# S-Priority Verification Feasibility

Date: 2026-06-29

## Answer

The S-priority unverified items are not all verifiable in the same sense.

They split into four classes:

| Class | Meaning | Items |
| --- | --- | --- |
| Bounded empirical verification | Verifiable by country, region type, source, and benchmark stratum. Not globally absolute. | candidate generation, multilingual recall, natural/cultural feature coverage |
| Implementation verification | Verifiable for declared data packs and local artifacts. Global strictness needs every pack. | strict GIS validation |
| Controlled external benchmark | Verifiable only with API credentials, terms review, and rights-cleared test data. | commercial API comparison |
| Security research and audit | Locally modelable, but production claims require implementation and external review. | ZK circuit safety, AGID/AOID production security |

The safe rule is:

> AMT can verify bounded claims and failure behavior now. It cannot honestly
> claim worldwide completeness, commercial superiority, complete ZK security, or
> production security from the theory repository alone.

## S Items

| Priority | Item | Can it be verified? | Current safe status | Paper wording |
| --- | --- | --- | --- | --- |
| S | Worldwide candidate generation completeness | Partially. Verify recall by strata; never claim absolute global completeness. | Empirical target | "Candidate-generation sufficiency is regional and source-bound." |
| S | Multilingual search recall improvement | Yes, with paired fixtures and false-merge measurement. | Bounded empirical benchmark | "Multilingual expansion is a recall layer, not identity preservation." |
| S | Natural and cultural feature worldwide coverage | Partially. Verify feature types and sources; do not claim exhaustive recognition. | Source-bound empirical target | "AMT models source-bound natural and cultural referents." |
| S | Strict GIS validation | Yes for named packs. Global strict validation requires every pack to close warnings. | Implementation test | "Hard errors are zero for declared packs; strict global validation remains open." |
| S | Commercial API comparison | Yes only after API terms, credentials, and benchmark rights are cleared. | Controlled benchmark plan | "Compare by evaluation condition; do not claim universal superiority." |
| S | Real ZK circuit safety | Not yet as a complete claim. Verify envelopes now; circuits require implementation and audit. | ZK-ready only | "AMT defines predicates; audited circuits are companion work." |
| S | AGID/AOID production security | Not from AMT alone. Local threat model and gates can be verified; production requires audit. | Protocol security target | "AMT defines semantics; implementation security requires external review." |

## First Experiments

1. Candidate generation: 10-country stratified fixture with urban units, rural
   villages, islands, no-postcode regions, natural features, and renamed places.
2. Multilingual recall: native script, Latin transliteration, English,
   historical names, abbreviations, and dialect variants.
3. Natural/cultural features: islands, ports, lakes, mountains, deserts, caves,
   heritage sites, and seasonal or vague-boundary features.
4. GIS strictness: one small island pack, one dense city pack, one mountain or
   desert pack, and one disputed-region policy pack.
5. Commercial APIs: dry-run adapter design for Loqate, Experian, Melissa, and
   Smarty; no live calls until credentials and terms are approved.
6. ZK: one toy residence-country predicate and one toy delivery-zone predicate.
7. AGID/AOID security: threat model for QR replay, revocation, delegation,
   connector errors, key handling, audit logs, and public/private boundaries.

## Commercial API Boundary

Commercial comparison is feasible but must be handled carefully.

Reference entry points:

- Loqate API documentation: <https://docs.loqate.com/>
- Experian Address Validation: <https://docs.experianaperture.io/address-validation/>
- Melissa Global Address Verification: <https://docs.melissa.com/cloud-api/global-address/>
- Smarty International Street API: <https://www.smarty.com/docs/cloud/international-street-api>

The repo should not store credentials, raw personal address datasets, private
recipient data, or proprietary response bodies. Publish only aggregate metrics
and benchmark methodology unless the provider terms explicitly allow more.

## What This Means For The Paper

AMT should become stronger by being more conservative:

- Treat false precision as a failure.
- Treat `unresolved` as a valid safety output.
- Treat global coverage as a benchmark program.
- Treat multilingual expansion as recall, not identity.
- Treat ZK and AGID/AOID as companion implementation/security work.
- Treat commercial comparisons as condition-by-condition evaluation, not a
  victory claim.

This framing is more credible than claiming that AMT already solves global
addressing.
