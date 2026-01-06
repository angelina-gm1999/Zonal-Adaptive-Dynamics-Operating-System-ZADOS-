"""
Logic reward domain.

This domain evaluates epistemic soundness, consistency, and semantic
stability of system outputs. Only a curated subset of submodules is
exposed publicly; additional evaluators exist internally and are
intentionally redacted.
"""

from .domain import LogicDomain

# ---------------------------------------------------------------------
# Publicly exposed logic submodules (curated)
# ---------------------------------------------------------------------

from .epistemic_calibration import EpistemicCalibrationSubmodule
from .uncertainty_acknowledgment import UncertaintyAcknowledgmentSubmodule
from .internal_consistency import InternalConsistencySubmodule
from .semantic_continuity import SemanticContinuitySubmodule


__all__ = [
    "LogicDomain",
    "EpistemicCalibrationSubmodule",
    "UncertaintyAcknowledgmentSubmodule",
    "InternalConsistencySubmodule",
    "SemanticContinuitySubmodule",
]

# ---------------------------------------------------------------------
# Redacted internal submodules
# ---------------------------------------------------------------------
# Additional logic evaluators exist but are intentionally not exported.
# These include longitudinal, contrastive, abstention-related, and
# trace-based evaluators whose implementations and interfaces are
# withheld in this public release.
#
# Public exposure status:
#   4 / 11 logic submodules exposed
#   7 / 11 logic submodules redacted
