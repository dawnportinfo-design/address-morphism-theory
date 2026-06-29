# ZK Circuit Prototypes

This directory contains audit-target circuit prototypes for AMT-compatible
address predicates.

The circuits are intentionally narrow:

- they do not resolve addresses;
- they do not encode raw address content;
- they do not publish PID values, recipients, precise coordinates, proof
  internals, or keys;
- they prove only scoped predicates over an AMT-compatible envelope.

Current prototype:

- `no-postcode-postal-equivalent.circom` - a Circom profile for proving that a
  no-postcode region has a postal-equivalent delivery zone, verified AMT state,
  consent scope, freshness, revocation safety, and anonymity lower bound.

Status: prototype, not audited, not production-ready.

