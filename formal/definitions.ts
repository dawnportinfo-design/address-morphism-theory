export type AddressState =
  | 'verified'
  | 'ambiguous'
  | 'unresolved'
  | 'rejected'
  | 'manual_review'
  | 'deprecated';

export type Purpose =
  | 'delivery'
  | 'identity'
  | 'map_search'
  | 'postal_zone'
  | 'private_proof'
  | 'audit';

export type EvidenceSource = {
  id: string;
  authority: 'official' | 'postal' | 'open_geo' | 'field_report' | 'institutional' | 'synthetic';
  confidence: number;
  licenseDeclared: boolean;
  fresh: boolean;
};

export type AddressCandidate = {
  id: string;
  type: 'building' | 'unit' | 'entrance' | 'locker' | 'port' | 'marine_region' | 'natural_place' | 'institution';
  evidence: EvidenceSource[];
};

export type ResolutionContext = {
  jurisdiction: string;
  language: string;
  purpose: Purpose;
  threshold: number;
};

export type ResolutionResult = {
  state: AddressState;
  candidateIds: string[];
  reason: string;
};

export function hasSufficientEvidence(candidate: AddressCandidate, threshold: number): boolean {
  const usable = candidate.evidence.filter(source => source.licenseDeclared && source.fresh);
  const confidence = usable.reduce((sum, source) => sum + source.confidence, 0);
  return confidence >= threshold;
}
