import type { AddressCandidate, ResolutionContext, ResolutionResult } from './definitions.ts';
import { decideResolution } from './unresolvability.ts';

export type MorphismTrace = {
  surface: string;
  normalized: string;
  candidateCount: number;
  result: ResolutionResult;
  pidIssued: boolean;
};

export function normalizeExpression(surface: string): string {
  return surface.trim().replace(/\s+/g, ' ').toLocaleLowerCase();
}

export function runMorphismChain(
  surface: string,
  candidates: AddressCandidate[],
  context: ResolutionContext,
): MorphismTrace {
  const normalized = normalizeExpression(surface);
  const result = decideResolution(candidates, context);
  return {
    surface,
    normalized,
    candidateCount: candidates.length,
    result,
    pidIssued: result.state === 'verified',
  };
}
