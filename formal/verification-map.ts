export type ClaimClass =
  | 'formal'
  | 'executable-model'
  | 'empirical-target'
  | 'implementation-test'
  | 'speculative'
  | 'out-of-scope';

export type VerificationItem = {
  claim: string;
  classification: ClaimClass;
  evidencePath: string;
  productionClaimAllowed: boolean;
};

export function canPromoteToProductionClaim(item: VerificationItem): boolean {
  return item.productionClaimAllowed && ['formal', 'implementation-test'].includes(item.classification);
}
