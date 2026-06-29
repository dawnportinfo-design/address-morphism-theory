import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import { decideZkPredicateEligibility, type AMTZkPredicate, type AMTZkResolutionState } from '../formal/amt-zk-compatibility.ts';

type ContractVector = {
  id: string;
  amt: {
    resolutionState: AMTZkResolutionState;
    allowedPredicates: AMTZkPredicate[];
  };
  zk: {
    predicate: AMTZkPredicate;
  };
};

const contractFixturePath = '../agid-interoperability-contracts/fixtures/interop-vectors.json';
const localFixturePath = 'tests/fixtures/interop-vectors.json';
const fixturePath = fs.existsSync(contractFixturePath) ? contractFixturePath : localFixturePath;

const fixture = JSON.parse(fs.readFileSync(fixturePath, 'utf8')) as {
  vectors: ContractVector[];
};

test('AMT conformance reads shared interop vectors', () => {
  assert.ok(fixture.vectors.length >= 4);
});

test('AMT verified vector allows postal-equivalent proof request', () => {
  const vector = fixture.vectors.find((item) => item.id === 'verified-postal-proof-allowed');
  assert.ok(vector);
  assert.equal(decideZkPredicateEligibility(vector.amt.resolutionState, vector.zk.predicate), 'allowed');
});

test('AMT unresolved vector blocks proof request', () => {
  const vector = fixture.vectors.find((item) => item.id === 'unresolved-proof-blocked');
  assert.ok(vector);
  assert.equal(decideZkPredicateEligibility(vector.amt.resolutionState, vector.zk.predicate), 'blocked');
});

test('AMT no-postcode demo keeps postal-equivalent predicate eligible only after verified resolution', () => {
  const vector = fixture.vectors.find((item) => item.id === 'no-postcode-agid-to-zk-demo');
  assert.ok(vector);
  assert.equal(vector.amt.resolutionState, 'verified');
  assert.equal(vector.zk.predicate, 'postal_equivalent_membership');
  assert.equal(decideZkPredicateEligibility(vector.amt.resolutionState, vector.zk.predicate), 'allowed');
});
