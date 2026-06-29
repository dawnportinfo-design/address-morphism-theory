export function shannonEntropy(probabilities: number[]): number {
  return probabilities
    .filter(probability => probability > 0)
    .reduce((sum, probability) => sum - probability * Math.log2(probability), 0);
}

export function ambiguityReduction(before: number[], after: number[]): number {
  return shannonEntropy(before) - shannonEntropy(after);
}

export function isOverCompressed(reduction: number, privacyLeakage: number, leakageLimit: number): boolean {
  return reduction > 0 && privacyLeakage > leakageLimit;
}
