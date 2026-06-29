# 11. Safe Resolution And PID Issuance

A persistent identifier should be issued only when the resolver can justify the
referent, scope, confidence, source lineage, privacy boundary, and successor
policy.

PID issuance is blocked for unresolved, ambiguous, source-incomplete, or
privacy-unsafe states. Application identifiers may be derived later, but they
must not replace the core referent record.

Model hook: `formal/morphism-chain.ts`, `formal/unresolvability.ts`.
