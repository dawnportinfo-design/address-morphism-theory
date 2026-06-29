import assert from 'node:assert/strict';
import test from 'node:test';
import {
  canIssuePid,
  estimateFiniteResolutionComplexity,
  projectPublicResolution,
  resolveFiniteAMT,
  scoreCandidate,
  type AMTCandidate,
  type AMTEvidence,
} from '../formal/mathematical-core.ts';

const candidateA: AMTCandidate = {
  id: 'candidate:a',
  referentId: 'referent:a',
  compatiblePurposes: ['delivery', 'map_search'],
};

const candidateB: AMTCandidate = {
  id: 'candidate:b',
  referentId: 'referent:b',
  compatiblePurposes: ['delivery'],
};

test('candidate score uses fresh licensed supporting evidence for the declared purpose', () => {
  const evidence: AMTEvidence[] = [
    { id: 'e1', candidateId: 'candidate:a', confidence: 0.6, fresh: true, licensed: true, polarity: 'support' },
    { id: 'e2', candidateId: 'candidate:a', confidence: 0.4, fresh: false, licensed: true, polarity: 'support' },
    { id: 'e3', candidateId: 'candidate:a', confidence: 0.4, fresh: true, licensed: false, polarity: 'support' },
  ];

  assert.equal(scoreCandidate(candidateA, evidence, 'delivery'), 0.6);
  assert.equal(scoreCandidate(candidateA, evidence, 'identity'), 0);
});

test('existence theorem executable form resolves a unique candidate above threshold', () => {
  const resolution = resolveFiniteAMT({
    purpose: 'delivery',
    threshold: 0.8,
    candidates: [candidateA, candidateB],
    evidence: [
      { id: 'e1', candidateId: 'candidate:a', confidence: 0.9, fresh: true, licensed: true, polarity: 'support' },
      { id: 'e2', candidateId: 'candidate:b', confidence: 0.4, fresh: true, licensed: true, polarity: 'support' },
    ],
  });

  assert.equal(resolution.kind, 'resolved');
  assert.equal(resolution.referentId, 'referent:a');
  assert.equal(canIssuePid(resolution), true);
});

test('uniqueness theorem executable form refuses ties', () => {
  const resolution = resolveFiniteAMT({
    purpose: 'delivery',
    threshold: 0.8,
    candidates: [candidateA, candidateB],
    evidence: [
      { id: 'e1', candidateId: 'candidate:a', confidence: 0.9, fresh: true, licensed: true, polarity: 'support' },
      { id: 'e2', candidateId: 'candidate:b', confidence: 0.9, fresh: true, licensed: true, polarity: 'support' },
    ],
  });

  assert.equal(resolution.kind, 'ambiguous');
  assert.equal(canIssuePid(resolution), false);
});

test('contradiction blocks resolution even with high support', () => {
  const resolution = resolveFiniteAMT({
    purpose: 'delivery',
    threshold: 0.8,
    candidates: [candidateA],
    evidence: [
      { id: 'e1', candidateId: 'candidate:a', confidence: 0.9, fresh: true, licensed: true, polarity: 'support' },
      { id: 'e2', candidateId: 'candidate:a', confidence: 0.1, fresh: true, licensed: true, polarity: 'contradiction' },
    ],
  });

  assert.equal(resolution.kind, 'contradicted');
  assert.equal(canIssuePid(resolution), false);
});

test('public projection never exposes private content', () => {
  const projection = projectPublicResolution({
    kind: 'resolved',
    referentId: 'referent:a',
    candidateId: 'candidate:a',
    scoreByCandidate: { 'candidate:a': 0.9 },
    reason: 'unique candidate reached threshold',
  });

  assert.equal(projection.privateContentExposed, false);
  assert.equal(projection.referentCommitment, 'commitment:referent:a');
});

test('finite complexity estimate is explicit', () => {
  assert.equal(estimateFiniteResolutionComplexity(12, 40), 'O(12 + 40)');
  assert.throws(() => estimateFiniteResolutionComplexity(-1, 0));
});

