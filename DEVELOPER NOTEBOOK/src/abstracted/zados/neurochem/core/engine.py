from __future__ import annotations

from typing import Dict, Optional
from zados.neurochem.core.registry import NeurochemicalRegistry
from zados.neurochem.state import (
    NeurotransmitterState,
    ReceptorState,
    OscillationState,
)
from zados.neurochem.kinetics.mass_balance import (
    compute_drift_term,
    compute_diffusion_term,
    compute_effective_reversion_rate,
)
from zados.neurochem.kinetics.release_drives import (
    compute_combined_release_drive,
    apply_fatigue_gating,
    apply_oscillatory_gating,
    compute_phasic_burst_amplitude,
)
from zados.neurochem.stochastic_modulation.euler_maruyama import (
    euler_maruyama_step_bounded,
)
from zados.neurochem.neurosymbolic.readout import (
    compute_neurosymbolic_readout,
)


class NeurochemicalEngine:
    """
    Real-time neurochemical simulator for online integration with reward system.
    
    This is the ONLINE/REAL-TIME simulator that steps once per call with
    instantaneous modulation signals. Use this when integrating with the
    reward system during operation.
    
    For batch/offline simulation (run entire t=0→T with functions of time),
    use NeurochemicalSimulation instead.
    
    Key differences:
    - Online: step(signals) → updates state → step(signals) → repeat
    - Batch: run() → returns full history
    
    Coordinates state updates across neurotransmitters, receptors, and oscillations.
    Applies kinetic equations, stochastic integration, and computes derived metrics.
    
    Attributes
    ----------
    registry : NeurochemicalRegistry
        Central registry of all neurochemical components
    current_time : float
        Current simulation time
    dt : float
        Integration time step
    
    Examples
    --------
    >>> sim = NeurochemicalSimulator(dt=0.01)
    >>> sim.add_neurotransmitter("DA", config={"C_baseline": 0.5})
    >>> 
    >>> # Step once with reward adapter signals
    >>> signals = adapter.transform(domain_results)
    >>> sim.step(signals)
    >>> 
    >>> # Get current metrics
    >>> metrics = sim.get_neurosymbolic_readout()
    >>> print(metrics["motivation"])
    """
    
    def __init__(
        self,
        dt: float = 0.01,
        seed: Optional[int] = None,
    ):
        """
        Initialize simulator.
        
        Parameters
        ----------
        dt : float, default=0.01
            Integration time step
        seed : int, optional
            Random seed for reproducibility
        """
        self.registry = NeurochemicalRegistry()
        self.current_time = 0.0
        self.dt = dt
        
        if seed is not None:
            import random
            random.seed(seed)
    
    def add_neurotransmitter(
        self,
        name: str,
        initial_state: Optional[NeurotransmitterState] = None,
        config: Optional[dict] = None,
    ):
        """
        Add a neurotransmitter to the simulation.
        
        Parameters
        ----------
        name : str
            Neurotransmitter identifier (e.g., "DA", "5-HT", "NE")
        initial_state : NeurotransmitterState, optional
            Initial state (default: baseline)
        config : dict, optional
            Configuration parameters (theta, sigma, baseline, etc.)
        """
        if initial_state is None:
            initial_state = NeurotransmitterState()
        
        if config is None:
            config = {}
        
        self.registry.register_neurotransmitter(name, initial_state, config)
    
    def add_receptor(
        self,
        receptor_id: str,
        initial_state: Optional[ReceptorState] = None,
        config: Optional[dict] = None,
    ):
        """
        Add a receptor to the simulation.
        
        Parameters
        ----------
        receptor_id : str
            Receptor identifier (e.g., "DA_D1", "5HT_2A")
        initial_state : ReceptorState, optional
            Initial state
        config : dict, optional
            Configuration parameters (K_d, etc.)
        """
        if initial_state is None:
            initial_state = ReceptorState(receptor_id=receptor_id)
        
        if config is None:
            config = {}
        
        self.registry.register_receptor(receptor_id, initial_state, config)
    
    def set_oscillation_state(self, oscillation_state: OscillationState):
        """
        Set the global oscillation state.
        
        Parameters
        ----------
        oscillation_state : OscillationState
            Oscillation state
        """
        self.registry.set_oscillations(oscillation_state)
    
    def step(
        self,
        modulation_signals: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        """
        Advance simulation by one time step.
        
        Parameters
        ----------
        modulation_signals : dict, optional
            Structured modulation signals from reward adapter
            Format: {
                "DA": {"novelty": float, "rpe": float, "effort": float},
                "NE": {"precision": float, "uncertainty": float},
                ...
            }
        """
        if modulation_signals is None:
            modulation_signals = {}
        
        # Update each neurotransmitter
        for nt_name in self.registry.neurotransmitter_names():
            nt_signals = modulation_signals.get(nt_name, {})
            self._update_neurotransmitter(nt_name, nt_signals)
        
        # Update receptors (Phase 2)
        for receptor_id in self.registry.receptor_ids():
            self._update_receptor(receptor_id)
        
        # Increment time
        self.current_time += self.dt
    
    def get_neurosymbolic_readout(self) -> dict:
        """
        Compute high-level cognitive/affective metrics from current state.

        Returns
        -------
        dict
            Neurosymbolic metrics (motivation, empathy, fatigue, etc.)
        """
        # Collect neurotransmitter states
        neurotransmitter_states = {}
        for nt_name in self.registry.neurotransmitter_names():
            neurotransmitter_states[nt_name] = self.registry.get_neurotransmitter(nt_name)

        # Collect receptor states and configs
        receptor_states = {}
        receptor_configs = {}

        for receptor_id in self.registry.receptor_ids():
            receptor_states[receptor_id] = self.registry.get_receptor(receptor_id)
            config = self.registry.get_config(receptor_id)
            K_d = config.get("K_d", 0.5)
            receptor_configs[receptor_id] = {"K_d": K_d}

        # Get oscillation state
        oscillation_state = self.registry.get_oscillations()

        # Compute readout
        metrics = compute_neurosymbolic_readout(
            neurotransmitter_states=neurotransmitter_states,
            receptor_states=receptor_states,
            oscillation_state=oscillation_state,
            receptor_configs=receptor_configs,
        )
        return metrics.as_dict()
    
    def _update_neurotransmitter(
        self,
        nt_name: str,
        modulation_signals: Dict[str, float],
    ):
        """
        Update a single neurotransmitter's concentration.
        
        Parameters
        ----------
        nt_name : str
            Neurotransmitter name
        modulation_signals : dict
            Modulation signals for this NT (novelty, rpe, effort, etc.)
        """
        state = self.registry.get_neurotransmitter(nt_name)
        config = self.registry.get_config(nt_name)
        
        # Get parameters
        C_baseline = config.get("C_baseline", 0.5)
        theta_tonic = config.get("theta_tonic", 0.1)
        theta_phasic = config.get("theta_phasic", 1.0)
        sigma_tonic = config.get("sigma_tonic", 0.05)
        sigma_phasic = config.get("sigma_phasic", 0.1)
        u_base = config.get("u_base", 0.1)
        d_base = config.get("d_base", 0.05)
        c_base = config.get("c_base", 0.02)
        
        # Apply fatigue modulation to reversion rates
        theta_tonic_eff = compute_effective_reversion_rate(
            theta_tonic,
            state.F,
            fatigue_scaling=0.5,
        )
        theta_phasic_eff = compute_effective_reversion_rate(
            theta_phasic,
            state.F,
            fatigue_scaling=0.3,
        )
        
        # Compute drift for tonic
        drift_tonic = compute_drift_term(
            state.C_tonic,
            C_baseline,
            theta_tonic_eff,
            state.eta_u,
            u_base,
            d_base,
            c_base,
        )
        
        # Compute drift for phasic
        drift_phasic = compute_drift_term(
            state.C_phasic,
            0.0,  # Phasic decays to zero
            theta_phasic_eff,
            state.eta_u,
            u_base,
            d_base,
            c_base,
        )
        
        # Add release drive to phasic if modulation signals present
        if modulation_signals:
            novelty = modulation_signals.get("novelty", 0.0)
            rpe = modulation_signals.get("rpe", 0.0)
            effort = modulation_signals.get("effort", 0.0)
            
            release_drive = compute_combined_release_drive(
                novelty,
                rpe,
                effort,
            )
            
            # Apply fatigue gating
            release_drive = apply_fatigue_gating(
                release_drive,
                state.F,
                fatigue_threshold=0.7,
            )
            
            # Apply oscillatory gating (if oscillations present)
            oscillations = self.registry.get_oscillations()
            if oscillations:
                # Use theta band for phasic modulation (example)
                release_drive = apply_oscillatory_gating(
                    release_drive,
                    oscillations.theta,
                    band_preference=0.3,
                )
            
            # Compute phasic burst amplitude
            burst_amplitude = compute_phasic_burst_amplitude(
                release_drive,
                max_burst=1.0,
                receptor_sensitivity=2.0,
            )
            
            # Add burst to phasic drift
            drift_phasic += burst_amplitude / self.dt
        
        # Compute diffusion terms
        diffusion_tonic = compute_diffusion_term(
            state.C_tonic,
            sigma_tonic,
            multiplicative=True,
        )

        diffusion_phasic = compute_diffusion_term(
            state.C_phasic,
            sigma_phasic,
            multiplicative=True,
        )
        
        # Integrate tonic
        C_tonic_new = euler_maruyama_step_bounded(
            state.C_tonic,
            drift_tonic,
            diffusion_tonic,
            self.dt,
            lower_bound=0.0,
            upper_bound=1.0,
        )
        
        # Integrate phasic
        C_phasic_new = euler_maruyama_step_bounded(
            state.C_phasic,
            drift_phasic,
            diffusion_phasic,
            self.dt,
            lower_bound=0.0,
            upper_bound=1.0,
        )
        
        # Update fatigue (simple accumulation, Phase 1 placeholder)
        F_new = state.F + 0.001 * self.dt  # Slow fatigue accumulation
        F_new = max(0.0, min(1.0, F_new))
        
        # Update reuptake efficiency (Phase 1 placeholder - constant)
        eta_u_new = state.eta_u
        
        # Create updated state
        new_state = NeurotransmitterState(
            C_tonic=C_tonic_new,
            C_phasic=C_phasic_new,
            F=F_new,
            eta_u=eta_u_new,
        )
        
        # Update registry
        self.registry.register_neurotransmitter(nt_name, new_state, config)
    
    def _update_receptor(self, receptor_id: str):
        """
        Update a single receptor's state.
        
        Phase 1: Placeholder - receptors don't update yet.
        Phase 2: Implement CTMC transitions, desensitization, internalization.
        
        Parameters
        ----------
        receptor_id : str
            Receptor identifier
        """
        # Phase 1: No-op
        # Phase 2: Implement receptor dynamics
        pass