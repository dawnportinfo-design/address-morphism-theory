export type AddressTransactionStatus =
  | 'requested'
  | 'authorized'
  | 'requires_review'
  | 'declined'
  | 'captured'
  | 'settled'
  | 'reversed'
  | 'disputed'
  | 'revoked'
  | 'expired';

export type AddressPurpose = 'delivery' | 'hotel_checkin' | 'locker_pickup' | 'field_handoff' | 'audit';

export type AddressTransaction = {
  transactionId: string;
  addressToken: string;
  purpose: AddressPurpose;
  requester: string;
  issuer: string;
  policyId: string;
  status: AddressTransactionStatus;
  idempotencyKey: string;
  createdAtEpochSeconds: number;
  expiresAtEpochSeconds: number;
  receiptId?: string;
  riskDecision: 'allow' | 'review' | 'deny';
};

export type AddressTransactionDecision = {
  status: AddressTransactionStatus;
  reason: string;
};

export function authorizeAddressUse(
  transaction: AddressTransaction,
  nowEpochSeconds: number,
): AddressTransactionDecision {
  if (transaction.status === 'revoked') return { status: 'revoked', reason: 'token-revoked' };
  if (nowEpochSeconds > transaction.expiresAtEpochSeconds) return { status: 'expired', reason: 'token-expired' };
  if (transaction.riskDecision === 'deny') return { status: 'declined', reason: 'risk-deny' };
  if (transaction.riskDecision === 'review') return { status: 'requires_review', reason: 'risk-review' };
  return { status: 'authorized', reason: 'policy-allowed' };
}

export function captureAddressUse(transaction: AddressTransaction, receiptId: string): AddressTransaction {
  if (transaction.status !== 'authorized') {
    return transaction;
  }
  return {
    ...transaction,
    status: 'captured',
    receiptId,
  };
}

export function settleAddressReceipt(transaction: AddressTransaction): AddressTransaction {
  if (transaction.status !== 'captured' || !transaction.receiptId) {
    return transaction;
  }
  return {
    ...transaction,
    status: 'settled',
  };
}

export function reverseAddressUse(transaction: AddressTransaction, reason: 'cancelled' | 'successor' | 'operator_error'): AddressTransaction {
  if (['settled', 'revoked'].includes(transaction.status)) {
    return transaction;
  }
  return {
    ...transaction,
    status: reason === 'successor' ? 'revoked' : 'reversed',
  };
}

export function disputeAddressUse(transaction: AddressTransaction): AddressTransaction {
  if (!['captured', 'settled'].includes(transaction.status)) {
    return transaction;
  }
  return {
    ...transaction,
    status: 'disputed',
  };
}

export function isPublicTransactionSafe(value: Record<string, unknown>): boolean {
  const serialized = JSON.stringify(value).toLowerCase();
  return !['rawaddress', 'recipient', 'witness', 'privatekey', 'decrypted', 'latitude', 'longitude'].some(forbidden =>
    serialized.includes(forbidden),
  );
}
