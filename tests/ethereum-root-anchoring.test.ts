import assert from 'node:assert/strict';
import test from 'node:test';
import {
  deriveAnchorCommitment,
  ethereumFoundationReadinessChecklist,
  isRootLike,
  validateEthereumAnchorPayload,
  validateEthereumVerifierPolicy,
  type EthereumAnchorPayload,
  type EthereumVerifierPolicy,
} from '../formal/ethereum-root-anchoring.ts';

const rootA = '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
const rootB = '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';
const rootC = 'sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc';

const safeAnchor: EthereumAnchorPayload = {
  version: 'ethereum-root-anchor-v0.1',
  chainId: 1,
  epoch: '2026-06',
  evidenceRoot: rootA,
  issuerRegistryRoot: rootB,
  freshnessRoot: rootC,
  revocationRoot: '0xdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',
  policyId: 'agid.delivery.zk.v0',
  schemaHash: '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
};

test('Ethereum root anchor accepts only public roots and policy metadata', () => {
  const validation = validateEthereumAnchorPayload(safeAnchor);

  assert.equal(validation.ok, true);
  assert.deepEqual(validation.forbiddenPaths, []);
  assert.equal(isRootLike(safeAnchor.evidenceRoot), true);
});

test('anchor commitment is deterministic and root-shaped', () => {
  const commitment = deriveAnchorCommitment(safeAnchor);

  assert.match(commitment, /^0x[0-9a-f]{64}$/);
  assert.equal(commitment, deriveAnchorCommitment({ ...safeAnchor }));
});

test('anchor validation rejects raw address and witness-shaped fields', () => {
  const validation = validateEthereumAnchorPayload({
    ...safeAnchor,
    rawAddress: 'REDACTED',
    nested: {
      witness: 'REDACTED',
    },
  });

  assert.equal(validation.ok, false);
  assert(validation.forbiddenPaths.includes('$.rawAddress'));
  assert(validation.forbiddenPaths.includes('$.nested.witness'));
  assert(validation.errors.some((error) => error.includes('forbidden private address')));
});

test('anchor validation rejects non-root values and unknown fields', () => {
  const validation = validateEthereumAnchorPayload({
    ...safeAnchor,
    evidenceRoot: 'not-a-root',
    note: 'public memo',
  });

  assert.equal(validation.ok, false);
  assert(validation.errors.includes('evidenceRoot must be a root, digest, or CID'));
  assert(validation.errors.includes('unknown anchor field: note'));
});

test('verifier policy requires concrete proof system and privacy-deny defaults', () => {
  const policy: EthereumVerifierPolicy = {
    version: 'ethereum-verifier-policy-v0.1',
    policyId: 'agid.delivery.zk.v0',
    proofSystem: 'plonk',
    circuitId: 'region-membership-v0',
    allowedPredicates: ['region_membership', 'not_revoked', 'freshness'],
    maxFreshnessDays: 30,
    minAnonymitySet: 128,
    disallowRawAddress: true,
    disallowPreciseCoordinates: true,
  };

  assert.equal(validateEthereumVerifierPolicy(policy).ok, true);
});

test('verifier policy blocks vague circuits and address disclosure', () => {
  const validation = validateEthereumVerifierPolicy({
    version: 'ethereum-verifier-policy-v0.1',
    policyId: 'agid.delivery.zk.v0',
    proofSystem: 'unknown',
    circuitId: '',
    allowedPredicates: ['region_membership'],
    maxFreshnessDays: 30,
    minAnonymitySet: 1,
    disallowRawAddress: false,
    disallowPreciseCoordinates: false,
  });

  assert.equal(validation.ok, false);
  assert(validation.errors.includes('proofSystem must name a concrete proof system'));
  assert(validation.errors.includes('disallowRawAddress must be true'));
  assert(validation.errors.includes('disallowPreciseCoordinates must be true'));
});

test('readiness checklist states the Ethereum public-good boundary', () => {
  assert(ethereumFoundationReadinessChecklist.includes('root-only anchoring'));
  assert(
    ethereumFoundationReadinessChecklist.includes(
      'no address, PID, recipient, coordinate, witness, or key material on-chain',
    ),
  );
});
