import assert from 'node:assert/strict';
import { test } from 'node:test';

import { equivalenceClass } from '../formal/equivalence-classes.ts';

test('equivalence is purpose-relative', () => {
  const expressions = [
    { expression: 'front entrance', referentId: 'r1', validPurposes: ['delivery'] as const },
    { expression: 'legal parcel', referentId: 'r1', validPurposes: ['identity'] as const },
  ];

  assert.equal(equivalenceClass(expressions, expressions[0], 'delivery').length, 1);
  assert.equal(equivalenceClass(expressions, expressions[0], 'identity').length, 0);
});
