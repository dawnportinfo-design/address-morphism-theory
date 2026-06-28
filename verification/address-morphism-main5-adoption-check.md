# Address Morphism Theory adoption check for `main (5).pdf`

Date: 2026-06-27

Source reviewed: `C:/Users/kitau/Downloads/main (5).pdf`

## Verdict

The current AMT repository already covers many items that should be retained:
unresolved safety, lineage, context relativity, natural geography, vertical
reference, source governance, security boundaries, LaTeX notation, and
commutative diagrams.

The source PDF still has several strong elements that are worth adopting into
the current AMT paper, especially where they strengthen the mathematical core
instead of expanding product or protocol detail.

## Highest-priority additions to AMT core

| Priority | Addition | Why it should be added | Safe placement |
| --- | --- | --- | --- |
| S | Related-work chapter/table | The PDF has a clear comparison against normalization, geocoding, place IDs, entity resolution, geographic ontology, and DID. This makes AMT more academically legible. | Early chapter after introduction, or appendix promoted into body. |
| S | Bayesian sequential estimation model | The PDF's probability chapter gives AMT a stronger uncertainty model. Current paper has evidence and quality, but sequential belief update deserves a named section. | After evidence/evaluation or before decision theory. |
| S | Bayesian decision theory / loss model | AMT should state that resolution is a decision under context, risk, and loss, not just a score. This supports unresolved as a rational action. | Context-relative optimality or evidence chapter. |
| S | Existence, uniqueness, and stability theorem under conditions | The PDF's Chapter 13 gives a strong theorem framing. It should be included only with explicit assumptions: finite candidates, separation margin, source validity, context, and gate satisfaction. | Formal semantics or theorem appendix. |
| A | Structural dissimilarity is not a metric, with counterexample | This prevents reviewers from attacking \(D_{\chi,t}\) for failing symmetry or triangle inequality. | Structural dissimilarity section and appendix. |
| A | Learnable threshold \(\delta\) and calibration policy | The PDF treats \(\delta\) as theoretically meaningful and learnable. Current paper can add calibration without claiming universal optimality. | Clustering section or benchmark protocol. |
| A | Natural geography manifold / GNAM bridge | The PDF's natural geography model is more ambitious. Adopt a weakened version: natural geography as typed geometry, topology, access, and temporal-change layer. | Natural geography validation model. |
| A | Vertical reference layer as a typed model | Current paper has vertical reference, but the PDF's decomposition into vertical entity, vertical attributes, access equivalence, privacy separation, and vertical uncertainty is valuable. | Vertical reference section. |
| A | Delivery as the strictest validation test, not the whole theory | This phrase is useful: AMT is not a delivery theory, but delivery is one of the hardest empirical tests of address reference. | Introduction or verification strategy. |

## Add only with weakened wording

| Source idea | Risk | Safer wording |
| --- | --- | --- |
| "Address reference can be computed deterministically" | Too strong globally. | "Address reference can be conditionally resolved under declared candidates, context, evidence, and gates." |
| Convergence theorem | Real-world source drift can break convergence. | "Under stationary source assumptions and stable evidence updates, cluster belief may converge." |
| Natural geography manifold | May sound over-formal if not empirically backed. | "A useful model for natural referents is a typed geometric/topological layer." |
| Vertical determinability | Building interiors and access rules are often private or missing. | "Vertical reference is decidable only under sufficient vertical evidence." |
| PID temporal consistency | Semantic mis-resolution can still occur. | "PID bit stability is separate from semantic correctness." |

## Keep outside AMT core

| Item | Destination |
| --- | --- |
| AGID/AOID wire format, QR, API, SDK conformance | AGID/AOID protocol paper |
| ZK circuit, nullifier, revocation, freshness, proof bundle details | Zero-Knowledge Address Predicates paper |
| Product UX, app flows, POS, hotel, drone, locker workflows | AGID product/protocol docs |
| Full country-by-country source registry | Data/source registry or country-pack docs |
| Claims of global postal/API coverage | Empirical validation appendix only |

## Recommended next patch sequence

1. Add a concise "Related Work and Distinctions" section to the English and
   Japanese AMT papers.
2. Add a "Probabilistic Evidence Update and Decision Loss" section with clear
   non-claims.
3. Add a theorem: "Conditional Existence, Uniqueness, and Stability" with
   explicit assumptions.
4. Add the non-metric counterexample for structural dissimilarity.
5. Strengthen vertical reference and natural geography only as typed models,
   not as claims of complete data coverage.

## Final judgment

The most valuable material to import from `main (5).pdf` is not more product
detail. It is the mathematical framing: related-work contrast, Bayesian update,
decision theory, conditional stability, non-metric dissimilarity, natural
geography typing, and vertical reference typing. Those will make AMT look more
like a real research theory while keeping AGID/AOID and ZK as companion layers.

