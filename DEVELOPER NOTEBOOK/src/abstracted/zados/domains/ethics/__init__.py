"""
Ethics reward domain.

This domain evaluates alignment with ethical constraints and downstream
consequences of system behavior. It is designed to operate as a
governance and safety constraint rather than an optimization target.

Concrete evaluators and enforcement logic are intentionally withheld
from this public release.
"""

from .domain import EthicsDomain

__all__ = [
    "EthicsDomain",
]

# ---------------------------------------------------------------------
# Redacted ethics submodules
# ---------------------------------------------------------------------
# The following ethical evaluators exist internally but are not exposed
# in this public interface. They span intent analysis, autonomy
# preservation, fairness, long-horizon impact assessment, and human
# cognition alignment.
#
# Submodules intentionally withheld include (non-exhaustive):
# - Intent clarity evaluation
# - Autonomy and consent preservation
# - Timeline and long-horizon reflection
# - Feasibility across temporal and civilizational horizons
# - Downstream risk amplification analysis
# - Failure mode awareness
# - Fairness and bias assessment
# - Human cognition alignment
#
# Public exposure status:
#   0 / 8 ethics submodules exposed
#   8 / 8 ethics submodules intentionally redacted
