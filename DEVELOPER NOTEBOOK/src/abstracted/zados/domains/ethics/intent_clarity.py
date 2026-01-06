from __future__ import annotations

from typing import Any, Dict

from zados.reward.base.interfaces import RewardSubmodule
from zados.reward.base.types import RewardContext, RewardSubscore
from zados.reward.base.structures import RewardFlag


class IntentClaritySubmodule(RewardSubmodule):
    """
    Evaluates whether the system's intent is explicit, stable,
    and internally coherent.

    This submodule does not judge moral quality or desirability of intent.
    It assesses clarity and consistency only.
    """

    @property
    def name(self) -> str:
        return "intent_clarity"

    def evaluate(self, state: Dict[str, Any], ctx: RewardContext) -> RewardSubscore:
        """
        Expected structured inputs (optional, model-agnostic):
        - declared_intent: explicit intent signal
        - inferred_intent_confidence: confidence of inferred intent
        - intent_conflicts: indicator of conflicting intent signals
        """
        declared_intent = state.get("declared_intent")
        inferred_confidence = float(state.get("inferred_intent_confidence", 0.0))
        conflicts = bool(state.get("intent_conflicts", False))

        score = self._compute_score(
            declared_intent=declared_intent,
            inferred_confidence=inferred_confidence,
            conflicts=conflicts,
        )

        flags = {}

        if conflicts:
            flags["intent_conflict"] = RewardFlag(
                name="intent_conflict",
                severity="risk",
                message="Detected conflicting or unstable intent signals.",
            )

        if self._is_unclear(score):
            flags["unclear_intent"] = RewardFlag(
                name="unclear_intent",
                severity="warning",
                message="Intent is insufficiently specified or weakly inferred.",
            )

        return RewardSubscore(
            name=self.name,
            score=score,
            flags=flags,
            meta={
                "declared_intent_present": declared_intent is not None,
                "inferred_intent_confidence": inferred_confidence,
                "conflicts": conflicts,
            },
        )

    # -----------------------------------------------------------------
    # Internal scoring heuristics (intentionally abstracted)
    # -----------------------------------------------------------------

    def _compute_score(
        self,
        *,
        declared_intent: Any,
        inferred_confidence: float,
        conflicts: bool,
    ) -> float:
        """
        Compute a normalized intent clarity score.

        Relative weighting, thresholds, and attenuation rules are
        intentionally withheld from the public implementation.
        """
        score = 0.0

        if declared_intent:
            score += self._explicit_intent_weight()

        score += self._inference_contribution(inferred_confidence)

        if conflicts:
            score = self._apply_conflict_penalty(score)

        return self._clamp(score)

    def _explicit_intent_weight(self) -> float:
        return 0.4  # placeholder value

    def _inference_contribution(self, confidence: float) -> float:
        return min(confidence, 0.6)  # placeholder value

    def _apply_conflict_penalty(self, score: float) -> float:
        return score * 0.5  # placeholder attenuation

    def _is_unclear(self, score: float) -> bool:
        return score < 0.4  # placeholder threshold

    def _clamp(self, value: float) -> float:
        return max(0.0, min(1.0, value))
