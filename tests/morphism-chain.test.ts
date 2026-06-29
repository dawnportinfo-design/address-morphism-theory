import assert from 'node:assert/strict';
import { test } from 'node:test';

import { runMorphismChain } from '../formal/morphism-chain.ts';

test('morphism chain issues PID only for a single sufficient candidate', () => {
  const trace = runMorphismChain('  Alias   A  ', [
    {
      id: 'candidate-1',
      type: 'building',
      evidence: [{ id: 'official-1', authority: 'official', confidence: 0.95, licenseDeclared: true, fresh: true }],
    },
  ], {
    jurisdiction: 'JP',
    language: 'ja',
    purpose: 'delivery',
    threshold: 0.9,
  });

  assert.equal(trace.normalized, 'alias a');
  assert.equal(trace.pidIssued, true);
  assert.equal(trace.result.state, 'verified');
});
