# Open-Source ZK Onboarding

This guide shows how a contributor can evaluate the AMT/ZK no-postcode path
without sending production traffic or handling private address material.

## Local Path

```powershell
npm install
npm run verify:zk-demo
npm run test:formal
npm run verify
```

The demo uses synthetic public fixtures only. It does not include raw address,
recipient, private key, proof-secret, or precise coordinate material.

## What Contributors Can Improve

1. Add rejected-path vectors for more AMT states.
2. Replace prototype membership flags with audited Merkle gadgets.
3. Add circuit compiler integration behind an optional script.
4. Add country-pack fixtures for one strong-postcode, one weak-postcode, and
   one no-postcode region.
5. Connect `zk-address-predicates`, `agid-interoperability-contracts`, and AMT
   to the same fixture set.

## First Good Issues

- Document a new refusal case in `demos/no-postcode-private-proof-demo.json`.
- Add a static circuit safety assertion to
  `scripts/verify_no_postcode_zk_demo.py`.
- Add one public-signal allowlist test.
- Improve `audit/zk-audit-readiness.md` with an auditor question.

## Maintainer Rules

- Do not accept raw personal addresses in fixtures.
- Do not accept recipient records.
- Do not accept private keys, proof secrets, or witness dumps.
- Do not label the circuit as production-ready before external audit.
- Keep Ethereum usage root-only.

