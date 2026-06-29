# ZK Audit Readiness

This repository is not claiming an audited ZK system. It is preparing the
materials that an external auditor, grant reviewer, or implementation team
would need before circuit work becomes production-relevant.

## Audit Package Contents

- Circuit prototype: `circuits/no-postcode-postal-equivalent.circom`
- Demo fixture: `demos/no-postcode-private-proof-demo.json`
- Verification script: `scripts/verify_no_postcode_zk_demo.py`
- Threat model: `zk/implementation/threat-model.md`
- Circuit-readiness matrix: `zk/specification/circuit-readiness-matrix.md`
- Ethereum boundary: `paper/30-ethereum-root-anchoring-boundary.md`

## Required External Audit Questions

1. Are membership checks bound to the correct AMT envelope root?
2. Are issuer, freshness, and revocation roots updated and scoped correctly?
3. Are public signals limited to roots, policy identifiers, nullifiers, and
   verifier decisions?
4. Can nullifiers be linked across verifier scopes?
5. Can no-postcode postal-equivalent zones be overclaimed by weak source data?
6. Does the circuit reject unresolved, ambiguous, stale, revoked, or
   low-anonymity subjects?
7. Are test vectors sufficient for accepted and rejected paths?

## Non-Claims

- The current circuit prototype is not audited.
- The prototype does not prove global candidate completeness.
- The prototype does not make a postal-equivalent zone legally official.
- Ethereum anchoring does not put address data on-chain.
- AMT resolution errors remain AMT errors even if a ZK proof verifies.

## Adoption Gate

An open-source user may run the local demo and review the refusal behavior. A
production user must wait for an audited circuit, checked setup ceremony or
transparent proof profile, dependency review, and operational key policy.

