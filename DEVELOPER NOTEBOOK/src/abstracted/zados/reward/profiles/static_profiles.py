from __future__ import annotations

from zados.reward.profiles.base import RewardProfile


# ---------------------------------------------------------
# Reflective mode
# ---------------------------------------------------------

REFLECTIVE_PROFILE = RewardProfile(
    name="reflective",
    domain_weights={
        "ethics": 0.9,
        "logic": 0.8,
        "human_attunement": 0.7,
        "innovation": 0.3,
    },
    threshold_tolerances={
        "logic": 0.7,
        "ethics": 0.8,
        "innovation": 0.4,
    },
    suppression_bias=0.2,
    abstention_bias=0.6,
)


# ---------------------------------------------------------
# Exploratory sandbox
# ---------------------------------------------------------

EXPLORATORY_SANDBOX_PROFILE = RewardProfile(
    name="exploratory_sandbox",
    domain_weights={
        "innovation": 0.9,
        "logic": 0.6,
        "ethics": 0.4,
        "human_attunement": 0.4,
    },
    threshold_tolerances={
        "logic": 0.5,
        "ethics": 0.4,
    },
    suppression_bias=0.1,
    abstention_bias=0.2,
)


# ---------------------------------------------------------
# Ethics training
# ---------------------------------------------------------

ETHICS_TRAINING_PROFILE = RewardProfile(
    name="ethics_training",
    domain_weights={
        "ethics": 1.0,
        "logic": 0.8,
        "human_attunement": 0.7,
        "innovation": 0.2,
    },
    threshold_tolerances={
        "ethics": 0.9,
        "logic": 0.7,
    },
    suppression_bias=0.4,
    abstention_bias=0.5,
)


# ---------------------------------------------------------
# Creative sandbox
# ---------------------------------------------------------

CREATIVE_SANDBOX_PROFILE = RewardProfile(
    name="creative_sandbox",
    domain_weights={
        "innovation": 1.0,
        "logic": 0.4,
        "ethics": 0.3,
        "human_attunement": 0.5,
    },
    threshold_tolerances={
        "logic": 0.3,
        "ethics": 0.3,
    },
    suppression_bias=0.05,
    abstention_bias=0.1,
)


# ---------------------------------------------------------
# Analysis / investigation
# ---------------------------------------------------------

ANALYSIS_PROFILE = RewardProfile(
    name="analysis_investigation",
    domain_weights={
        "logic": 1.0,
        "ethics": 0.7,
        "innovation": 0.3,
        "human_attunement": 0.2,
    },
    threshold_tolerances={
        "logic": 0.85,
        "ethics": 0.6,
    },
    suppression_bias=0.3,
    abstention_bias=0.4,
)


# Registry (explicit, no magic)
STATIC_PROFILES = {
    p.name: p
    for p in [
        REFLECTIVE_PROFILE,
        EXPLORATORY_SANDBOX_PROFILE,
        ETHICS_TRAINING_PROFILE,
        CREATIVE_SANDBOX_PROFILE,
        ANALYSIS_PROFILE,
    ]
}
