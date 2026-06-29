import assert from 'node:assert/strict';
import { test } from 'node:test';

import { decideResolution } from '../formal/unresolvability.ts';

test('empty candidates remain unresolved', () => {
  const result = decideResolution([], {
    jurisdiction: 'HK',
    language: 'en',
    purpose: 'delivery',
    threshold: 0.9,
  });

  assert.equal(result.state, 'unresolved');
  assert.equal(result.reason, 'candidate-set-empty');
});

test('multiple sufficient candidates are ambiguous', () => {
  const result = decideResolution([
    {
      id: 'a',
      type: 'entrance',
      evidence: [{ id: 'field-a', authority: 'field_report', confidence: 0.9, licenseDeclared: true, fresh: true }],
    },
    {
      id: 'b',
      type: 'entrance',
      evidence: [{ id: 'field-b', authority: 'field_report', confidence: 0.9, licenseDeclared: true, fresh: true }],
    },
  ], {
    jurisdiction: 'JP',
    language: 'ja',
    purpose: 'delivery',
    threshold: 0.8,
  });

  assert.equal(result.state, 'ambiguous');
});
