export type AMTPurpose =
  | 'delivery'
  | 'identity'
  | 'map_search'
  | 'postal_equivalent'
  | 'private_proof'
  | 'audit';

export type EvidencePolarity = 'support' | 'contradiction';

export type AMTEvidence = {
  id: string;
  candidateId: string;
  confidence: number;
  fresh: boolean;
  licensed: boolean;
  polarity: EvidencePolarity;
};

export type AMTCandidate = {
  id: string;
  referentId: string;
  compatiblePurposes: AMTPurpose[];
};

export type AMTResolutionKind = 'resolved' | 'unresolved' | 'ambiguous' | 'contradicted';

export type AMTFiniteInstance = {
  purpose: AMTPurpose;
  threshold: number;
  candidates: AMTCandidate[];
  evidence: AMTEvidence[];
};

export type AMTResolution = {
  kind: AMTResolutionKind;
  referentId?: string;
  candidateId?: string;
  scoreByCandidate: Record<string, number>;
  reason: string;
};

export type AMTPublicProjection = {
  kind: AMTResolutionKind;
  referentCommitment?: string;
  qualityClass: 'verified' | 'partial' | 'manual_required' | 'rejected';
  privateContentExposed: false;
};

export function scoreCandidate(candidate: AMTCandidate, evidence: AMTEvidence[], purpose: AMTPurpose): number {
  if (!candidate.compatiblePurposes.includes(purpose)) {
    return 0;
  }

  return evidence
    .filter((item) => item.candidateId === candidate.id && item.fresh && item.licensed && item.polarity === 'support')
    .reduce((sum, item) => sum + item.confidence, 0);
}

export function hasContradiction(candidate: AMTCandidate, evidence: AMTEvidence[]): boolean {
  return evidence.some(
    (item) => item.candidateId === candidate.id && item.fresh && item.licensed && item.polarity === 'contradiction',
  );
}

export function resolveFiniteAMT(instance: AMTFiniteInstance): AMTResolution {
  const scoreByCandidate = Object.fromEntries(
    instance.candidates.map((candidate) => [
      candidate.id,
      scoreCandidate(candidate, instance.evidence, instance.purpose),
    ]),
  );

  const contradicted = instance.candidates.filter((candidate) => hasContradiction(candidate, instance.evidence));
  if (contradicted.length > 0) {
    return {
      kind: 'contradicted',
      scoreByCandidate,
      reason: 'fresh licensed contradiction exists',
    };
  }

  const passing = instance.candidates.filter((candidate) => scoreByCandidate[candidate.id] >= instance.threshold);
  if (passing.length === 0) {
    return {
      kind: 'unresolved',
      scoreByCandidate,
      reason: 'no candidate reached threshold',
    };
  }

  if (passing.length > 1) {
    return {
      kind: 'ambiguous',
      scoreByCandidate,
      reason: 'multiple candidates reached threshold',
    };
  }

  const selected = passing[0];
  return {
    kind: 'resolved',
    referentId: selected.referentId,
    candidateId: selected.id,
    scoreByCandidate,
    reason: 'unique candidate reached threshold',
  };
}

export function canIssuePid(resolution: AMTResolution): boolean {
  return resolution.kind === 'resolved' && Boolean(resolution.referentId);
}

export function projectPublicResolution(resolution: AMTResolution): AMTPublicProjection {
  if (resolution.kind === 'resolved' && resolution.referentId) {
    return {
      kind: 'resolved',
      referentCommitment: `commitment:${resolution.referentId}`,
      qualityClass: 'verified',
      privateContentExposed: false,
    };
  }

  if (resolution.kind === 'ambiguous' || resolution.kind === 'contradicted') {
    return {
      kind: resolution.kind,
      qualityClass: 'manual_required',
      privateContentExposed: false,
    };
  }

  return {
    kind: 'unresolved',
    qualityClass: 'partial',
    privateContentExposed: false,
  };
}

export function estimateFiniteResolutionComplexity(candidateCount: number, evidenceCount: number): string {
  if (candidateCount < 0 || evidenceCount < 0) {
    throw new Error('counts must be non-negative');
  }
  return `O(${candidateCount} + ${evidenceCount})`;
}
