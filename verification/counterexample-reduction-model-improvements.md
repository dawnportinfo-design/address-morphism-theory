# Counterexample Reduction Model Improvements for AMT

Date: 2026-06-27

## Purpose

This memo checks whether Address Morphism Theory can be improved so that
counterexamples become rarer, narrower, and safer.

The answer is yes, but with an important boundary:

> AMT should not try to eliminate all counterexamples by claiming perfect
> resolution. It should reduce counterexamples by strengthening assumptions,
> splitting contexts, preserving uncertainty, and refusing unsafe output.

The best mathematical strategy is not "always resolve." The best strategy is:

\[
\text{resolve when conditions hold; otherwise emit a safe non-answer.}
\]

## Main counterexample families

| Counterexample family | Why it breaks naive models | Safer model improvement |
| --- | --- | --- |
| Same name, different place | Surface string is non-injective | Add structural and source gates. |
| Same place, many names | Literal strings are unstable | Use referent equivalence classes. |
| Translation collision | Romanization or translation merges names | Add language/script collision risk. |
| Administrative change | Old and new boundaries coexist | Add temporal validity intervals. |
| Postal code ambiguity | Postal code is area compression | Keep postal code as evidence, not identity. |
| Building/room ambiguity | 2D geometry cannot distinguish vertical entities | Add vertical reference layer. |
| Natural feature access | Mountain/lake/island exists but handoff point differs | Separate referent, display point, access point, handoff point. |
| Private/hidden address | Evidence exists but cannot be public | Add scoped disclosure and private predicates. |
| Weak source country | Data source incomplete | Add country/source quality class. |
| Disputed territory | Multiple authorities claim the same referent | Add viewpoint policy and claim layers. |

## Model improvement 1: conditional theorem instead of universal theorem

Replace unconditional uniqueness claims with conditional uniqueness:

\[
\exists!q\in C_t(s)
\quad\text{if}\quad
\Delta(q,q')>\delta_{\chi,t}
\quad\forall q'\neq q
\]

and required evidence gates pass:

\[
G_{\chi,t}(s,q)=1.
\]

Then the resolver may emit \(q\). Otherwise:

\[
G_{\chi,t}(s,q)=0
\Rightarrow
\mathrm{unresolved}
\]

or:

\[
\exists q_1\neq q_2:
\Delta(q_1,q_2)\le\delta_{\chi,t}
\Rightarrow
\mathrm{ambiguous}.
\]

This does not remove every hard case, but it removes false certainty.

## Model improvement 2: typed equivalence relations

Do not use one equality relation for all address identity. Define typed
equivalence:

\[
\sim_{\mathrm{geo}},\quad
\sim_{\mathrm{postal}},\quad
\sim_{\mathrm{admin}},\quad
\sim_{\mathrm{delivery}},\quad
\sim_{\mathrm{legal}},\quad
\sim_{\mathrm{display}},\quad
\sim_{\mathrm{proof}}.
\]

Many counterexamples disappear once the theory stops asking one relation to do
every job.

Example:

- two expressions may be display-equivalent but not delivery-equivalent;
- two entrances may be building-equivalent but not handoff-equivalent;
- an old address may be lineage-equivalent but not current-postal-equivalent.

## Model improvement 3: context-indexed resolver

Use a context-indexed resolver:

\[
R_{\chi,t}:S_t\to
\mathcal{P}(Q_t)\times \mathsf{Status}\times \mathsf{Evidence}.
\]

The same input can validly produce different outputs for:

- postal delivery;
- emergency response;
- legal registration;
- navigation;
- natural feature search;
- private proof;
- international shipping.

This reduces counterexamples caused by mixing purposes.

## Model improvement 4: evidence vector instead of scalar confidence

Scalar confidence hides why a result is weak. Use evidence vector:

\[
E(q)=
(e_{\mathrm{postal}},
e_{\mathrm{admin}},
e_{\mathrm{geo}},
e_{\mathrm{language}},
e_{\mathrm{source}},
e_{\mathrm{delivery}},
e_{\mathrm{freshness}},
e_{\mathrm{privacy}})
\]

Then gates can be context-specific:

\[
G_{\mathrm{delivery}}(E)=1
\]

may require postal and delivery evidence, while:

\[
G_{\mathrm{naturalSearch}}(E)=1
\]

may require geographic and multilingual evidence.

## Model improvement 5: source quality class

Attach source class to every candidate:

\[
\operatorname{src}(q)\in
\{\mathrm{official},\mathrm{postal},\mathrm{carrier},
\mathrm{openData},\mathrm{community},\mathrm{derived},\mathrm{manual}\}.
\]

Attach country or region data maturity:

\[
M(r)\in\{A,B,C,D\}
\]

where:

- A: strong official/postal data;
- B: postal code exists but weak API/data;
- C: no postal code but strong geo OSS;
- D: weak postal and weak geo OSS.

This prevents low-data regions from being judged by the same assumptions as
high-data regions.

## Model improvement 6: collision budget

For translation, romanization, and alias expansion, define collision risk:

\[
\operatorname{Collide}(\tau,s)
=
|\{q\in Q_t:\tau(q)=\tau(s)\}|.
\]

If:

\[
\operatorname{Collide}(\tau,s)>1
\]

then the translation is search-only or manual-required unless structural
evidence separates the candidates.

This directly reduces counterexamples from pinyin, romanization, dialect,
Wade-Giles, Hepburn, Arabic romanization, and multilingual aliases.

## Model improvement 7: access-point factorization

For physical places, split:

\[
q=(q_{\mathrm{referent}},
q_{\mathrm{label}},
q_{\mathrm{access}},
q_{\mathrm{handoff}},
q_{\mathrm{route}})
\]

This reduces false delivery claims for:

- islands;
- mountains;
- rivers;
- ports;
- airports;
- large buildings;
- gated facilities;
- ski resorts;
- golf courses;
- disaster shelters.

The named place and delivery point do not have to be the same object.

## Model improvement 8: temporal versioning

Make all core maps time-indexed:

\[
\rho_t,\epsilon_t,C_t,D_t,G_t,P_t.
\]

Every emitted result should carry:

\[
(\mathsf{validFrom},\mathsf{validTo},\mathsf{sourceVersion}).
\]

This reduces counterexamples from:

- old addresses;
- city mergers;
- renamed streets;
- postal code changes;
- new buildings;
- disaster relocation.

## Model improvement 9: non-answer as first-class output

Define status:

\[
\mathsf{Status}\in
\{\mathrm{resolved},\mathrm{partial},\mathrm{ambiguous},
\mathrm{unresolved},\mathrm{manualRequired},\mathrm{rejected}\}.
\]

The theory is stronger if it treats these as successful safe outcomes, not
failures.

Many counterexamples only refute a theory that always answers. They do not
refute a theory that is allowed to say:

> The available evidence is insufficient for this context.

## Model improvement 10: proof obligations for emitted identifiers

Every emitted PID/AGID/AOID-derived output should carry proof obligations:

\[
\mathcal{O}=
\{O_{\mathrm{candidate}},
O_{\mathrm{separation}},
O_{\mathrm{source}},
O_{\mathrm{freshness}},
O_{\mathrm{context}},
O_{\mathrm{privacy}}\}.
\]

If any obligation fails, the system can still show candidates, but should not
emit a final identifier or delivery-ready rendering.

## Recommended theorem shape

The strongest safe theorem is:

> Conditional Sound Emission Theorem:
> Given a finite candidate set, declared source versions, a context-indexed
> dissimilarity, a separation margin, and passing evidence gates, the resolver
> may emit a resolved referent. If those conditions do not hold, the resolver
> must emit a non-resolved status.

Symbolically:

\[
\left[
\begin{array}{c}
C_t(s)\ \mathrm{finite}\\
\exists q^\star\in C_t(s)\\
\forall q\neq q^\star,\ D_{\chi,t}(q^\star,q)>\delta_{\chi,t}\\
G_{\chi,t}(s,q^\star)=1
\end{array}
\right]
\Rightarrow
R_{\chi,t}(s)=\mathrm{resolved}(q^\star).
\]

Otherwise:

\[
\neg G_{\chi,t}
\lor
\neg \mathrm{Separated}
\lor
\operatorname{SourceGap}
\Rightarrow
R_{\chi,t}(s)\in
\{\mathrm{partial},\mathrm{ambiguous},\mathrm{unresolved},\mathrm{manualRequired}\}.
\]

This theorem reduces counterexamples because it makes the assumptions explicit
and converts unsafe cases into expected non-answer states.

## What cannot be eliminated

Some counterexamples are unavoidable:

- missing official data;
- wrong official data;
- new construction before data update;
- fraudulent user input;
- political disputes;
- private building interior data;
- carrier-specific access restrictions;
- legal/customs constraints;
- disaster-time changes.

AMT should not promise to solve these unconditionally. It should promise to
detect uncertainty, preserve evidence, and avoid false precision.

## Final recommendation

To reduce counterexamples, improve AMT with:

1. conditional theorems;
2. typed equivalence relations;
3. context-indexed resolvers;
4. evidence vectors;
5. source maturity classes;
6. collision budgets;
7. access-point factorization;
8. temporal versioning;
9. first-class non-answer states;
10. proof obligations for emitted identifiers.

This makes AMT harder to refute because it no longer claims perfect address
resolution. It claims safe, context-aware, evidence-gated resolution.

