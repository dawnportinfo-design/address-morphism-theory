pragma circom 2.1.6;

/*
  NoPostcodePostalEquivalent

  Audit-target prototype circuit for a no-postcode region.

  Public signals are root and policy metadata only. The circuit must not expose
  raw address content, recipients, PID values, precise coordinates, proof
  internals, or keys.

  This prototype uses local constraint flags for membership and consent. A
  production circuit must replace those flags with audited Merkle inclusion,
  revocation, freshness, and issuer-registry gadgets.
*/

template BooleanFlag() {
  signal input value;
  value * (value - 1) === 0;
}

template AtLeastConstant(minimum) {
  signal input value;
  signal input slack;
  value === minimum + slack;
}

template AtMostConstant(maximum) {
  signal input value;
  signal input slack;
  value + slack === maximum;
}

template NoPostcodePostalEquivalent(minQualityBps, maxFreshnessDays, minAnonymitySet) {
  // Public verifier signals.
  signal input commitmentHash;
  signal input regionRoot;
  signal input freshnessRoot;
  signal input revocationRoot;
  signal input policyHash;
  signal input nullifier;
  signal input result;

  // Private envelope-derived checks. These are private signals in Circom.
  signal input amtResolved;
  signal input postalEquivalentMember;
  signal input regionMember;
  signal input qualityBps;
  signal input qualitySlack;
  signal input freshnessDays;
  signal input freshnessSlack;
  signal input revoked;
  signal input consentScopeOk;
  signal input anonymitySetSize;
  signal input anonymitySlack;

  component stateFlag = BooleanFlag();
  stateFlag.value <== amtResolved;

  component postalFlag = BooleanFlag();
  postalFlag.value <== postalEquivalentMember;

  component regionFlag = BooleanFlag();
  regionFlag.value <== regionMember;

  component revokedFlag = BooleanFlag();
  revokedFlag.value <== revoked;

  component consentFlag = BooleanFlag();
  consentFlag.value <== consentScopeOk;

  component qualityGate = AtLeastConstant(minQualityBps);
  qualityGate.value <== qualityBps;
  qualityGate.slack <== qualitySlack;

  component freshnessGate = AtMostConstant(maxFreshnessDays);
  freshnessGate.value <== freshnessDays;
  freshnessGate.slack <== freshnessSlack;

  component anonymityGate = AtLeastConstant(minAnonymitySet);
  anonymityGate.value <== anonymitySetSize;
  anonymityGate.slack <== anonymitySlack;

  amtResolved === 1;
  postalEquivalentMember === 1;
  regionMember === 1;
  revoked === 0;
  consentScopeOk === 1;
  result === 1;

  // Keep public roots live in the constraint system.
  commitmentHash * 1 === commitmentHash;
  regionRoot * 1 === regionRoot;
  freshnessRoot * 1 === freshnessRoot;
  revocationRoot * 1 === revocationRoot;
  policyHash * 1 === policyHash;
  nullifier * 1 === nullifier;
}

component main {
  public [
    commitmentHash,
    regionRoot,
    freshnessRoot,
    revocationRoot,
    policyHash,
    nullifier,
    result
  ]
} = NoPostcodePostalEquivalent(9000, 30, 128);

