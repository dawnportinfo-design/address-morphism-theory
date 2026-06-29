# 27. Address Payment Rails: Treating Address Use Like Electronic Payment

Electronic payment systems do not repeatedly expose a bank account number to
every merchant. They use tokens, authorization, capture, settlement, reversal,
chargeback, risk scoring, audit trails, and regulated intermediaries.

AMT can treat address use in the same way.

The central idea is:

```text
Do not copy the raw address into every system.
Authorize a purpose-bound address transaction.
Settle the transaction with receipts, proofs, lineage, and revocation.
```

## 27.1 Payment Analogy

| Electronic payment | Address-use equivalent |
| --- | --- |
| card number / account | private address referent |
| payment token | address alias, commitment, or scoped delivery token |
| authorization | consented address-use authorization |
| capture | handoff or fulfillment claim |
| settlement | receipt reconciliation between actors |
| refund / reversal | revocation, cancellation, or successor-code update |
| chargeback | delivery dispute, cannot-reach report, or misuse claim |
| merchant category | verifier purpose scope |
| fraud score | address risk and quality score |
| payment network rules | AMT resolver, issuer, and verifier policy |

This analogy is not merely metaphorical. It suggests a protocol architecture for
addresses that avoids repeated raw-address disclosure.

## 27.2 Address Transaction Object

An address transaction is a purpose-bound use of an address referent.

Minimum fields:

- `transactionId`
- `addressToken`
- `purpose`
- `requester`
- `issuer`
- `policyId`
- `status`
- `createdAt`
- `expiresAt`
- `receiptId`
- `riskDecision`

Forbidden public fields:

- raw address
- recipient record
- witness
- private key
- precise private coordinate
- decrypted QR payload

## 27.3 Authorization

Authorization answers:

> Is this actor allowed to use this address referent for this purpose now?

The authorization result should be one of:

- `authorized`
- `requires_review`
- `declined`
- `expired`
- `revoked`

Authorization must be idempotent. Repeating the same authorization request with
the same idempotency key should not create multiple address-use rights.

## 27.4 Capture And Handoff

Capture is the claim that an authorized address use was consumed for a concrete
operation: delivery accepted, hotel PMS export prepared, locker pickup enabled,
field handoff attempted, or POS receipt issued.

Capture must not reveal more address material than the role needs. A POS staff
surface may see `deliverable`, `alias`, `receipt`, and `riskDecision`, while a
carrier may receive a decryptable handoff object under policy.

## 27.5 Settlement

Settlement reconciles the parties' views:

- requester asked for address use
- issuer authorized it
- verifier checked policy
- operator performed or attempted handoff
- receipt records the outcome

Settlement does not require publishing the address. It requires compatible
receipts, timestamps, policy ids, and non-replayable identifiers.

## 27.6 Reversal, Dispute, And Revocation

Address systems need payment-like dispute flows.

- `reversal`: cancel before handoff
- `refund-like replacement`: issue successor token or successor PID
- `chargeback-like dispute`: recipient, carrier, hotel, or platform disputes use
- `cannot-reach`: operator reports bounded failure without revealing precise
  private telemetry
- `revocation`: token or credential is no longer valid

These states must be first-class. Treating them as operational exceptions hides
the most important audit evidence.

## 27.7 Clearing Network

The address clearing network is not necessarily a centralized company. It is a
logical role that validates policy, routes authorizations, records redacted
receipts, and enforces revocation and replay rules.

Possible implementations:

- local-first wallet and carrier verifier
- public-sector registry
- private carrier clearing service
- federation of country packs and issuer registries
- optional blockchain root anchoring without raw address data

## 27.8 Theorem: Raw Address Minimization

If an address transaction can be authorized, captured, settled, and disputed
using scoped tokens, commitments, receipts, and policy identifiers, then raw
address disclosure is not required for every participant.

This does not prove that no actor ever needs the address. It proves that address
knowledge can be role-minimized.

## 27.9 Consequence For AGID

AGID should expose address use as a protocol surface:

```text
authorizeAddressUse()
captureAddressUse()
settleAddressReceipt()
reverseAddressUse()
disputeAddressUse()
revokeAddressToken()
```

The API should look less like a form submission and more like a payment rail:
tokenized, scoped, auditable, reversible, and privacy-minimized.

Model hook: `formal/address-payment-rails.ts`, `tests/address-payment-rails.test.ts`.
