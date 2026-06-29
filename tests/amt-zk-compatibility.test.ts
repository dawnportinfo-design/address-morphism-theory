import assert from 'node:assert/strict';
import test from 'node:test';
import { decideZkPredicateEligibility } from '../formal/amt-zk-compatibility.ts';

test('verified AMT state can request a delivery-zone ZK predicate', () => {
  assert.equal(decideZkPredicateEligibility('verified', 'delivery_zone_eligibility'), 'allowed');
});

test('partial AMT state cannot upgrade into precise deliverability proof', () => {
  assert.equal(decideZkPredicateEligibility('partial', 'delivery_zone_eligibility'), 'blocked');
  assert.equal(decideZkPredicateEligibility('partial', 'quality_threshold'), 'limited');
});

test('unsafe AMT states block proof issuance', () => {
  assert.equal(decideZkPredicateEligibility('ambiguous', 'region_membership'), 'blocked');
  assert.equal(decideZkPredicateEligibility('unresolved', 'region_membership'), 'blocked');
  assert.equal(decideZkPredicateEligibility('rejected', 'freshness'), 'blocked');
});

test('disputed states are policy dependent', () => {
  assert.equal(decideZkPredicateEligibility('disputed', 'anonymous_rate_limit'), 'policy_dependent');
  assert.equal(decideZkPredicateEligibility('disputed', 'delivery_zone_eligibility'), 'policy_dependent');
});

