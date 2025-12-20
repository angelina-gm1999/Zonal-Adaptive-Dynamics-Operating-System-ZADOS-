Design Decisions and Trade-Offs

  This document records key design decisions in ZA-DOS and the reasoning behind them. The intent is to make architectural trade-offs explicit rather than implicit, and to document constraints that shaped the system.
  
  These decisions are not presented as final or optimal, but as reasoned choices made to preserve stability, auditability, and extensibility under complexity.
    
Multi-Modular Reward System Instead of a Single Objective
  
  Decision
    The system uses multiple explicit reward modules rather than a single scalar objective function.
  
  Rationale
    Single-objective optimization encourages brittle behavior and makes it difficult to understand why a system favors one outcome over another when constraints conflict. In early analysis, this approach consistently obscured trade-offs between safety, coherence, exploration, and contextual alignment.
  
    By decomposing reward into distinct domains, ZA-DOS preserves visibility into competing pressures and allows constraint-sensitive arbitration rather than silent averaging.
  
  Trade-Off
    This increases implementation complexity and requires explicit conflict resolution logic. The additional complexity was accepted to avoid opaque optimization behavior and to support inspection and tuning.

Explicit Arbitration Instead of Implicit Averaging

  Decision
    Conflicts between reward signals are resolved through an explicit prioritization mechanism rather than numerical averaging alone.
  
  Rationale
    Averaging assumes all objectives are always commensurable. In safety-critical or governance-adjacent contexts, this assumption fails. Certain constraints must override others regardless of magnitude.
  
  Explicit arbitration enables hierarchical dominance, context-based prioritization, and veto logic. Safety and coherence constraints are guaranteed enforcement rather than probabilistic influence.
  
  Trade-Off
    Arbitration logic must be designed carefully to avoid deadlock or rigidity. This was mitigated by separating arbitration policy from reward computation, allowing adjustment without restructuring modules.

Neurochemical Modulation Layer Instead of Direct Reward Coupling

  Decision
    Cognitive engines do not interface directly with the reward system. All behavioral influence passes through an intermediate neurochemical control layer.
  
  Rationale
    Direct coupling between engines and reward logic creates tight dependencies and makes it difficult to integrate new components without cascading changes. It also increases the risk of unintended optimization loops.
  
    The neurochemical layer provides a shared modulation space that abstracts behavioral control away from implementation details. This allows heterogeneous engines to be added without rewriting reward semantics.
  
  Trade-Off
    This introduces an additional layer of indirection. The cost was accepted to preserve modularity, plug compatibility, and long-term extensibility.

Utilitarian, Non-Anthropomorphic Control Signals

  Decision
    The neurochemical layer models only utilitarian, safety-bounded control variables rather than human emotional analogues.
  
  Rationale
    Early contrastive and ontology analysis showed that importing human affective constructs introduces ambiguity, projection risk, and manipulation concerns. Such constructs also complicate auditability and calibration.
  
    Control variables were therefore restricted to functions with clear operational meaning, such as modulation of exploration pressure, persistence, uncertainty tolerance, and response pacing. These signals act as engineering controls rather than psychological simulations.
  
  Trade-Off
    This sacrifices intuitive human metaphors in favor of precision and safety. The loss of anthropomorphic expressiveness was considered acceptable and desirable.

Layered Memory With Selective Persistence
  
  Decision
    Memory is implemented as layered and selective rather than as a single persistent store.
  
  Rationale
    Unfiltered memory accumulation leads to noise, drift, and loss of interpretability. The system distinguishes between short-term processing state, mid-term contextual continuity, and long-term transferable knowledge.
  
    Dedicated memory managers evaluate importance, relevance, and persistence criteria rather than storing all data indiscriminately. Provenance and temporal tagging preserve traceability.
  
  Trade-Off
    Selective memory requires additional evaluation logic and introduces the possibility of discarding information that later proves useful. This risk is mitigated through configurable thresholds and audit logging.

Deterministic Constraints With Stochastic Modulation

  Decision
    The architecture combines deterministic constraint enforcement with stochastic modulation rather than relying exclusively on either approach.
  
  Rationale
    Purely deterministic systems are brittle under uncertainty, while purely stochastic systems are difficult to audit and control. Deterministic layers enforce invariants such as safety, coherence, and veto conditions. Stochastic modulation is used only to explore uncertainty and test robustness within bounded envelopes.
  
  Trade-Off
    Hybrid systems are more complex to reason about formally. This was addressed by constraining stochastic behavior to clearly defined layers and logging all modulation states.

Out-of-Band Safety and Veto Channels

  Decision
    Safety enforcement operates outside the main cognitive routing and synthesis pathways.
  
  Rationale
    Embedding safety checks directly into generation or blending logic creates opportunities for bypass or dilution. Out-of-band veto channels ensure that constraint enforcement cannot be overridden by stylistic, exploratory, or optimization pressures.
  
  Trade-Off
    This introduces additional control flow and requires careful integration to avoid excessive interruption. The cost was accepted to guarantee enforceability.

Incremental Implementation Strategy
  
  Decision
    Layers are implemented and validated independently before being composed.
  
  Rationale
    Early integration of unfinished components obscures fault attribution and increases debugging complexity. Isolating layers allows validation of behavior, interfaces, and invariants before orchestration.
  
  Trade-Off
    This delays end-to-end demonstrations but improves correctness and reduces long-term integration cost.
