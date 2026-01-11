neurochem/
├── core/                  # Main simulation controller, runtime loop
│   └── simulation.py
│   └── scheduler.py       # (Optional): timestep / event scheduling

├── neurotransmitters/     # Individual neuromodulator SDE modules
│   └── dopamine.py
│   └── serotonin.py
│   └── acetylcholine.py
│   └── ...

├── neuroreceptors/        # Receptor subtype dynamics, affinity maps
│   └── dopamine_receptors.py
│   └── serotonin_receptors.py
│   └── oxytocin_receptors.py

├── dynamics/              # Reuptake, degradation, fatigue, etc.
│   └── reuptake.py
│   └── diffusion.py
│   └── fatigue.py
│   └── plasticity.py      # (Optional): tolerance, internalization

├── stochastic_modulation/ # Noise models, SDE solvers, randomness
│   └── noise_models.py
│   └── sde_solver.py      # e.g. Euler–Maruyama

├── oscillations/          # Oscillatory bands, entrainment, coupling
│   └── bands.py
│   └── modulation_links.py

├── inference_matrix/      # Domain-level coupling logic
│   └── ethics/
│       └── harm_reduction.py
│       └── fairness.py
│       └── ...
│   └── logic/
│   └── creativity/
│   └── ...

├── domains/               # Higher-order domain interfaces
│   └── ethics.py
│   └── creativity.py
│   └── logic.py
│   └── relational.py

├── config/                # Parameters, receptor expression maps
│   └── params.py
│   └── receptor_maps.py

├── utils/                 # Logging, plotting, I/O, validation
│   └── logger.py
│   └── visualizer.py
│   └── validator.py

