# Address Morphism Theory LaTeX notation normalization

Date: 2026-06-27

## Purpose

This note records the normalization of AMT mathematical notation into
LaTeX-first manuscript notation. Code-style names are still allowed in
implementation appendices, but the theory paper should use typed sets,
morphisms, direct sums, and predicate notation.

## Updated manuscript sections

- `papers/address-morphism-theory-full-paper-en-v3.md`
  - `Appendix A. Core Notation`
  - `Appendix K. Mathematical Inventory / Core Notation`
- `papers/address-morphism-theory-ja-v1-master.md`
  - `付録A 中核記法`

## Canonical notation

The canonical AMT spaces are:

\[
t\in\mathbb{T},\quad
\chi\in\mathcal{X},\quad
W_t,\quad
X_t,\quad
S_t,\quad
Y_t,\quad
N_t,\quad
T_t,\quad
\mathcal{E}_t^{+},\quad
\mathcal{Q}_t,\quad
\mathcal{V}_t,\quad
\mathcal{R}_{\chi,t},\quad
\mathcal{H}_t.
\]

The canonical morphism chain is:

\[
\begin{aligned}
O_t &: X_t \to Y_t,\\
N_t &: Y_t \to N_t(Y_t),\\
\pi_t &: S_t \to T_t,\\
\varepsilon_t &: T_t \to \mathcal{E}_t^{+},\\
\Gamma_t &: \mathcal{E}_t^{+} \to \mathcal{P}_{\mathrm{fin}}(X_t),\\
\Delta_{\chi,t} &: \mathcal{P}_{\mathrm{fin}}(X_t) \to \mathcal{Q}_t,\\
\operatorname{Eval}_{\chi,t} &: \mathcal{Q}_t\times\mathcal{V}_t \to \mathcal{R}_{\chi,t},\\
G_t &: \mathcal{R}_{\chi,t}\times\mathcal{V}_t
  \to \mathrm{PID}_t\sqcup\mathrm{NonIssue},\\
\operatorname{Update}_t &: \mathcal{H}_t\times\mathcal{R}_{\chi,t}
  \to \mathcal{H}_{t+1}.
\end{aligned}
\]

The canonical outcome type is:

\[
\mathcal{R}_{\chi,t}
=
\operatorname{Resolved}(\mathcal{Q}_t)
\sqcup
\operatorname{Ambiguous}(\mathcal{P}_{\mathrm{fin}}(\mathcal{Q}_t))
\sqcup
\operatorname{Unresolved}(\mathrm{Reason})
\sqcup
\operatorname{Rejected}(\mathrm{Reason})
\sqcup
\operatorname{Conditional}(\mathcal{Q}_t,\mathrm{Condition}).
\]

## Editorial rule

Use LaTeX notation for the mathematical paper. Use code names only when:

- referring to an implementation API, module, command, or test;
- giving a Lean or TypeScript mapping;
- documenting a reproducible command.

Avoid mixing \(E_t\) as both an entity space and an evaluation score. The
normalized notation uses \(X_t\) for entities, \(\operatorname{Eval}_{\chi,t}\)
for evaluation, and \(\mathcal{E}_t^{+}\) for expansion.

