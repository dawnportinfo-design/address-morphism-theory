import { createHash } from 'node:crypto';

export type EthereumAnchorPayload = {
  version: 'ethereum-root-anchor-v0.1';
  chainId: number;
  epoch: string;
  evidenceRoot: string;
  issuerRegistryRoot: string;
  policyId: string;
  schemaHash: string;
  freshnessRoot?: string;
  revocationRoot?: string;
  publicSignalHash?: string;
};

export type EthereumProofSystem = 'groth16' | 'plonk' | 'halo2' | 'stark';

export type EthereumVerifierPolicy = {
  version: 'ethereum-verifier-policy-v0.1';
  policyId: string;
  proofSystem: EthereumProofSystem;
  circuitId: string;
  allowedPredicates: string[];
  maxFreshnessDays: number;
  minAnonymitySet: number;
  disallowRawAddress: true;
  disallowPreciseCoordinates: true;
};

export type EthereumAnchorValidation = {
  ok: boolean;
  errors: string[];
  forbiddenPaths: string[];
};

const ROOT_FIELDS = [
  'evidenceRoot',
  'issuerRegistryRoot',
  'schemaHash',
  'freshnessRoot',
  'revocationRoot',
  'publicSignalHash',
] as const;

const REQUIRED_ANCHOR_FIELDS = [
  'version',
  'chainId',
  'epoch',
  'evidenceRoot',
  'issuerRegistryRoot',
  'policyId',
  'schemaHash',
] as const;

const ALLOWED_ANCHOR_FIELDS = new Set<string>([
  ...REQUIRED_ANCHOR_FIELDS,
  'freshnessRoot',
  'revocationRoot',
  'publicSignalHash',
]);

const FORBIDDEN_FIELD_PATTERNS = [
  /address/i,
  /raw/i,
  /recipient/i,
  /pid$/i,
  /pidcommitment/i,
  /precise/i,
  /coordinate/i,
  /lat/i,
  /lon/i,
  /lng/i,
  /witness/i,
  /private/i,
  /secret/i,
  /key/i,
  /proofmaterial/i,
];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

export function isRootLike(value: unknown): value is string {
  if (typeof value !== 'string') {
    return false;
  }

  return (
    /^0x[0-9a-fA-F]{64}$/.test(value) ||
    /^sha256:[0-9a-fA-F]{64}$/.test(value) ||
    /^bafy[a-z2-7]{20,}$/.test(value)
  );
}

export function isPolicyId(value: unknown): value is string {
  return typeof value === 'string' && /^[a-z0-9][a-z0-9._:-]{3,128}$/i.test(value);
}

export function collectForbiddenPaths(value: unknown, path = '$'): string[] {
  if (!isRecord(value)) {
    return [];
  }

  const matches: string[] = [];
  for (const [key, child] of Object.entries(value)) {
    const childPath = `${path}.${key}`;
    const isExplicitDenyFlag = key.startsWith('disallow');
    if (!isExplicitDenyFlag && FORBIDDEN_FIELD_PATTERNS.some((pattern) => pattern.test(key))) {
      matches.push(childPath);
    }
    matches.push(...collectForbiddenPaths(child, childPath));
  }

  return matches;
}

export function validateEthereumAnchorPayload(payload: unknown): EthereumAnchorValidation {
  const errors: string[] = [];
  const forbiddenPaths = collectForbiddenPaths(payload);

  if (!isRecord(payload)) {
    return {
      ok: false,
      errors: ['payload must be an object'],
      forbiddenPaths,
    };
  }

  for (const key of Object.keys(payload)) {
    if (!ALLOWED_ANCHOR_FIELDS.has(key)) {
      errors.push(`unknown anchor field: ${key}`);
    }
  }

  for (const key of REQUIRED_ANCHOR_FIELDS) {
    if (!(key in payload)) {
      errors.push(`missing anchor field: ${key}`);
    }
  }

  if (payload.version !== 'ethereum-root-anchor-v0.1') {
    errors.push('version must be ethereum-root-anchor-v0.1');
  }

  if (!Number.isInteger(payload.chainId) || Number(payload.chainId) <= 0) {
    errors.push('chainId must be a positive integer');
  }

  if (typeof payload.epoch !== 'string' || !/^[0-9]{4}-[0-9]{2}$/.test(payload.epoch)) {
    errors.push('epoch must use YYYY-MM form');
  }

  if (!isPolicyId(payload.policyId)) {
    errors.push('policyId must be a stable policy identifier');
  }

  for (const field of ROOT_FIELDS) {
    if (field in payload && !isRootLike(payload[field])) {
      errors.push(`${field} must be a root, digest, or CID`);
    }
  }

  if (forbiddenPaths.length > 0) {
    errors.push('payload contains forbidden private address or witness fields');
  }

  return {
    ok: errors.length === 0,
    errors,
    forbiddenPaths,
  };
}

export function deriveAnchorCommitment(payload: EthereumAnchorPayload): string {
  const validation = validateEthereumAnchorPayload(payload);
  if (!validation.ok) {
    throw new Error(`invalid Ethereum anchor payload: ${validation.errors.join('; ')}`);
  }

  const canonical = Object.fromEntries(
    Object.entries(payload)
      .filter(([, value]) => value !== undefined)
      .sort(([left], [right]) => left.localeCompare(right)),
  );

  return `0x${createHash('sha256').update(JSON.stringify(canonical)).digest('hex')}`;
}

export function validateEthereumVerifierPolicy(policy: unknown): EthereumAnchorValidation {
  const errors: string[] = [];
  const forbiddenPaths = collectForbiddenPaths(policy);

  if (!isRecord(policy)) {
    return {
      ok: false,
      errors: ['policy must be an object'],
      forbiddenPaths,
    };
  }

  if (policy.version !== 'ethereum-verifier-policy-v0.1') {
    errors.push('version must be ethereum-verifier-policy-v0.1');
  }

  if (!isPolicyId(policy.policyId)) {
    errors.push('policyId must be a stable policy identifier');
  }

  if (!['groth16', 'plonk', 'halo2', 'stark'].includes(String(policy.proofSystem))) {
    errors.push('proofSystem must name a concrete proof system');
  }

  if (typeof policy.circuitId !== 'string' || policy.circuitId.length < 4) {
    errors.push('circuitId must identify the audited circuit or profile');
  }

  if (!Array.isArray(policy.allowedPredicates) || policy.allowedPredicates.length === 0) {
    errors.push('allowedPredicates must be a non-empty array');
  }

  if (!Number.isInteger(policy.maxFreshnessDays) || Number(policy.maxFreshnessDays) <= 0) {
    errors.push('maxFreshnessDays must be positive');
  }

  if (!Number.isInteger(policy.minAnonymitySet) || Number(policy.minAnonymitySet) < 2) {
    errors.push('minAnonymitySet must be at least 2');
  }

  if (policy.disallowRawAddress !== true) {
    errors.push('disallowRawAddress must be true');
  }

  if (policy.disallowPreciseCoordinates !== true) {
    errors.push('disallowPreciseCoordinates must be true');
  }

  if (forbiddenPaths.length > 0) {
    errors.push('policy contains forbidden private address or witness fields');
  }

  return {
    ok: errors.length === 0,
    errors,
    forbiddenPaths,
  };
}

export const ethereumFoundationReadinessChecklist = [
  'root-only anchoring',
  'no address, PID, recipient, coordinate, witness, or key material on-chain',
  'open-source verifier policy and test vectors',
  'circuit-readiness matrix before production claims',
  'explicit non-claim that ZK cannot repair bad AMT resolution',
] as const;
