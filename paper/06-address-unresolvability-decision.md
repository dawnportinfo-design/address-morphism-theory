# 6. Address Unresolvability Decision

Unresolvability is not failure noise. It is a valid output state.

A resolver must abstain when candidate coverage is insufficient, evidence
conflicts, confidence is below threshold, source licenses are missing, privacy
policy blocks disclosure, or the requested identifier would overclaim.

This chapter defines a decision procedure for `verified`, `ambiguous`,
`unresolved`, `rejected`, and `manual_review` states.

Model hook: `formal/unresolvability.ts`, `tests/unresolvability.test.ts`.
