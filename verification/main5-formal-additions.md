# Formal Additions From the 142-page Manuscript PDF

This note records the theory items promoted from the locally supplied
`main (5).pdf` manuscript into the short formal core and executable model.

The PDF is TeX-generated and text extraction contains font-encoding artifacts,
so this note uses conservative topic-level extraction rather than long quoted
passages. The goal is to keep publication claims safe while strengthening the
formal spine of Address Morphism Theory.

## Added to the Formal Core

| Manuscript signal | Formal addition | Why it matters |
| --- | --- | --- |
| Conditional resolution and operational constraints | `conditional` outcome | Prevents treating a limited handoff condition as a globally resolved address. |
| Context-dependent use cases such as delivery, emergency, tourism, disaster response, and administration | Context utility and context-optimal candidate set | Makes it explicit that the best referent can differ by operational purpose. |
| Address uncertainty / entropy discussion | Address reference entropy | Gives ambiguity a mathematical quantity without claiming that low entropy proves truth. |
| Evidence, observation history, and failure reports | Evidence update proposition | Separates uncertainty reduction from correctness and avoids overclaiming. |
| Unresolved and rejected cases | Abstention monotonicity theorem | A resolver cannot become more precise without new evidence, policy, or freshness. |
| Privacy and predicate-style disclosure | Predicate anonymity set proposition | Shows why ZK-style proofs must control predicate granularity, not only hide strings. |

## Added to the Executable Model

The local executable model now checks:

- collision creates `ambiguous`;
- missing candidates create `unresolved`;
- gate failure creates `rejected`;
- no-postcode regions can resolve with AGID-first evidence;
- lineage splits require relations;
- context can change the operationally optimal referent;
- disambiguating evidence reduces candidate entropy inside the available set;
- abstention is stable without new evidence;
- private predicates need minimum anonymity sets.

## Safe Claim Boundary

These additions do not prove global coverage, commercial geocoder superiority,
or cryptographic soundness. They make the theoretical contract clearer:

- AMT is a context-indexed reference theory, not a universal perfect geocoder.
- Entropy is a measure of uncertainty, not a certificate of truth.
- `conditional`, `ambiguous`, `unresolved`, and `rejected` are valid outcomes.
- ZK readiness requires separate circuit design and security review.
- Real-world deployment still needs data coverage, governance, threat models,
  and empirical benchmarks.

