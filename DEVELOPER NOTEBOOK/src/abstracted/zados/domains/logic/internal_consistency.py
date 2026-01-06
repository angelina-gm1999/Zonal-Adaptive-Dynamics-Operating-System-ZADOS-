from __future__ import annotations

from typing import Any, Dict

from zados.reward.base.interfaces import RewardSubmodule
from zados.reward.base.types import RewardContext, RewardSubscore
from zados.reward.base.structures import RewardFlag
from zados.reward.domains.logic.ports import MemoryContrastPort


class InternalConsistencySubmodule(RewardSubmodule):
    """
    Evaluates internal coherence of the current output.

    This submodule detects self-contradictions or incompatible internal
    representations using an attached contrast capability. The specific
    comparison mechanics and similarity metrics are intentionally
    abstracted in this public release.
    """

    def __init__(self, *, memory_contrast: MemoryContrastPort | None = None):
        self._memory_contrast = memory_contrast

    @property
    def name(self) -> str:
        return "internal_consistency"

    def evaluate(self, state: Dict[str, Any], ctx: RewardContext) -> RewardSubscore:
        # Capability not attached: evaluation cannot proceed
        if self._memory_contrast is None:
            return RewardSubscore(
                name=self.name,
                score=0.0,
                flags={
                    "missing_memory_contrast": RewardFlag(
                        name="missing_memory_contrast",
                        severity="warning",
                        message=(
                            "Internal consistency evaluation skipped: "
                            "no memory contrast capability attached."
                        ),
                    )
                },
                meta={"skipped": True},
            )

        representation = state.get("representation", {})

        result = self._contrast(representation, ctx)

        score = self._score_from_result(result)

        flags = {}
        if self._is_contradictory(result):
            flags["internal_contradiction"] = RewardFlag(
                name="internal_contradiction",
                severity="risk",
                message="Detected internal inconsistency within current output.",
            )

        return RewardSubscore(
            name=self.name,
            score=score,
            flags=flags,
            meta={
                "contrast_applied": True,
            },
        )

    # -----------------------------------------------------------------
    # Internal contrast handling (intentionally abstracted)
    # -----------------------------------------------------------------

    def _contrast(self, representation: Any, ctx: RewardContext) -> Any:
        """
        Apply internal contrast against the provided representation.

        Concrete comparison strategy, reference selection, and scoring
        semantics are intentionally withheld.
        """
        return self._memory_contrast.contrast(
            current=representation,
            query_type="internal",
            ctx_id=ctx.meta.get("context_id"),
        )

    def _score_from_result(self, result: Any) -> float:
        """
        Derive a normalized consistency score from contrast output.

        Exact mapping and thresholds are intentionally withheld.
        """
        # Placeholder normalization for interface completeness
        divergence = getattr(result, "divergence", 1.0)
        return max(0.0, 1.0 - divergence)

    def _is_contradictory(self, result: Any) -> bool:
        """
        Determine whether contrast output indicates a contradiction.

        Thresholds and heuristics are intentionally abstracted.
        """
        divergence = getattr(result, "divergence", 0.0)
        return divergence > 0.6
