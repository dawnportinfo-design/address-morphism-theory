export type AMTZkResolutionState =
  | 'verified'
  | 'partial'
  | 'ambiguous'
  | 'unresolved'
  | 'rejected'
  | 'deprecated'
  | 'disputed';

export type AMTZkPredicate =
  | 'region_membership'
  | 'quality_threshold'
  | 'consent_scope'
  | 'freshness'
  | 'not_revoked'
  | 'delivery_zone_eligibility'
  | 'anonymous_rate_limit'
  | 'postal_equivalent_membership';

export type AMTZkDecision = 'allowed' | 'limited' | 'blocked' | 'policy_dependent';

const predicateRules: Record<AMTZkResolutionState, { decision: AMTZkDecision; predicates: AMTZkPredicate[] }> = {
  verified: {
    decision: 'allowed',
    predicates: [
      'region_membership',
      'quality_threshold',
      'consent_scope',
      'freshness',
      'not_revoked',
      'delivery_zone_eligibility',
      'anonymous_rate_limit',
      'postal_equivalent_membership',
    ],
  },
  partial: {
    decision: 'limited',
    predicates: ['quality_threshold', 'freshness', 'not_revoked', 'anonymous_rate_limit'],
  },
  ambiguous: {
    decision: 'blocked',
    predicates: ['freshness', 'not_revoked'],
  },
  unresolved: {
    decision: 'blocked',
    predicates: [],
  },
  rejected: {
    decision: 'blocked',
    predicates: [],
  },
  deprecated: {
    decision: 'blocked',
    predicates: ['freshness', 'not_revoked'],
  },
  disputed: {
    decision: 'policy_dependent',
    predicates: ['freshness', 'not_revoked', 'anonymous_rate_limit'],
  },
};

export function decideZkPredicateEligibility(
  resolutionState: AMTZkResolutionState,
  requestedPredicate: AMTZkPredicate,
): AMTZkDecision {
  const rule = predicateRules[resolutionState];
  if (!rule.predicates.includes(requestedPredicate)) {
    return resolutionState === 'disputed' ? 'policy_dependent' : 'blocked';
  }
  return rule.decision;
}
