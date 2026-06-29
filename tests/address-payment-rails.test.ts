import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
  authorizeAddressUse,
  captureAddressUse,
  disputeAddressUse,
  isPublicTransactionSafe,
  reverseAddressUse,
  settleAddressReceipt,
  type AddressTransaction,
} from '../formal/address-payment-rails.ts';

const base: AddressTransaction = {
  transactionId: 'addr_txn_001',
  addressToken: 'addr_tok_delivery_001',
  purpose: 'delivery',
  requester: 'merchant-example',
  issuer: 'issuer-example',
  policyId: 'policy-delivery',
  status: 'requested',
  idempotencyKey: 'idem-001',
  createdAtEpochSeconds: 100,
  expiresAtEpochSeconds: 200,
  riskDecision: 'allow',
};

test('authorizes, captures, and settles an address-use transaction', () => {
  const decision = authorizeAddressUse(base, 120);
  assert.equal(decision.status, 'authorized');

  const authorized = { ...base, status: decision.status };
  const captured = captureAddressUse(authorized, 'receipt-001');
  assert.equal(captured.status, 'captured');

  const settled = settleAddressReceipt(captured);
  assert.equal(settled.status, 'settled');
});

test('requires review or declines without exposing raw address', () => {
  assert.equal(authorizeAddressUse({ ...base, riskDecision: 'review' }, 120).status, 'requires_review');
  assert.equal(authorizeAddressUse({ ...base, riskDecision: 'deny' }, 120).status, 'declined');
  assert.equal(isPublicTransactionSafe(base), true);
});

test('supports reversal before settlement and dispute after capture', () => {
  const reversed = reverseAddressUse({ ...base, status: 'authorized' }, 'cancelled');
  assert.equal(reversed.status, 'reversed');

  const disputed = disputeAddressUse({ ...base, status: 'captured', receiptId: 'receipt-001' });
  assert.equal(disputed.status, 'disputed');
});

test('public transaction safety rejects private address material keys', () => {
  assert.equal(isPublicTransactionSafe({ ...base, rawAddress: 'REDACTED' }), false);
});
