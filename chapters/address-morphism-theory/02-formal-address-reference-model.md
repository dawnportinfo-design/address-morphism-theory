# Formal Address Reference Model

The formal model separates four things that are often collapsed:

1. the written or spoken surface expression
2. the normalized address structure
3. the candidate referent set
4. the emitted identifier or non-final state

Let `S` be the space of surface expressions, `C` the candidate-set functor over
available evidence, `E` the evidence gate, and `R` the referent space. A resolver
is not a total function `S -> R`. It is a partial, evidence-sensitive morphism:

```text
resolve_p,e : S -> R + NonFinal
```

where `p` is purpose and `e` is an evidence state.

## Non-Finality

`NonFinal` is not an error bucket. It is part of the semantics:

- `unresolved` - no sufficient candidate set exists
- `ambiguous` - multiple candidates remain plausible
- `conditional` - resolution depends on purpose, role, time, or authority
- `rejected` - a gate failed

## Compatibility With AGID

AGID can be an emitted identifier when the morphism is final. When it is not
final, the compatible output is a structured non-final state, not a guessed AGID.
