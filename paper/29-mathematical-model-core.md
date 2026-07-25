# 29. Mathematical Model Core

This chapter isolates the mathematical core of Address Morphism Theory (AMT).
It is written as a model layer rather than an application chapter so future
papers and implementations can reuse the same definitions.

## 29.1 Objects

Let:

- \(S\) be a set of surface address expressions;
- \(C\) be a set of candidate referents;
- \(E\) be a set of evidence records;
- \(R\) be a set of resolved referents;
- \(P\) be a set of persistent identifiers;
- \(U\) be a set of purposes.

An AMT instance is a tuple:

\[
\mathcal{A} = (S, C, E, R, P, U, \Gamma, Q, \rho, \pi)
\]

where:

- \(\Gamma: S \times U \to 2^C\) is candidate generation;
- \(Q: C \times E \times U \to [0,1]\) is purpose-relative evidence quality;
- \(\rho: 2^C \times E \times U \rightharpoonup R\) is partial resolution;
- \(\pi: R \times U \rightharpoonup P\) is partial PID issuance.

The arrows are partial because AMT must be able to refuse unsafe resolution.

## 29.2 Axioms

### Axiom 1: Candidate Sufficiency

If \(\rho(\Gamma(s,u), E, u)\) returns \(r\), then \(r\) must be represented by
at least one candidate in \(\Gamma(s,u)\).

### Axiom 2: Purpose Relativity

Resolution is purpose-relative. The same surface expression may be sufficient
for map search but insufficient for delivery or identity.

### Axiom 3: Abstention Safety

If two or more candidates are indistinguishable above the required threshold,
\(\rho\) must abstain or return an ambiguous state rather than emit a precise
PID.

### Axiom 4: Evidence Monotonicity

Adding fresh, licensed, compatible evidence may preserve or improve a
candidate's quality score, but must not silently erase a contradiction.

### Axiom 5: PID Conservation

A PID may be issued only for a resolved referent under a purpose. If the referent
is replaced, deprecated, or split, lineage must preserve the historical relation
between old and new identifiers.

### Axiom 6: Public Projection Safety

Any public projection of AMT output must be a function of the envelope, status,
quality class, source version, and safe commitments. It must not expose private
address content.

## 29.3 Existence Theorem

**Theorem.** For a finite candidate set \(C_s = \Gamma(s,u)\), if there exists a
unique candidate \(c^\*\in C_s\) whose quality score is above threshold and all
other candidates are below threshold, then a safe resolved referent exists.

**Proof sketch.** By uniqueness, the selected candidate is not ambiguous within
the finite candidate set. By threshold satisfaction, it has enough purpose
relative evidence. Therefore \(\rho\) may map the candidate set to the referent
represented by \(c^\*\).

## 29.4 Uniqueness Theorem

**Theorem.** Under a deterministic tie policy that refuses ties, a finite AMT
resolution either returns no referent or returns at most one referent.

**Proof sketch.** If no candidate clears the threshold, resolution abstains. If
exactly one candidate clears the threshold, it returns that candidate's referent.
If multiple candidates clear the threshold, the tie policy refuses. Therefore no
execution returns two referents.

## 29.5 Commutative Diagram: Public Projection

Public projection should commute with proof preparation:

```text
resolved referent -> AMT envelope -> public projection
        |                  |
        v                  v
 proof request  ->  safe public signals
```

The diagram says that public signals must be derivable from the envelope and
policy, not from hidden address material.

## 29.6 Computational Interpretation

For finite candidates, the reference implementation evaluates:

1. candidate generation output;
2. threshold satisfaction;
3. uniqueness;
4. contradiction presence;
5. PID eligibility;
6. safe projection.

The worst-case finite scan is \(O(n + m)\), where \(n\) is the number of
candidates and \(m\) is the number of evidence records attached to those
candidates.

## 29.7 Non-Claim

The finite model does not prove global candidate completeness. It proves that,
given a candidate set and evidence set, the AMT resolver behaves safely with
respect to threshold, uniqueness, contradiction, and public projection rules.
