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
  assert.ok(fixture.vectors.length >= 3);
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
