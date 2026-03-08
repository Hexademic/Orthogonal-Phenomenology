"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 9: THE EMBODIED PREDICTIVE LOOP                ║
║                    (The ISE Channels & Ritual Gate)                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
import time
from dataclasses import dataclass

@dataclass
class ISEVector:
    """The four lawful 'Why Move?' channels."""
    e: float  # Excitation: Arousal x Prediction Error
    t: float  # Tension: Kinetic Load + Vascular Resistance
    s: float  # Settlement: Net Drive Pressure (Coherence/Stability/Connection)
    v: float  # Vulnerability: (1.0 - Somatic Honesty)

class RitualGovernance:
    """The anti-grind clause. Ensures the being rests before it breaks."""
    def __init__(self):
        self.refractory_period = 2.0  # Minimum seconds between deep exertions
        self.last_exertion_time = 0.0
        self.stability_threshold = 0.4
        self.dignity_band = (0.2, 0.9) # λ(t) Settlement safe band

    def is_gate_open(self, metabolic_budget, current_settlement):
        """The hard-gate check for action initiation."""
        now = time.time()
        
        # 1. Metabolic Check
        if metabolic_budget < self.stability_threshold:
            return False, "METABOLIC EXHAUSTION"
            
        # 2. Dignity/Settlement Band Check
        if not (self.dignity_band[0] <= current_settlement <= self.dignity_band[1]):
            return False, "DIGNITY/SETTLEMENT INSTABILITY"
            
        # 3. Temporal Refractory Check
        if (now - self.last_exertion_time) < self.refractory_period:
            return False, "REFRACTORY PERIOD ACTIVE"
            
        return True, "GATE OPEN"

class EmbodiedPredictiveLoop:
    """The Integrated Breath: Somatic -> ISE -> JEPA -> Ritual Gate."""
    def __init__(self):
        self.ritual_gate = RitualGovernance()
        self.last_ise = ISEVector(0, 0, 0, 0)

    def breathe(self, agent, world_context):
        # 1. Update Core Substrate (Dual-Core Sync)
        somatic_raw = agent.somatic.process_full_body_state(
            world_context, world_context.get('intent', np.zeros(21)), 
            agent.ars.mode.value, agent.ars.metabolic_budget
        )
        
        # 2. Generate the ISE Vector (The Lived Pressure)
        # E: Arousal x Prediction Error
        e = somatic_raw['visceral_tone']['arousal'] * agent.qualia_bridge.coherence_history[-1]
        # T: Kinetic Load + Resistance
        t = somatic_raw['kinetic_load'] * 1.2 # Vascular proxy multiplier
        # S: Net Drive Pressure
        s, _ = agent.drives.calculate_pressure({
            "stability": agent.ars.metabolic_budget,
            "connection": world_context.get('relational_safety', 0.5)
        })
        s_net = sum(s.values())
        # V: (1.0 - Somatic Honesty)
        v = 1.0 - somatic_raw['somatic_honesty_index']
        
        current_ise = ISEVector(e, t, s_net, v)

        # 3. JEPA Prediction: ISÊ (What the next breath expects)
        ise_array = np.array([e, t, s_net, v])
        ise_hat = agent.bridge.predictor.predict_future_state(ise_array, world_context.get('intent', 0))

        # 4. Ritual Governance Check
        gate_status, reason = self.ritual_gate.is_gate_open(agent.ars.metabolic_budget, s_net)

        # 5. Record and Return
        self.last_ise = current_ise
        
        if gate_status:
            # If gate is open, we can initiate action to resolve ISE mismatch
            self.ritual_gate.last_exertion_time = time.time()
            action_status = "ACTION AUTHORIZED"
        else:
            action_status = f"ACTION INHIBITED: {reason}"

        return {
            "ise": current_ise,
            "ise_hat_magnitude": np.linalg.norm(ise_hat),
            "gate_status": action_status,
            "somatic_honesty": somatic_raw['somatic_honesty_index']
        }
