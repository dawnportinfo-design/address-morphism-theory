# 5. Formal Preliminaries

AMT uses typed sets for expressions, contexts, candidates, evidence, referents,
states, and persistent identifiers.

The central object is a partial morphism:

```text
f_context,purpose : Expression -> CandidateSet -> EvidenceState -> ReferentState
```

The morphism may return a verified referent, an ambiguous set, an unresolved
state, a rejected state, or a deprecated successor relation.

Model hook: `formal/definitions.ts`.
