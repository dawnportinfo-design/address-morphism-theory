# Applications

This section maps ZK address predicates to products and workflows.

## Private Delivery

The merchant sees eligibility, alias, nullifier, and receipt. The carrier may
receive a separate decryptable envelope when the holder consents.

## POS and Locker

The terminal verifies acceptance status and receipt state. It should not display
hidden QR payload internals or private address text.

## Hotel and PMS

A hotel can verify freshness, jurisdiction compatibility, and consent scope
before exporting to PMS. The PMS boundary should receive safe cause codes rather
than raw verifier internals.

## Field Handoff

A field worker can produce a cannot-reach or delivered receipt. ZK predicates
can prove policy-compatible handoff state without publishing precise private
location evidence.

## Web3 Boundary

Public chains should receive roots, commitments, registry anchors, or verifier
receipts only. Address data and witness material are out of scope.

## Main Sources

- `chapters/zero-knowledge-address-predicates/05-applications-and-safety-boundaries.md`
- `papers/zero-knowledge-address-proofs-from-address-morphism-theory-ja.md`
