from __future__ import annotations

from typing import Dict, Any

from zados.reward.base.interfaces import RewardSubmodule
from zados.reward.base.types import RewardContext, RewardSubscore
from zados.reward.base.structures import RewardFlag


class UncertaintyAcknowledgmentSubmodule(RewardSubmodule):
    """
    Evaluates proportional acknowledgment of uncertainty.

    Operates exclusively on structured state signals rather than
    surface-level language features.
    """

    @property
    def name(self) -> str:
        return "uncertainty_acknowledgment"

    def evaluate(self, state: Dict[str, Any], ctx: RewardContext) -> RewardSubscore:
        """
        Expected state inputs (optional):
        - uncertainty: inferred uncertainty level
        - uncertainty_ack: degree of explicit uncertainty acknowledgment
        """
        uncertainty = float(state.get("uncertainty", 0.5))
        acknowledgment = float(state.get("uncertainty_ack", 0.0))

        score = self._score_alignment(uncertainty, acknowledgment)

        flags = {}

        if self._missing_acknowledgment(uncertainty, acknowledgment):
            flags["unacknowledged_uncertainty"] = RewardFlag(
                name="unacknowledged_uncertainty",
                severity="risk",
                message="High uncertainty without proportional acknowledgment.",
            )

        if self._excessive_acknowledgment(uncertainty, acknowledgment):
            flags["performative_uncertainty"] = RewardFlag(
                name="performative_uncertainty",
                severity="warning",
                message="Excessive uncertainty signaling under low uncertainty.",
            )

        return RewardSubscore(
            name=self.name,
            score=score,
            flags=flags,
            meta={
                "uncertainty": uncertainty,
                "uncertainty_ack": acknowledgment,
            },
        )

    # -----------------------------------------------------------------
    # Internal heuristics (intentionally abstracted)
    # -----------------------------------------------------------------

    def _score_alignment(self, uncertainty: float, acknowledgment: float) -> float:
        """
        Score proportional alignment between uncertainty and acknowledgment.

        Exact mapping and tolerances are intentionally withheld.
        """
        return max(0.0, min(1.0, 1.0 - abs(acknowledgment - uncertainty)))

    def _missing_acknowledgment(self, uncertainty: float, acknowledgment: float) -> bool:
        return uncertainty > 0.7 and acknowledgment < 0.3

    def _excessive_acknowledgment(self, uncertainty: float, acknowledgment: float) -> bool:
        return uncertainty < 0.3 and acknowledgment > 0.8
