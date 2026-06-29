import type { AddressCandidate, ResolutionContext, ResolutionResult } from './definitions.ts';
import { hasSufficientEvidence } from './definitions.ts';

export function decideResolution(candidates: AddressCandidate[], context: ResolutionContext): ResolutionResult {
  if (candidates.length === 0) {
    return { state: 'unresolved', candidateIds: [], reason: 'candidate-set-empty' };
  }

  const sufficient = candidates.filter(candidate => hasSufficientEvidence(candidate, context.threshold));
  if (sufficient.length === 0) {
    return {
      state: 'manual_review',
      candidateIds: candidates.map(candidate => candidate.id),
      reason: 'candidate-evidence-below-threshold',
    };
  }

  if (sufficient.length > 1) {
    return {
      state: 'ambiguous',
      candidateIds: sufficient.map(candidate => candidate.id),
      reason: 'multiple-sufficient-candidates',
    };
  }

  return {
    state: 'verified',
    candidateIds: [sufficient[0].id],
    reason: 'single-sufficient-candidate',
  };
}
