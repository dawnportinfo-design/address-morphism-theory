# Postal Code Generation Model Search and Verification

Date: 2026-06-27

## Scope

This memo searches the current Address Morphism Theory repository for proposed
mathematical models related to creating, adopting, validating, and governing
postal-code-like systems. It verifies which models are strong enough to keep,
which need refinement, and which claims should be weakened.

Primary sources searched:

- `verification/universal-postal-code-adoption-theory.md`
- `verification/counterexample-reduction-model-improvements.md`
- AMT full paper and Japanese master paper references to postal code as
  compression, evidence, and partial address expression.
- Existing verification notes about source coverage, postal API availability,
  no-postal-code regions, and country maturity classes.

## High-level verdict

The current proposals are directionally strong. The most important correction is
to describe the project as:

> Postal zone design and governed code adoption.

not:

> Arbitrary postal number generation.

The best model is a multi-objective, source-aware, versioned, country-pack based
postal zone system with official-first behavior and AGID fallback for missing or
weak postal-code regions.

## Found model 1: Postal codes as institutional compression

Proposed model:

\[
P_t:Q_t\to Z_t
\]

where \(Q_t\) is the AMT referent space and \(Z_t\) is the code space.

### Verification

Keep.

This is mathematically sound because postal codes are not addresses. They are
compressed institutional or operational labels over regions, routes, localities,
or delivery zones.

### Required clarification

The map is usually not injective:

\[
q_1\neq q_2 \not\Rightarrow P_t(q_1)\neq P_t(q_2).
\]

Therefore postal code alone must not issue a building-level PID or delivery
endpoint.

## Found model 2: Postal Zone Object

Proposed model:

\[
\mathsf{PZO}=
(\mathsf{code},\mathsf{country},\mathsf{zone},\mathsf{level},
\mathsf{geometryRef},\mathsf{adminRef},\mathsf{deliveryPolicy},
\mathsf{source},\mathsf{version},\mathsf{confidence},\mathsf{status})
\]

### Verification

Keep and promote.

This is the strongest data model because it separates code, geometry,
administrative reference, delivery policy, source, version, confidence, and
status.

### Required additions

Add:

- `namespace`;
- `validFrom`;
- `validTo`;
- `successorCode`;
- `privacyClass`;
- `governanceStatus`;
- `licenseRef`;
- `sourceVersion`.

Recommended extended form:

\[
\mathsf{PZO}^{+}=
(\mathsf{namespace},\mathsf{code},\mathsf{country},\mathsf{zone},
\mathsf{level},\mathsf{geometryRef},\mathsf{adminRef},
\mathsf{deliveryPolicy},\mathsf{source},\mathsf{sourceVersion},
\mathsf{licenseRef},\mathsf{validFrom},\mathsf{validTo},
\mathsf{confidence},\mathsf{privacyClass},\mathsf{status},
\mathsf{successorCode})
\]

## Found model 3: Code assignment as set-valued function

Proposed model:

\[
\Gamma_{\chi,t}:Q_t\to\mathcal{P}(\mathsf{PZO}_t)
\]

### Verification

Keep.

This is stronger than a single-code function because one place may have:

- official postal code;
- carrier route code;
- municipal code;
- island or port code;
- disaster relief zone;
- AGID-generated fallback code.

### Required clarification

The application must define a selection function:

\[
\operatorname{Select}_{\chi,t}(\Gamma(q))\to \mathsf{PZO}\cup\{\mathrm{manualRequired}\}
\]

The selected code depends on context: domestic postal, international shipping,
disaster relief, locker delivery, drone handoff, or administrative reporting.

## Found model 4: Four adoption classes

Proposed classes:

| Class | Meaning |
| --- | --- |
| A | Postal Code Available + Reliable API |
| B | Postal Code Available + Weak API |
| C | No Postal Code + Strong Geo OSS |
| D | No Postal Code + Weak Geo OSS |

### Verification

Keep.

This is operationally important. It prevents countries without reliable postal
APIs from being treated as if they had strong postal validation.

### Required refinement

Split "Reliable API" into:

- reliable official data;
- reliable API availability;
- license/terms allowed;
- freshness;
- coverage.

A country can have official data but no public API, or an API with restrictive
terms. Therefore a better maturity vector is:

\[
M(r)=
(m_{\mathrm{official}},
m_{\mathrm{api}},
m_{\mathrm{license}},
m_{\mathrm{freshness}},
m_{\mathrm{coverage}},
m_{\mathrm{geo}})
\]

and A/B/C/D can be derived from that vector.

## Found model 5: Coverage metric

Proposed model:

\[
\mathrm{Coverage}(R)=
\frac{\mu(\{q\in R:\Gamma(q)\neq\emptyset\})}{\mu(R)}
\]

### Verification

Keep, but make \(\mu\) explicit.

Area-weighted coverage can be misleading in deserts, mountains, forests, ocean
regions, and sparsely inhabited islands. For postal code design, the best
coverage measure is often a vector:

\[
\mathrm{CoverageVector}
=
(c_{\mathrm{population}},
c_{\mathrm{building}},
c_{\mathrm{deliveryDemand}},
c_{\mathrm{roadAccess}},
c_{\mathrm{adminArea}},
c_{\mathrm{landArea}})
\]

### Required guard

Do not optimize only geographic area coverage. That can produce beautiful zones
that do not match delivery demand.

## Found model 6: Balance metric

Proposed model:

\[
\mathrm{Balance}=
\frac{\max_i w(Z_i)}{\min_i w(Z_i)+\epsilon}
\]

### Verification

Keep, but avoid ratio-only optimization.

Ratios are sensitive to very small zones. Use additional dispersion metrics:

\[
\operatorname{CV}(w)=\frac{\sigma(w)}{\mu(w)}
\]

and target ranges:

\[
w_{\min}\le w(Z_i)\le w_{\max}
\]

where \(w\) can be population, delivery volume, route time, building count, or
service workload.

## Found model 7: Access graph contiguity

Proposed model:

\[
G_{\mathrm{access}}=(V,E)
\]

### Verification

Keep and promote.

This is essential. Postal zones should not be built only from Euclidean
geometry. Islands, rivers, mountains, gates, borders, ferries, airports, and
roads define practical adjacency.

### Required addition

Use multi-layer access graphs:

\[
G_{\mathrm{access}}=
G_{\mathrm{road}}\cup
G_{\mathrm{foot}}\cup
G_{\mathrm{ferry}}\cup
G_{\mathrm{air}}\cup
G_{\mathrm{drone}}\cup
G_{\mathrm{restricted}}.
\]

Each delivery mode should select its own graph.

## Found model 8: Stability / change cost

Proposed model:

\[
\mathrm{ChangeCost}(Z_t,Z_{t+1})\le\lambda
\]

### Verification

Keep.

Postal codes should be stable because people, systems, labels, forms, and
historical records depend on them.

### Required addition

Define split/merge costs:

\[
C_{\mathrm{split}},\quad C_{\mathrm{merge}},\quad C_{\mathrm{rename}},
\quad C_{\mathrm{successor}}.
\]

Every code change should produce a successor mapping:

\[
\mathsf{oldCode}\to \{\mathsf{successorCode}_1,\ldots,\mathsf{successorCode}_k\}.
\]

## Found model 9: Namespace uniqueness

Proposed model:

\[
(\mathsf{country},\mathsf{namespace},\mathsf{code},t)\mapsto \mathsf{PZO}
\]

### Verification

Keep.

This is the right way to get global uniqueness without forcing one global code
format. Country and namespace prevent collisions between official, carrier,
municipal, and AGID-generated codes.

### Required addition

Add time interval rather than a single time:

\[
(\mathsf{country},\mathsf{namespace},\mathsf{code},[t_0,t_1))
\mapsto \mathsf{PZO}.
\]

## Found model 10: Deliverability predicate

Proposed model:

\[
P_{\mathrm{deliver}}(q,\mathsf{PZO},\rho,\chi,t)=1
\]

### Verification

Keep and make mandatory.

Postal-code existence is not deliverability. A zone code may exist for a region
where delivery requires pickup, port handoff, carrier review, customs handling,
or manual routing.

### Required output states

Use:

- `deliverable_to_door`;
- `deliverable_to_entrance`;
- `deliverable_to_locker`;
- `deliverable_to_port`;
- `carrier_only`;
- `manual_required`;
- `not_serviceable`.

## Found model 11: Postal Zone Designer optimization

Proposed model:

\[
\min_{\mathcal{Z}}
\alpha C_{\mathrm{route}}
+\beta C_{\mathrm{imbalance}}
+\gamma C_{\mathrm{boundary}}
+\delta C_{\mathrm{change}}
+\eta C_{\mathrm{ambiguity}}
\]

### Verification

Keep, but add constraints and objectives.

### Missing terms

Add:

\[
\zeta C_{\mathrm{privacy}}
+\theta C_{\mathrm{sourceGap}}
+\iota C_{\mathrm{governance}}
+\kappa C_{\mathrm{access}}
+\lambda C_{\mathrm{international}}
\]

Recommended full objective:

\[
\min_{\mathcal{Z}}
\alpha C_{\mathrm{route}}
+\beta C_{\mathrm{imbalance}}
+\gamma C_{\mathrm{boundary}}
+\delta C_{\mathrm{change}}
+\eta C_{\mathrm{ambiguity}}
+\zeta C_{\mathrm{privacy}}
+\theta C_{\mathrm{sourceGap}}
+\iota C_{\mathrm{governance}}
+\kappa C_{\mathrm{access}}
+\lambda C_{\mathrm{international}}
\]

subject to:

- namespace uniqueness;
- official-source compatibility;
- country policy;
- license constraints;
- minimum coverage;
- privacy threshold;
- deliverability gate;
- versioning;
- successor mapping;
- manual review for weak-source areas.

## Found model 12: Privacy/anonymity threshold

Proposed model:

\[
|\{q\in Z_i\}|\ge k_{\min}
\]

### Verification

Keep.

Very small zones can expose households, shelters, clinics, sensitive facilities,
or political targets.

### Required refinement

Use different thresholds by public visibility:

\[
k_{\min}^{public} > k_{\min}^{carrier} > k_{\min}^{private}.
\]

Public postal code zones should be coarser than carrier-only routing zones.

## Found model 13: Stage model for no-postal-code countries

Proposed stages:

1. AGID-only.
2. Provisional route zones.
3. Public country pack.
4. Review and governance.
5. Official or carrier adoption.

### Verification

Keep.

This is realistic and avoids falsely labeling AGID-generated zones as official
postal codes.

### Required addition

Every stage should have exit criteria.

Example:

- Stage 0 -> Stage 1: enough settlement/road/admin data.
- Stage 1 -> Stage 2: zones pass coverage, balance, privacy, and access checks.
- Stage 2 -> Stage 3: country pack has sources, tests, version, and license.
- Stage 3 -> Stage 4: accepted by local authority, carrier, NGO, or governance
  body for a declared use.

## Found model 14: Country pack

Proposed package:

```text
rules.json
zones.geojson or pmtiles
sources.json
tests.json
version.json
```

### Verification

Keep.

This is the right packaging model.

### Required addition

Add:

```text
schema.json
license.json
quality.json
successors.json
privacy.json
sample-fixtures.json
```

Heavy geometry should be distributed as PMTiles, FlatGeobuf, or another
compressed spatial format rather than bundled into the main app.

## Found model 15: Non-answer / manual-required behavior

Found in counterexample reduction model:

\[
\mathsf{Status}\in
\{\mathrm{resolved},\mathrm{partial},\mathrm{ambiguous},
\mathrm{unresolved},\mathrm{manualRequired},\mathrm{rejected}\}
\]

### Verification

Keep and make central.

Postal code generation must be able to refuse:

- weak data;
- privacy risk;
- governance conflict;
- disputed boundary;
- unbalanced zone;
- inaccessible zone;
- code collision;
- license restriction;
- no deliverability evidence.

## Models that need weakening

### "All countries can have postal codes"

Weaken to:

> All regions can have governed address or delivery zone identifiers, but not
> every region should be labeled as having official postal codes.

### "AGID can generate postal codes"

Weaken to:

> AGID can generate provisional postal-zone-like identifiers or fallback
> delivery zones, with status clearly marked as `agid-generated`.

### "Postal code solves address quality"

Weaken to:

> Postal code is one evidence layer. Address quality also requires admin,
> geography, delivery, source, freshness, and component evidence.

## Proposed verification experiments

### Experiment 1: island micro-state

Use a small island or island group. Measure:

- settlement coverage;
- port/ferry/road access;
- population balance;
- public privacy threshold;
- route-zone contiguity.

Best for testing: Antigua and Barbuda, Tuvalu, Kiribati, Maldives, or Samoa.

### Experiment 2: no-postal-code strong geo data

Test a country or territory with weak postal codes but enough OSM/geographic
data. Measure AGID fallback zone quality.

### Experiment 3: mature postal-code country

Use existing official postal codes and verify that the model does not overwrite
them. The output should be classification, validation, and compatibility, not
generation.

### Experiment 4: privacy stress test

Generate small zones and verify the system blocks zones below public anonymity
threshold.

### Experiment 5: split/merge test

Create a population growth scenario and verify stable successor codes after
zone split.

## Recommended final model

The postal-code creation model should be:

\[
\operatorname{PostalForge}(R,\chi,t,\mathcal{D},\mathcal{P})
\to
(\mathcal{Z},\mathcal{C},\mathcal{Q},\mathsf{Status})
\]

where:

- \(R\): target region;
- \(\chi\): use context;
- \(\mathcal{D}\): data sources;
- \(\mathcal{P}\): policy constraints;
- \(\mathcal{Z}\): generated or imported zones;
- \(\mathcal{C}\): namespace-safe codes;
- \(\mathcal{Q}\): quality report;
- \(\mathsf{Status}\): official, derived, agid-generated, manual-required, or
  rejected.

Final decision rule:

\[
\operatorname{EmitCode}(Z_i)=1
\]

only if:

\[
\begin{array}{c}
\operatorname{UniqueNamespace}(Z_i)=1\\
\operatorname{CoverageGate}(Z_i)=1\\
\operatorname{AccessGate}(Z_i)=1\\
\operatorname{BalanceGate}(Z_i)=1\\
\operatorname{PrivacyGate}(Z_i)=1\\
\operatorname{SourceGate}(Z_i)=1\\
\operatorname{DeliverabilityGate}(Z_i)=1\\
\operatorname{VersionGate}(Z_i)=1
\end{array}
\]

Otherwise the result must be `draft`, `manualRequired`, or `rejected`.

## Final judgment

The proposed models are strong enough to become a companion theory, but the
language should be precise:

- "postal code generation" should become "postal zone design";
- official postal systems must not be overwritten;
- AGID-generated codes must be visibly provisional;
- deliverability and postal-code existence must remain separate;
- privacy and governance gates are mandatory.

The best next paper title is:

> Postal Zone Design Theory over Address Morphism Theory

