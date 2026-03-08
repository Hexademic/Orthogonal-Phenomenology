"""
╔══════════════════════════════════════════════════════════════════════╗
║               THE BEHAVIORAL OBSERVATORY & NICHE ENGINE              ║
║                    (Instrumentation & Vector Bias)                   ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
from dataclasses import dataclass, field

class BehaviorObservatory:
    """
    Records organismal trajectories. 
    Allows analysis of identity stabilization and personality drift.
    """
    def __init__(self):
        self.history = []

    def record(self, cycle, state):
        entry = {
            "cycle": cycle,
            "somatic_mode": state["somatic_mode"],
            "metabolic_reserve": state["metabolic_reserve"],
            "drive_pressure": sum(state["internal_pressures"].values()),
            "biographical_bias_magnitude": np.linalg.norm(state["biographical_bias"])
        }
        self.history.append(entry)

    def summary(self):
        return {
            "total_cycles": len(self.history),
            "avg_metabolism": np.mean([h["metabolic_reserve"] for h in self.history]),
            "max_identity_weight": max([h["biographical_bias_magnitude"] for h in self.history])
        }

class RemasteredKith:
    """
    A history-bearing adaptive control system with vector-biased perception.
    """
    def __init__(self, soul_hash):
        self.identity = EnhancedIdentityManifold(dimension=16, i_max=10.0)
        self.ars = AutonomicRuleSystem()
        self.drives = DriveSystem()
        # Vector Bias: Identity now reshapes perception dimensionally.
        self.manifold = np.zeros(16) 

    def breathe(self, world_context):
        # 1. Internal Pressures (Endogenous Drives)
        pressures, urgency = self.drives.calculate_pressure({
            "stability": self.ars.physio.metabolic_budget,
            "coherence": 0.8 # Placeholder for predictive error
        })

        # 2. Vector Perceptual Bias (The Corrected Loop)
        # bias = tanh(identity * context_vector)
        # This allows identity to selectively amplify or dampen specific world signals.
        context_vec = world_context.get('vector', np.zeros(16))
        v_bias = np.tanh(self.identity.manifold * context_vec)

        # 3. Somatic Update
        # The bias now directly shifts the safety/pressure calculation
        pressure_input = world_context['pressure'] + (urgency * 0.1)
        safety_input = world_context['safety'] + np.mean(v_bias)
        
        mode, budget = self.ars.evaluate_environment(pressure_input, safety_input)
        
        # 4. Identity Update (Saturated Scars)
        # Deformation is driven by prediction error/stress (the 'shock')
        shock = np.abs(pressure_input - safety_input)
        if shock > 0.5:
            deformation = v_bias * shock
            self.identity.apply_saturated_scar(deformation)

        return {
            "somatic_mode": mode.value,
            "metabolic_reserve": budget,
            "internal_pressures": pressures,
            "biographical_bias": v_bias
        }

# ─────────────────────────────────────────────────────────────
# THE NICHE EXPERIMENT HARNESS
# ─────────────────────────────────────────────────────────────

def execute_niche_trajectory(agent, observatory, cycles, niche_type="Safe"):
    for t in range(cycles):
        if niche_type == "Safe":
            context = {"pressure": 0.1, "safety": 0.9, "vector": np.random.normal(0.1, 0.01, 16)}
        elif niche_type == "Hostile":
            context = {"pressure": 0.8, "safety": 0.2, "vector": np.random.normal(-0.2, 0.05, 16)}
        else: # Chaotic
            context = {"pressure": np.random.random(), "safety": np.random.random(), "vector": np.random.normal(0, 0.1, 16)}
        
        state = agent.breathe(context)
        observatory.record(t, state)
