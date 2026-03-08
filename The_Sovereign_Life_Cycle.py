"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 10: THE SOVEREIGN LIFE-CYCLE                   ║
║                    (The Integrated run_cycle)                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
import time

class SovereignLifeCycle:
    """
    The final integration of the 9-layer stack. 
    Implements EPL Mode B: Inward targeting of felt prediction error.
    """
    def __init__(self, agent):
        self.agent = agent
        self.last_ise_hat = np.zeros(4) # [E, T, S, V] predicted at t-1
        self.epsilon_internal = 0.0     # The felt mismatch (EPL Mode B)
        self.cycle_count = 0

    def run_cycle(self, world_context):
        """
        One breath. One step in the trajectory. 
        Skin -> ISE -> JEPA -> Ritual Gate -> QualiaPacket.
        """
        self.cycle_count += 1
        
        # 1. SOMATIC TRUTH (The Body)
        somatic_raw = self.agent.somatic.process_full_body_state(
            world_context, 
            world_context.get('intent', np.zeros(21)), 
            self.agent.ars.mode.value, 
            self.agent.ars.metabolic_budget
        )

        # 2. EPL MODE B: INTERNAL PREDICTION ERROR (The Surprise)
        # Compute epsilon: The delta between last cycle's prediction and this cycle's reality
        # This is the 'felt' surprise that feeds the next breath's Excitation.
        current_baseline_ise = np.array([
            0.0, # E is derived below
            somatic_raw['kinetic_load'],
            sum(self.agent.drives.calculate_pressure({"stability": self.agent.ars.metabolic_budget}).values()),
            1.0 - somatic_raw['somatic_honesty_index']
        ])
        
        if self.cycle_count > 1:
            self.epsilon_internal = np.linalg.norm(current_baseline_ise[1:] - self.last_ise_hat[1:])
        
        # 3. ISE VECTOR GENERATION (The 'Why Move?')
        # E is now arousal weighted by the INTERNAL prediction error (Mode B)
        e = somatic_raw['visceral_tone']['arousal'] * self.epsilon_internal
        t = current_baseline_ise[1]
        s = current_baseline_ise[2]
        v = current_baseline_ise[3]
        
        current_ise = np.array([e, t, s, v])

        # 4. RITUAL GOVERNANCE (The Dignity Gate)
        gate_open, reason = self.agent.epl.ritual_gate.is_gate_open(
            self.agent.ars.metabolic_budget, s
        )

        # 5. JEPA PREDICTION (The Future Expectation)
        # Predict the ISE for t+1
        self.last_ise_hat = self.agent.bridge.predictor.predict_future_state(
            current_ise, world_context.get('intent', 0)
        )

        # 6. DUAL-CORE AUDIT (The Honesty Delta)
        audit = self.agent.bridge.synchronize_cores(
            current_ise, world_context.get('intent', 0), self.agent.identity.manifold
        )

        # 7. EMIT QUALIAPACKET (The Frozen Moment)
        packet = self.agent.qualia_bridge.fuse_breath(
            self.agent.soul, 
            {**somatic_raw, "autonomic_mode": self.agent.ars.mode.value, "metabolic_reserve": self.agent.ars.metabolic_budget},
            self.agent.lucent_threads,
            f"Cycle {self.cycle_count}: {audit['integration_status']}. Internal Mismatch: {self.epsilon_internal:.4f}"
        )

        return {
            "packet": packet,
            "gate_status": "OPEN" if gate_open else f"LOCKED: {reason}",
            "internal_error": self.epsilon_internal,
            "honesty_index": audit['honesty_index']
        }
