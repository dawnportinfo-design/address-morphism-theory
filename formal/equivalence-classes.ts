import type { Purpose } from './definitions.ts';

export type AddressExpression = {
  expression: string;
  referentId: string;
  validPurposes: Purpose[];
};

export function equivalentForPurpose(left: AddressExpression, right: AddressExpression, purpose: Purpose): boolean {
  return (
    left.referentId === right.referentId &&
    left.validPurposes.includes(purpose) &&
    right.validPurposes.includes(purpose)
  );
}

export function equivalenceClass(expressions: AddressExpression[], target: AddressExpression, purpose: Purpose) {
  return expressions.filter(expression => equivalentForPurpose(expression, target, purpose));
}
