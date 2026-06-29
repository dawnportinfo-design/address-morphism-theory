import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ambiguityReduction, isOverCompressed, shannonEntropy } from '../formal/entropy.ts';

test('entropy model records ambiguity reduction and leakage risk separately', () => {
  assert.equal(shannonEntropy([1]), 0);
  assert.ok(ambiguityReduction([0.5, 0.5], [1]) > 0);
  assert.equal(isOverCompressed(1, 0.9, 0.5), true);
});
