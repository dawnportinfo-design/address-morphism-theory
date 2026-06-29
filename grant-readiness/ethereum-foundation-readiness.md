# Ethereum Foundation Readiness Package

This note frames Address Morphism Theory (AMT) for Ethereum public-good review.
It is intentionally conservative: AMT does not ask Ethereum to store addresses.
It asks Ethereum-compatible tooling to verify public roots, policies, and
privacy-preserving predicates over AMT outputs.

## Fit

The strongest fit is a public-good package for privacy-preserving address
eligibility:

```text
AMT resolution -> AMT envelope -> ZK predicate -> root-only Ethereum anchor
```

The grant-worthy claim is not "addresses on-chain." The claim is:

> people, merchants, carriers, hotels, lockers, and public services should be
> able to verify delivery-relevant facts without publishing the address itself.

## Ethereum Boundary

Allowed on-chain or chain-adjacent data:

- evidence root;
- issuer registry root;
- revocation root;
- freshness root;
- schema hash;
- verifier policy ID;
- epoch and chain ID;
- proof-verification result when policy permits.

Forbidden data:

- raw address;
- recipient;
- PID value;
- precise private coordinate;
- proof witness;
- private key;
- proof secret;
- arbitrary memo fields that can smuggle private material.

The executable boundary is `formal/ethereum-root-anchoring.ts`.

## Public-Good Deliverables

1. AMT-to-ZK envelope specification.
2. Ethereum root-anchor specification.
3. ZK predicate DSL for delivery, region, quality, consent, freshness, and
   revocation predicates.
4. Test vectors shared with `zk-address-predicates` and
   `agid-interoperability-contracts`.
5. Verifier policy fixtures and refusal tests.
6. Circuit-readiness matrix that separates implemented models from audited
   circuits.
7. No-postcode demo: AGID region -> postal-equivalent predicate -> validation ->
   proof policy decision.
8. Publication-safety gate for raw address, witness, and key material.

## Six-Month Milestones

| Month | Milestone | Evidence |
| --- | --- | --- |
| 1 | Root-anchor and verifier-policy schemas | TypeScript model and tests |
| 2 | Shared fixtures across AMT, ZK, validation, and postal theory | Cross-repo vector set |
| 3 | Predicate DSL profile for no-postcode regions | Local verifier and refusal tests |
| 4 | Prototype circuit profiles | Circuit-readiness matrix, no audit claim |
| 5 | Demo path for postal-equivalent private proof | Reproducible local script |
| 6 | Security review package | Threat model, non-claims, audit checklist |

## Review Safety

AMT should make the following non-claims explicit in any Ethereum Foundation
application:

- ZK does not fix wrong AMT resolution.
- Ethereum anchors do not prove global candidate-generation completeness.
- Root anchoring is not an address registry.
- Test vectors are not a cryptographic audit.
- Circuit-ready does not mean production audited.

## Why This Is Ethereum-Relevant

Ethereum can provide neutral coordination and verifiability for roots and
policies while preserving off-chain address privacy. That is a better fit than
putting addresses, identity documents, or delivery locations directly on-chain.

The result is an Ethereum-compatible public-good layer for private address
predicates, not an Ethereum-dependent address system.

## Sources To Cite In Applications

- Ethereum Foundation Ecosystem Support Program:
  <https://esp.ethereum.foundation/>
- ESP applicant guidance:
  <https://esp.ethereum.foundation/applicants>
