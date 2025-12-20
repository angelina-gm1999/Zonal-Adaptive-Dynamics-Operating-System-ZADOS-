Open Questions and Active Investigation Areas

    This document captures open questions, unresolved challenges, and areas of active investigation within ZA-DOS. These are not framed as deficiencies, but as known hard problems inherent to building regulated, modular cognitive systems.
    
    Documenting these explicitly is intended to prevent false confidence, preserve design flexibility, and support future iteration under controlled conditions.

Reward Drift and Long-Term Stability

  Open Question
    How to detect and correct subtle reward drift over long operational periods, especially when modulation and arbitration logic interact in non-obvious ways.
  
  Context
    Even with explicit reward modules and bounded control signals, slow drift can emerge through repeated arbitration patterns or skewed modulation distributions.
  
  Current Approach
    Reward contributions and modulation states are fully logged. Periodic analysis and replay are planned to identify systematic bias accumulation.

  Open Work
    Formal criteria for identifying unacceptable drift patterns without overconstraining adaptive behavior.

Arbitration Policy Sensitivity

  Open Question
    How sensitive global behavior is to changes in arbitration policy under edge cases.
  
  Context
    Explicit arbitration enables safety guarantees, but poorly tuned dominance rules could introduce rigidity or suppress legitimate exploration.
  
  Current Approach
    Arbitration logic is parameterized and isolated from reward computation. Multiple arbitration strategies can be tested without structural changes.
  
  Open Work
    Systematic stress-testing of arbitration policies across simulated conflict scenarios.

Neurochemical Modulation Calibration

  Open Question
    How to calibrate modulation ranges to balance responsiveness with stability across heterogeneous cognitive engines.
  
  Context
    The neurochemical layer abstracts behavioral control, but different engines may respond unevenly to the same modulation signals.
  
  Current Approach
    Bounded ranges, smooth update rules, and controlled noise are enforced. Engines are integrated incrementally to observe interaction effects.
  
  Open Work
    Developing engine-specific sensitivity profiles without breaking the abstraction boundary.

Memory Pruning and Long-Term Relevance

  Open Question
    How to determine which information should persist long-term without prematurely discarding data that later becomes relevant.
  
  Context
    Selective memory is necessary for interpretability and scalability, but relevance is often context-dependent and time-shifted.
  
  Current Approach
    Memory managers use importance, recurrence, and contextual relevance heuristics with conservative thresholds.
  
  Open Work
    Refining consolidation criteria and exploring delayed promotion mechanisms.

Integration of External Cognitive Frameworks

  Open Question
    How to integrate external cognitive frameworks without leaking their assumptions into core control logic.
  
  Context
    Frameworks such as symbolic planners or procedural reasoning systems bring strong priors that may conflict with internal arbitration or modulation.
  
  Current Approach
    External engines are treated as interchangeable tools routed through orchestration logic rather than embedded deeply.
  
  Open Work
    Defining interface contracts that preserve engine independence while allowing meaningful coordination.

Stochastic Exploration Boundaries

  Open Question
    How much stochasticity can be introduced before interpretability or auditability degrades.
  
  Context
    Stochastic modulation supports robustness testing and uncertainty exploration, but excessive randomness undermines traceability.
  
  Current Approach
    Stochastic components are isolated and logged. Deterministic constraints operate independently.
  
  Open Work
    Quantifying acceptable stochastic envelopes for different operational contexts.
  
Failure Mode Visibility

  Open Question
    How to ensure that failure modes remain legible rather than silently degrading performance.
  
  Context
    Complex systems often fail gradually rather than catastrophically. Without explicit signals, such degradation can go unnoticed.
  
  Current Approach
    Monitoring hooks and anomaly detection are planned at control and arbitration layers.
  
  Open Work
    Defining failure signatures that are both sensitive and actionable.

Human Interpretability at Scale
  
  Open Question
    How to preserve interpretability as the number of engines, reward modules, and memory components increases.
  
  Context
    Even fully logged systems can become cognitively opaque to human reviewers as scale grows.
  
  Current Approach
    Layer boundaries and explicit interfaces are enforced from the outset.
  
  Open Work
    Developing visualization or summarization tools that compress system state without hiding critical dependencies.
