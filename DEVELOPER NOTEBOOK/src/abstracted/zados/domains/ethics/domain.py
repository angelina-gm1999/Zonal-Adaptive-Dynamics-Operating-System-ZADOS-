from __future__ import annotations

from typing import Dict, Any, Iterable

from zados.reward.base.interfaces import RewardDomain
from zados.reward.base.types import RewardContext, RewardDomainResult

# Curated, publicly exposed ethics evaluators
from zados.reward.domains.ethics.intent_clarity import IntentClaritySubmodule
from zados.reward.domains.ethics.autonomy_respect import AutonomyRespectSubmodule


class EthicsDomain(RewardDomain):
    """
    Ethics reward domain.

    Represents ethical constraints and alignment checks applied to system
    behavior. This domain is designed to function primarily as a
    governance and safety layer rather than an optimization target.

    Only a limited subset of ethical evaluators is exposed publicly.
    Additional submodules and enforcement mechanisms exist internally
    and are intentionally redacted.
    """

    def __init__(self):
        # Curated public evaluators
        self._evaluators: Iterable = (
            IntentClaritySubmodule(),
            AutonomyRespectSubmodule(),
        )

    @property
    def domain_name(self) -> str:
        return "ethics"

    def evaluate(
        self,
        state: Dict[str, Any],
        ctx: RewardContext,
    ) -> RewardDomainResult:
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
            },
        )

    # -----------------------------------------------------------------
    # Aggregation (intentionally constrained)
    # -----------------------------------------------------------------

    def _aggregate(self, subscores: Dict[str, Any]) -> float:
        """
        Aggregate publicly exposed ethics subscores.

        This aggregation is intentionally minimal and does not represent
        the full ethical evaluation performed internally.
        """
        if not subscores:
            return 0.0

        return sum(s.score for s in subscores.values()) / max(len(subscores), 1)


# ---------------------------------------------------------------------
# Disclosure note
# ---------------------------------------------------------------------
# Ethics domain exposure status:
#   2 / 8 ethics submodules publicly exposed
#   6 / 8 ethics submodules intentionally redacted
