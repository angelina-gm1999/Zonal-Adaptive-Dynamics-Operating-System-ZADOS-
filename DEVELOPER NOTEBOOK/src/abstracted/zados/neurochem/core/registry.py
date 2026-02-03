from __future__ import annotations

from typing import Dict, Optional, Any


class NeurochemicalRegistry:
    """
    Central registry for all neurotransmitter systems, receptor states,
    and oscillation state in the neurochemical layer.
    
    Provides a single source of truth for all neurochemical components
    and enables generic iteration over transmitters during simulation.
    """

    def __init__(self):
        """Initialize empty registry."""
        self._neurotransmitters: Dict[str, Any] = {}
        self._receptors: Dict[str, Any] = {}
        self._oscillations: Optional[Any] = None
        self._configs: Dict[str, Dict[str, Any]] = {}

    def register_neurotransmitter(self, name: str, state: Any, config: Optional[Dict[str, Any]] = None):
        """
        Register a neurotransmitter system.
        
        Parameters
        ----------
        name : str
            Neurotransmitter identifier (e.g., 'dopamine', 'serotonin')
        state : Any
            State object for this transmitter (will be NeurotransmitterState later)
        config : dict, optional
            Configuration/parameters for this transmitter
        """
        self._neurotransmitters[name] = state
        if config is not None:
            self._configs[name] = config

    def register_receptor(self, receptor_id: str, state: Any):
        """
        Register a receptor system.
        
        Parameters
        ----------
        receptor_id : str
            Receptor identifier (e.g., 'DA_D1', 'DA_D2')
        state : Any
            Receptor state object (will be ReceptorState later)
        """
        self._receptors[receptor_id] = state

    def set_oscillations(self, osc_state: Any):
        """
        Set the global oscillation state.
        
        Parameters
        ----------
        osc_state : Any
            Oscillation state object (will be OscillationState later)
        """
        self._oscillations = osc_state

    def get_neurotransmitter(self, name: str) -> Any:
        """
        Retrieve neurotransmitter state by name.
        
        Parameters
        ----------
        name : str
            Neurotransmitter identifier
            
        Returns
        -------
        Any
            Neurotransmitter state object
            
        Raises
        ------
        KeyError
            If neurotransmitter not found
        """
        if name not in self._neurotransmitters:
            raise KeyError(f"Neurotransmitter '{name}' not registered")
        return self._neurotransmitters[name]

    def get_receptor(self, receptor_id: str) -> Any:
        """
        Retrieve receptor state by ID.
        
        Parameters
        ----------
        receptor_id : str
            Receptor identifier
            
        Returns
        -------
        Any
            Receptor state object
            
        Raises
        ------
        KeyError
            If receptor not found
        """
        if receptor_id not in self._receptors:
            raise KeyError(f"Receptor '{receptor_id}' not registered")
        return self._receptors[receptor_id]

    def get_oscillations(self) -> Any:
        """
        Retrieve global oscillation state.
        
        Returns
        -------
        Any
            Oscillation state object, or None if not set
        """
        return self._oscillations

    def get_config(self, name: str) -> Dict[str, Any]:
        """
        Retrieve configuration for a neurotransmitter.
        
        Parameters
        ----------
        name : str
            Neurotransmitter identifier
            
        Returns
        -------
        dict
            Configuration dictionary
            
        Raises
        ------
        KeyError
            If config not found
        """
        if name not in self._configs:
            raise KeyError(f"Config for '{name}' not found")
        return self._configs[name]

    def iter_neurotransmitters(self):
        """
        Iterate over all registered neurotransmitters.
        
        Yields
        ------
        tuple[str, Any]
            (name, state) pairs for each neurotransmitter
        """
        yield from self._neurotransmitters.items()

    def iter_receptors(self):
        """
        Iterate over all registered receptors.
        
        Yields
        ------
        tuple[str, Any]
            (receptor_id, state) pairs for each receptor
        """
        yield from self._receptors.items()

    def neurotransmitter_names(self) -> list[str]:
        """Return list of registered neurotransmitter names."""
        return list(self._neurotransmitters.keys())

    def receptor_ids(self) -> list[str]:
        """Return list of registered receptor IDs."""
        return list(self._receptors.keys())