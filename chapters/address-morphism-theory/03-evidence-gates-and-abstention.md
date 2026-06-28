# Evidence Gates and Abstention

An evidence gate is a predicate over candidate evidence. It determines whether
the resolver is allowed to promote a candidate into a final identifier.

Typical gate dimensions:

- source count and source independence
- source license and provenance
- administrative consistency
- postal or postal-equivalent consistency
- geometry validity
- recency and revocation state
- purpose-specific risk
- privacy policy and disclosure scope

## Abstention Theorem

If two candidates remain indistinguishable under the current observation and
policy, any resolver that emits one precise identifier is adding information not
justified by the evidence. The correct output is `ambiguous`.

This is the operational difference between AMT and ordinary address formatting:
formatting tries to produce a label; AMT tries to avoid false authority.
