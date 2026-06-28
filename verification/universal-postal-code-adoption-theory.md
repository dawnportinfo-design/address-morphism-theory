# Universal Postal Code Adoption Theory over AMT

Date: 2026-06-27

## Purpose

This memo proposes a theory for making postal-code-like systems adoptable
worldwide without forcing every country, territory, rural region, island,
mountain area, conflict zone, or non-postal area into one rigid format.

The goal is not:

> One global postal code format replaces all national postal systems.

The goal is:

> Every addressable or deliverable region can have a governed delivery-zone
> code, with explicit source quality, hierarchy, versioning, and fallback to
> AGID/AOID when official postal codes are absent or weak.

## Core idea

Postal codes are institutional compression maps:

\[
P_t: Q_t \to Z_t
\]

where \(Q_t\) is the AMT referent space and \(Z_t\) is a code space at time
\(t\).

The code does not need to identify a building. It may identify:

- a delivery zone;
- a postal route;
- a locality;
- a street segment;
- an island;
- a village cluster;
- a locker or pickup area;
- a disaster relief zone;
- an AGID-generated provisional zone.

Therefore the universal theory should separate:

\[
\text{postal code}
\neq
\text{address}
\neq
\text{coordinate}
\neq
\text{delivery endpoint}.
\]

## Four adoption classes

Countries and regions should be classified into four operational classes:

| Class | Meaning | Default behavior |
| --- | --- | --- |
| A | Postal Code Available + Reliable API | Strong validation and auto-fill. |
| B | Postal Code Available + Weak API | Format check, candidates, manual priority. |
| C | No Postal Code + Strong Geo OSS | AGID/geometry/admin verified zone code. |
| D | No Postal Code + Weak Geo OSS | AGID primary identifier and manual review. |

This prevents weak regions from pretending to have the same confidence as
official postal datasets.

## Universal adoption object

Define a Postal Zone Object:

\[
\mathsf{PZO}
=
(\mathsf{code},\mathsf{country},\mathsf{zone},\mathsf{level},
\mathsf{geometryRef},\mathsf{adminRef},\mathsf{deliveryPolicy},
\mathsf{source},\mathsf{version},\mathsf{confidence},\mathsf{status})
\]

The object is versioned and source-aware. It can represent official codes or
AGID-generated provisional codes.

Statuses:

- `official`;
- `open-data-derived`;
- `carrier-derived`;
- `agid-generated`;
- `manual-review`;
- `deprecated`;
- `successor-assigned`.

## Code function

A universal adoption model needs a code assignment function:

\[
\Gamma_{\chi,t}: Q_t \to \mathcal{P}(\mathsf{PZO}_t)
\]

where \(\chi\) is context. The result is a set because a location may have:

- national postal code;
- carrier route code;
- municipal code;
- island/port code;
- emergency/disaster code;
- AGID-generated fallback zone.

The app should choose the best code for the use context, not assume only one
code exists.

## Adoption principle

The universal postal code theory should obey:

1. Official-first: use official postal code where it exists and is reliable.
2. Compatible-not-replacing: do not overwrite national systems.
3. Fallback-by-quality: use AGID zones only where official systems are missing
   or insufficient.
4. Versioned zones: every code must have validity time and successor behavior.
5. Explainable confidence: every code must show source and confidence.
6. Non-deliverability safety: a code must not imply deliverability unless a
   delivery predicate passes.
7. Local script and international rendering: codes and zone labels must render
   in local format and international English format.

## Mathematical requirements

### 1. Coverage

For a target region \(R\), a postal adoption system should maximize:

\[
\mathrm{Coverage}(R)
=
\frac{\mu(\{q\in R:\Gamma(q)\neq \emptyset\})}{\mu(R)}
\]

where \(\mu\) may be population, delivery demand, building count, road access,
or geographic area depending on context.

Population-weighted coverage is often more useful than area-weighted coverage.

### 2. Balance

Postal zones should avoid extreme imbalance:

\[
\mathrm{Balance}
=
\frac{\max_i w(Z_i)}{\min_i w(Z_i)+\epsilon}
\]

where \(w\) may be population, delivery volume, route time, or building count.

Good postal zones are not necessarily equal area. They should be operationally
balanced.

### 3. Contiguity and accessibility

A zone should usually be connected under a relevant access graph:

\[
G_{\mathrm{access}}=(V,E)
\]

not only under Euclidean geometry. Islands, rivers, mountains, borders, and
security barriers make geometric closeness misleading.

### 4. Stability

Codes should not change too often:

\[
\mathrm{ChangeCost}(Z_t,Z_{t+1})\le \lambda
\]

unless administrative reform, population growth, disaster, conflict, or
delivery network changes justify a split or merge.

### 5. Uniqueness within namespace

Each code must be unique within its namespace:

\[
(\mathsf{country},\mathsf{namespace},\mathsf{code},t)
\mapsto
\mathsf{PZO}
\]

Global uniqueness can be achieved by namespacing, not by forcing all countries
to abandon local formats.

Example:

\[
\mathsf{JP}:100\text{-}0001
\quad
\mathsf{BR}:01310\text{-}000
\quad
\mathsf{AGID}:SO:00123
\]

### 6. Deliverability predicate

A postal zone code is valid for delivery only when:

\[
P_{\mathrm{deliver}}(q,\mathsf{PZO},\rho,\chi,t)=1.
\]

Postal existence and delivery possibility must remain separate.

## Code design for countries without postal codes

For countries or territories without reliable postal codes, use a staged model:

### Stage 0: AGID-only

Use AGID/AOID and administrative labels. No invented postal code is shown as
official.

### Stage 1: Provisional route zones

Generate delivery zones from:

- administrative boundaries;
- settlements;
- roads and access paths;
- building clusters;
- ports, airports, ferry routes;
- terrain barriers;
- delivery demand.

### Stage 2: Public country pack

Publish a country pack:

```text
rules.json
zones.geojson or pmtiles
sources.json
tests.json
version.json
```

### Stage 3: Review and governance

Local postal operators, government, NGOs, carriers, and community mappers can
review zones. AGID-generated status remains visible until official adoption.

### Stage 4: Official or carrier adoption

If adopted, a namespace or code series becomes official or carrier-recognized.
Old AGID-generated codes keep `deprecated` and `successorCode`.

## Postal Zone Designer theory

The design problem can be stated as optimization:

\[
\min_{\mathcal{Z}}
\alpha C_{\mathrm{route}}
+\beta C_{\mathrm{imbalance}}
+\gamma C_{\mathrm{boundary}}
+\delta C_{\mathrm{change}}
+\eta C_{\mathrm{ambiguity}}
\]

subject to:

- namespace uniqueness;
- zone coverage;
- source licensing;
- administrative compatibility;
- no excessive privacy leakage;
- deliverability gate;
- local governance approval where required.

This makes postal-code creation a measurable tool, not a random number
generator.

## Privacy constraint

Postal codes can leak location. Very small zones may expose a household,
shelter, clinic, or sensitive facility.

Require a minimum anonymity or aggregation threshold:

\[
|\{q\in Z_i\}|\ge k_{\min}
\]

or use a coarser public zone and keep precise delivery routing inside a
carrier-only view.

## Relationship to AMT

AMT defines the addressable object. Universal Postal Code Adoption Theory
defines a governed compression from addressable objects to delivery zone codes.

\[
\text{AMT referent}
\to
\text{delivery zone}
\to
\text{postal or AGID fallback code}
\to
\text{validated rendering}
\]

Postal codes should be treated as one layer of address evidence, not as the
whole address.

## Recommended companion document

Create a companion paper/spec:

> Universal Postal Zone Adoption over Address Morphism Theory

Suggested chapters:

1. Postal codes as institutional compression.
2. Official postal codes and weak-code regions.
3. AGID fallback zones.
4. Country pack format.
5. Postal Zone Designer optimization.
6. Coverage, balance, contiguity, stability, and privacy metrics.
7. Versioning, deprecation, and successor codes.
8. International rendering and local scripts.
9. Governance and adoption workflow.
10. Conformance tests.

## Final judgment

The strongest universal theory is not "one code format for the world."

The strongest theory is:

\[
\text{official where possible}
\quad+\quad
\text{AGID fallback where needed}
\quad+\quad
\text{quality and source always visible}.
\]

This makes postal-code adoption realistic for countries with mature systems,
weak systems, no postal codes, islands, mountains, rural regions, disaster
zones, and disputed or underserved territories.

