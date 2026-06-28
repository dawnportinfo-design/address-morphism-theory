"""Executable helpers for Address Morphism Theory.

The package intentionally contains small, dependency-free reference models.
They are not production resolvers or audited zero-knowledge circuits.
"""

from .predicate_dsl import (
    AddressPredicateSubject,
    PredicatePolicy,
    PredicateResult,
    evaluate_predicates,
)

__all__ = [
    "AddressPredicateSubject",
    "PredicatePolicy",
    "PredicateResult",
    "evaluate_predicates",
]
