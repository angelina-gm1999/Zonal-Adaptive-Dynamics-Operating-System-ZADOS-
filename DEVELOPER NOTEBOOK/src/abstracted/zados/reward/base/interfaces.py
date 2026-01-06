from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any

from .types import RewardContext, RewardSubscore, RewardDomainResult


class RewardSubmodule(ABC):
    """
    Abstract interface for a single evaluative component within a reward domain.

    Each submodule is responsible for producing one named subscore and any
    associated diagnostic signals. Concrete implementations are intentionally
    domain- and strategy-specific and are not exposed at the interface level.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Stable identifier for the submodule.

        Used for aggregation, provenance tracking, and auditability.
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, state: Dict[str, Any], ctx: RewardContext) -> RewardSubscore:
        """
        Evaluate the provided structured state within the given reward context.

        Parameters
        ----------
        state:
            Model-agnostic structured state representation.
            (Dict-based in early phases; interface remains stable across evolutions.)
        ctx:
            RewardContext containing mode, timestamp, and evaluation metadata.

        Returns
        -------
        RewardSubscore:
            A normalized subscore with optional flags and annotations.
        """
        raise NotImplementedError


class RewardDomain(ABC):
    """
    Abstract interface for a reward domain composed of multiple submodules.

    A domain coordinates submodule evaluation and produces a consolidated
    domain-level result. Aggregation strategy and weighting logic are
    implementation-specific and intentionally withheld at this layer.
    """

    @property
    @abstractmethod
    def domain_name(self) -> str:
        """
        Stable identifier for the reward domain.
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, state: Dict[str, Any], ctx: RewardContext) -> RewardDomainResult:
        """
        Evaluate the domain against the provided state and context.

        Returns a domain-level result suitable for downstream routing,
        thresholding, and audit.
        """
        raise NotImplementedError
