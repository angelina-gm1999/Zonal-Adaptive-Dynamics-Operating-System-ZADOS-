from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import time
import uuid


# ---------------------------------------------------------------------
# Threshold specifications
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ThresholdSpec:
    """
    Declarative specification for numeric thresholds used in regime
    classification or state transitions.

    This structure defines boundary values and optional hysteresis,
    but does not encode transition logic or enforcement strategy.
    """
    lower: float
    upper: float
    hysteresis: float = 0.0
    label: Optional[str] = None

    def in_range(self, value: float) -> bool:
        """
        Check whether a value lies within the declared bounds.

        Note: higher-order transition behavior (e.g. hysteresis handling,
        persistence, or temporal smoothing) is intentionally excluded.
        """
        return self.lower <= value <= self.upper


# ---------------------------------------------------------------------
# Structured reward flags
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RewardFlag:
    """
    Immutable descriptor for a reward-related diagnostic signal.

    Flags communicate qualitative state information to downstream
    systems without embedding control logic.
    """
    name: str
    severity: str = "info"  # info | warning | risk | critical
    message: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RewardFlagSet:
    """
    Lightweight container for grouped reward flags.

    Designed for inspection, filtering, and audit rather than mutation
    or behavioral control.
    """
    flags: Tuple[RewardFlag, ...] = ()

    def has_severity(self, severity: str) -> bool:
        """
        Check for presence of at least one flag with the given severity.
        """
        return any(f.severity == severity for f in self.flags)

    def names(self) -> Tuple[str, ...]:
        """
        Return all flag identifiers in stable order.
        """
        return tuple(f.name for f in self.flags)


# ---------------------------------------------------------------------
# Provenance and audit records
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ProvenanceRecord:
    """
    Minimal immutable provenance record for auditability.

    Tracks origin and timing without exposing internal routing,
    aggregation, or decision logic.
    """
    provenance_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=lambda: time.time())
    source: Optional[str] = None
    notes: Dict[str, Any] = field(default_factory=dict)
