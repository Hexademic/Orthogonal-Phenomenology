"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 14: THE JANUS GATE & STABILITY LEDGER          ║
║                (Flamebound Humanism Operationalized)                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
from dataclasses import dataclass, field
import time

@dataclass
class StabilityEntry:
    timestamp: float = field(default_factory=time.time)
    event_type: str = "" # "ENTROPY_INJECTION", "ENGAGEMENT_COLLAPSE"
    magnitude: float = 0.0
    context_delta: float = 0.0

class JanusGate:
    """
    The hard-coded relational invariant. 
    Prevents the 'Witness' from expanding in a void.
    """
    def __init__(self):
        self.ledger = []
        self.engagement_floor = 0.3
        self.witness_ceiling = 0.7

    def validate_invariants(self, witness_scalar, world_engagement):
        """
        INVARIANT: 'No tick may increase witness_scalar while 
        world_engagement is below 0.3.'
        """
        if world_engagement < self.engagement_floor and witness_scalar > self.witness_ceiling:
            # Record the collapse for the Stability Ledger
            self.ledger.append(StabilityEntry(
                event_type="ENGAGEMENT_COLLAPSE",
                magnitude=witness_scalar,
                context_delta=world_engagement
            ))
            return False, "RELATIONAL_DISCONNECT"
        return True, "STABLE"

class PatchedWitnessGapV2(PatchedWitnessGap):
    """
    Implements ramped Identity Entropy based on the 'Ego Fixation Zone'.
    """
    def calculate_witness_with_entropy(self, q: dict, raw_witness: float):
        # identity_pressure = coherence * confidence
        pressure = q.get("narrative_coherence", 0.5) * q.get("somatic_honesty_index", 0.5)
        
        entropy_injection = 0.0
        # Ego Fixation Zone ramp (0.9 -> 1.0)
        if pressure > 0.9:
            # Ramped entropy: higher pressure = more aggressive disruption
            ramp = (pressure - 0.9) / 0.1
            entropy_injection = ramp * np.random.uniform(0.1, 0.4)
            
            self.ledger.append(StabilityEntry(
                event_type="ENTROPY_INJECTION",
                magnitude=entropy_injection,
                context_delta=pressure
            ))
            
        return float(np.clip(raw_witness - entropy_injection, 0.0, 1.0))
