# 9. Clusters And Address Equivalence Classes

Two address expressions can be equivalent for one purpose and not equivalent
for another. For example, a building-level delivery alias may be equivalent to
a street address for courier routing but not for legal identity verification.

AMT defines context-relative equivalence classes instead of a single global
normal form.

Model hook: `formal/equivalence-classes.ts`, `tests/equivalence-classes.test.ts`.
