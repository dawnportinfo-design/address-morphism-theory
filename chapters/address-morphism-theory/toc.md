# Address Morphism Theory Table of Contents

Core theory for context-indexed address reference, evidence gates, abstention, lineage, and reconstruction.

## Chapters

1. [Problem and Scope](01-problem-and-scope.md)
   - Defines the address reference problem, non-goals, and when a resolver must abstain.
   - Model: [01-problem-and-scope.model.py](models/01-problem-and-scope.model.py)
   - Fixtures: [01-problem-and-scope.model-tests.json](models/01-problem-and-scope.model-tests.json)
2. [Formal Address Reference Model](02-formal-address-reference-model.md)
   - Defines typed referents, observations, evidence, partial morphisms, and candidate sets.
   - Model: [02-formal-address-reference-model.model.py](models/02-formal-address-reference-model.model.py)
   - Fixtures: [02-formal-address-reference-model.model-tests.json](models/02-formal-address-reference-model.model-tests.json)
3. [Evidence Gates and Abstention](03-evidence-gates-and-abstention.md)
   - Defines gate predicates, evidence thresholds, rejection, ambiguity, and unresolved states.
   - Model: [03-evidence-gates-and-abstention.model.py](models/03-evidence-gates-and-abstention.model.py)
   - Fixtures: [03-evidence-gates-and-abstention.model-tests.json](models/03-evidence-gates-and-abstention.model-tests.json)
4. [Morphisms, Lineage, and Reconstruction](04-morphisms-lineage-and-reconstruction.md)
   - Defines breadcrumb restoration, address lineage, split/merge relations, and reconstruction safety.
   - Model: [04-morphisms-lineage-and-reconstruction.model.py](models/04-morphisms-lineage-and-reconstruction.model.py)
   - Fixtures: [04-morphisms-lineage-and-reconstruction.model-tests.json](models/04-morphisms-lineage-and-reconstruction.model-tests.json)
5. [Protocol Boundaries and Applications](05-protocol-boundaries-and-applications.md)
   - Separates theory from protocol, SDK, resolver, QR, POS, hotel, and delivery applications.
   - Model: [05-protocol-boundaries-and-applications.model.py](models/05-protocol-boundaries-and-applications.model.py)
   - Fixtures: [05-protocol-boundaries-and-applications.model-tests.json](models/05-protocol-boundaries-and-applications.model-tests.json)
6. [Validation and Open Claims](06-validation-and-open-claims.md)
   - Classifies formal claims, executable claims, empirical targets, and remaining unverified items.
   - Model: [06-validation-and-open-claims.model.py](models/06-validation-and-open-claims.model.py)
   - Fixtures: [06-validation-and-open-claims.model-tests.json](models/06-validation-and-open-claims.model-tests.json)

## Source Paper

- `papers/address-morphism-theory-full-paper-en-v3.md`
