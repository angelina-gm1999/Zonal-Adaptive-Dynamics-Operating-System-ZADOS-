from __future__ import annotations

from typing import Dict, Any, Optional, Iterable

from zados.reward.base.interfaces import RewardDomain
from zados.reward.base.types import RewardContext, RewardDomainResult

# NOTE:
# Concrete logic submodules are selectively imported to control
# public surface area. Additional evaluators exist internally
# but are intentionally not referenced here.

from zados.reward.domains.logic.epistemic_calibration import (
    EpistemicCalibrationSubmodule,
)
from zados.reward.domains.logic.uncertainty_acknowledgment import (
    UncertaintyAcknowledgmentSubmodule,
)
from zados.reward.domains.logic.internal_consistency import (
    InternalConsistencySubmodule,
)
from zados.reward.domains.logic.semantic_continuity import (
    SemanticContinuitySubmodule,
)

# Capability ports (interfaces only; behavior withheld)
from zados.reward.domains.logic.ports import MemoryContrastPort, CognitiveTracePort


class LogicDomain(RewardDomain):
    """
    Logic / Coherence reward domain.

    Evaluates epistemic soundness, internal consistency, and semantic
    stability of system outputs.

    This public implementation exposes a curated subset of logic
    evaluators. Additional submodules and aggregation strategies
    exist internally and are intentionally redacted.
    """

    def __init__(
        self,
        *,
        memory_contrast: Optional[MemoryContrastPort] = None,
        cognitive_trace: Optional[CognitiveTracePort] = None,
    ):
        # Optional capability hooks
        self._memory_contrast = memory_contrast
        self._cognitive_trace = cognitive_trace

        # Curated public evaluators
        self._evaluators: Iterable = (
            EpistemicCalibrationSubmodule(),
            UncertaintyAcknowledgmentSubmodule(),
            InternalConsistencySubmodule(
                memory_contrast=self._memory_contrast
            ),
            SemanticContinuitySubmodule(),
        )

    @property
    def domain_name(self) -> str:
        return "logic"

    def evaluate(
        self,
        state: Dict[str, Any],
        ctx: RewardContext,
    ) -> RewardDomainResult:
        """
        Execute logic-domain evaluation.

        The ordering, weighting, and arbitration of evaluators are
        deliberately abstracted in this public release.
        """
        subscores: Dict[str, Any] = {}
        flags: Dict[str, Any] = {}

        for evaluator in self._evaluators:
            result = evaluator.evaluate(state, ctx)
            subscores[result.name] = result
            flags.update(result.flags)

        general_score = self._aggregate(subscores)

        return RewardDomainResult(
            domain=self.domain_name,
            general_score=general_score,
            subscores=subscores,
            flags=flags,
            meta={
                "public_submodules": list(subscores.keys()),
                "capabilities": {
                    "memory_contrast": self._memory_contrast is not None,
                    "cognitive_trace": self._cognitive_trace is not None,
                },
            },
        )

    # -----------------------------------------------------------------
    # Aggregation (intentionally abstracted)
    # -----------------------------------------------------------------

    def _aggregate(self, subscores: Dict[str, Any]) -> float:
        """
        Aggregate submodule outputs into a domain-level score.

        Concrete weighting, normalization, and arbitration logic
        is intentionally withheld from the public interface.
        """
        if not subscores:
            return 0.0

        # Placeholder aggregation for interface completeness only
        return sum(s.score for s in subscores.values()) / max(len(subscores), 1)


# ---------------------------------------------------------------------
# Disclosure note
# ---------------------------------------------------------------------
# Logic domain exposure status:
#   4 / 12 logic submodules publicly exposed
#   8 / 12 logic submodules intentionally redacted
