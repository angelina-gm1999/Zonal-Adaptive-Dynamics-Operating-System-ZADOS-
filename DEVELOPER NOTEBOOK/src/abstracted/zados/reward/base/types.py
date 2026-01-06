from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class RewardContext:
    """
    Minimal, model-agnostic context container passed to reward evaluators.

    This object carries evaluation-scoped metadata without embedding
    assumptions about model internals, execution environment, or
    downstream control flow.

    Fields may be extended in later phases without breaking interface
    compatibility.
    """
    mode: str = "default"
    timestamp: Optional[float] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RewardSubscore:
    """
    Result produced by an individual reward submodule.

    Represents a normalized evaluative signal and any associated
    diagnostic annotations. Interpretation and enforcement are
    handled elsewhere.
    """
    name: str
    score: float  # expected normalized range: 0.0 – 1.0
    flags: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RewardDomainResult:
    """
    Aggregated output of a reward domain evaluation.

    Encapsulates a domain-level score alongside its constituent
    subscores and structured annotations. Aggregation strategy,
    weighting, and arbitration logic are intentionally external.
    """
    domain: str
    general_score: float  # expected normalized range: 0.0 – 1.0
    subscores: Dict[str, RewardSubscore] = field(default_factory=dict)
    flags: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RewardWeights:
    """
    Declarative container for domain weighting parameters.

    In early versions, weights are treated as static configuration.
    Dynamic adaptation or learning-based updates are out of scope
    for this interface.
    """
    weights: Dict[str, float] = field(default_factory=dict)

    def get(self, domain: str, default: float = 0.0) -> float:
        """
        Retrieve the weight associated with a given domain.
        """
        return float(self.weights.get(domain, default))


@dataclass(frozen=True)
class RewardMetaDirective:
    """
    High-level directive emitted by synthesis or arbitration layers.

    This structure conveys output gating and routing intent without
    prescribing how downstream components must implement it.
    """
    allow_output: bool = True
    abstain: bool = False
    suppress: bool = False

    # Response shaping hints (kept generic and model-agnostic)
    directives: Dict[str, Any] = field(default_factory=dict)

    # Routing or selection hints for downstream components
    routing: Dict[str, Any] = field(default_factory=dict)

    # Risk, compliance, and audit signals
    flags: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)
