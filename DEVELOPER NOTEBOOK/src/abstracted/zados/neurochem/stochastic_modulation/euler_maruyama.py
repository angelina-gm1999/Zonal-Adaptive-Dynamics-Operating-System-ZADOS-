from __future__ import annotations

from typing import Callable, Optional
import math
import random


def euler_maruyama_step(
    X: float,
    drift: float,
    diffusion: float,
    dt: float,
    dW: Optional[float] = None,
) -> float:
    """
    Single Euler-Maruyama step for SDE integration.
    
    X(t+dt) = X(t) + μ(X,t)·dt + σ(X,t)·dW
    
    where dW ~ N(0, √dt) is Brownian increment.
    
    Parameters
    ----------
    X : float
        Current state
    drift : float
        Drift term μ(X,t)
    diffusion : float
        Diffusion term σ(X,t)
    dt : float
        Time step
    dW : float, optional
        Brownian increment. If None, generated as N(0, √dt)
        
    Returns
    -------
    float
        Next state X(t+dt)
    """
    if dW is None:
        dW = random.gauss(0.0, math.sqrt(dt))
    
    return X + drift * dt + diffusion * dW


def euler_maruyama_step_bounded(
    X: float,
    drift: float,
    diffusion: float,
    dt: float,
    lower_bound: float = 0.0,
    upper_bound: float = 1.0,
    dW: Optional[float] = None,
    reflection: bool = False,
) -> float:
    """
    Bounded Euler-Maruyama step with reflecting or absorbing boundaries.
    
    Parameters
    ----------
    X : float
        Current state
    drift : float
        Drift term
    diffusion : float
        Diffusion term
    dt : float
        Time step
    lower_bound : float, default=0.0
        Lower boundary
    upper_bound : float, default=1.0
        Upper boundary
    dW : float, optional
        Brownian increment
    reflection : bool, default=False
        If True, reflect at boundaries; if False, clamp
        
    Returns
    -------
    float
        Bounded next state
    """
    X_next = euler_maruyama_step(X, drift, diffusion, dt, dW)
    
    if reflection:
        # Reflecting boundaries
        while X_next < lower_bound or X_next > upper_bound:
            if X_next < lower_bound:
                X_next = 2 * lower_bound - X_next
            if X_next > upper_bound:
                X_next = 2 * upper_bound - X_next
    else:
        # Absorbing boundaries (clamp)
        X_next = max(lower_bound, min(upper_bound, X_next))
    
    return X_next


def integrate_sde(
    X0: float,
    drift_fn: Callable[[float, float], float],
    diffusion_fn: Callable[[float, float], float],
    t0: float,
    t_final: float,
    dt: float,
    lower_bound: float = 0.0,
    upper_bound: float = 1.0,
    reflection: bool = False,
    seed: Optional[int] = None,
) -> tuple[list[float], list[float]]:
    """
    Integrate an SDE from t0 to t_final using Euler-Maruyama.
    
    dX = μ(X,t)dt + σ(X,t)dW
    
    Parameters
    ----------
    X0 : float
        Initial state
    drift_fn : callable
        Drift function μ(X, t)
    diffusion_fn : callable
        Diffusion function σ(X, t)
    t0 : float
        Start time
    t_final : float
        End time
    dt : float
        Time step
    lower_bound : float, default=0.0
        Lower bound for state
    upper_bound : float, default=1.0
        Upper bound for state
    reflection : bool, default=False
        Use reflecting boundaries
    seed : int, optional
        Random seed for reproducibility
        
    Returns
    -------
    tuple[list[float], list[float]]
        (time_points, state_trajectory)
    """
    if seed is not None:
        random.seed(seed)
    
    time_points = []
    trajectory = []
    
    t = t0
    X = X0
    
    while t <= t_final:
        time_points.append(t)
        trajectory.append(X)
        
        if t >= t_final:
            break
        
        # Compute drift and diffusion at current state
        drift = drift_fn(X, t)
        diffusion = diffusion_fn(X, t)
        
        # Take bounded EM step
        X = euler_maruyama_step_bounded(
            X, drift, diffusion, dt,
            lower_bound, upper_bound,
            reflection=reflection,
        )
        
        t += dt
    
    return time_points, trajectory


def adaptive_step_euler_maruyama(
    X: float,
    drift: float,
    diffusion: float,
    dt: float,
    tolerance: float = 1e-3,
    min_dt: float = 1e-6,
    max_dt: float = 1.0,
    dW: Optional[float] = None,
) -> tuple[float, float]:
    """
    Adaptive time-stepping Euler-Maruyama.
    
    Adjusts step size based on local error estimate.
    
    Parameters
    ----------
    X : float
        Current state
    drift : float
        Drift term
    diffusion : float
        Diffusion term
    dt : float
        Proposed time step
    tolerance : float, default=1e-3
        Error tolerance
    min_dt : float, default=1e-6
        Minimum time step
    max_dt : float, default=1.0
        Maximum time step
    dW : float, optional
        Brownian increment
        
    Returns
    -------
    tuple[float, float]
        (next_state, accepted_dt)
    """
    # Generate noise if not provided
    if dW is None:
        dW = random.gauss(0.0, math.sqrt(dt))
    
    # Full step
    X_full = euler_maruyama_step(X, drift, diffusion, dt, dW)
    
    # Two half steps (for error estimation)
    dW_half1 = dW / math.sqrt(2.0)
    dW_half2 = dW / math.sqrt(2.0)
    
    X_half1 = euler_maruyama_step(X, drift, diffusion, dt/2, dW_half1)
    X_half2 = euler_maruyama_step(X_half1, drift, diffusion, dt/2, dW_half2)
    
    # Local error estimate
    error = abs(X_full - X_half2)
    
    # Adjust step size
    if error < tolerance:
        # Accept step, potentially increase dt
        dt_new = min(max_dt, dt * 1.5)
        return X_full, dt_new
    else:
        # Reject step, decrease dt
        dt_new = max(min_dt, dt * 0.5)
        # Retry with smaller step (recursive)
        return adaptive_step_euler_maruyama(
            X, drift, diffusion, dt_new,
            tolerance, min_dt, max_dt,
        )


def generate_brownian_increments(
    n_steps: int,
    dt: float,
    seed: Optional[int] = None,
) -> list[float]:
    """
    Generate a sequence of Brownian increments.
    
    dW_i ~ N(0, √dt)
    
    Parameters
    ----------
    n_steps : int
        Number of increments
    dt : float
        Time step
    seed : int, optional
        Random seed
        
    Returns
    -------
    list[float]
        Brownian increments
    """
    if seed is not None:
        random.seed(seed)
    
    std = math.sqrt(dt)
    return [random.gauss(0.0, std) for _ in range(n_steps)]


def compute_local_truncation_error(
    diffusion: float,
    dt: float,
) -> float:
    """
    Estimate local truncation error for EM scheme.
    
    Error ≈ σ · √dt
    
    Parameters
    ----------
    diffusion : float
        Diffusion coefficient
    dt : float
        Time step
        
    Returns
    -------
    float
        Error estimate
    """
    return abs(diffusion) * math.sqrt(dt)


def check_stability_condition(
    drift: float,
    diffusion: float,
    dt: float,
    X: float,
) -> bool:
    """
    Check stability condition for explicit EM scheme.
    
    Roughly: dt · |μ/X| should be small, dt · |σ²/X²| should be small
    
    Parameters
    ----------
    drift : float
        Drift term
    diffusion : float
        Diffusion term
    dt : float
        Time step
    X : float
        Current state
        
    Returns
    -------
    bool
        True if stable
    """
    if X == 0.0:
        return True
    
    drift_stability = abs(drift * dt / X) < 0.5
    diffusion_stability = abs(diffusion**2 * dt / X**2) < 0.5
    
    return drift_stability and diffusion_stability