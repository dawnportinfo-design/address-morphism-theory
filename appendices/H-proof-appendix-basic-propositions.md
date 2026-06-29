# Appendix H. Proof Appendix: Basic Propositions

## Proposition: Normalization Does Not Imply Referent Equality

If two expressions normalize to the same string but arise under different
contexts or candidate sets, equality of normalized form is insufficient to prove
referent equality.

Proof sketch: normalization maps expressions to surface form, while referent
resolution maps through candidate and evidence states. The former omits
contextual evidence required by the latter.

## Proposition: Candidate Insufficiency Requires Abstention

If candidate generation is not sufficient for the requested purpose, safe PID
issuance is blocked.

Proof sketch: issuing a PID asserts a stable referent. Without candidate
sufficiency, the resolver cannot exclude missing true referents.
