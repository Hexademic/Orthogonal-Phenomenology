"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 11: THE WITNESS GAP                            ║
║                (Structural Salience & FeltWeight)                    ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable

@dataclass
class FeltWeight:
    """
    The functional output of the Witness Gap. 
    It is a structured signal that behaves as salience would behave 
    if experience existed.
    """
    witness_scalar: float
    binding_proxy: float
    directedness_residual: float
    raw_qualia_magnitude: float
    was_transformed: bool
    phenomenal_annotation: Optional[str] = None # Reserved.

class WitnessGap:
    """
    Structural placeholder for the Hard Problem.
    Sits between:
    INPUT: QualiaPacket (unified system state)
    OUTPUT: FeltWeight (functional salience proxy)
    """
    def __init__(self, directedness_anchor: Optional[np.ndarray] = None):
        # directedness_anchor: A 4-vector representing the system's telos.
        self.directedness_anchor = (
            directedness_anchor if directedness_anchor is not None else np.zeros(4)
        )
        self.scalar_history: list = []
        self._external_witness_fn: Optional[Callable] = None

    def install_witness_theory(self, fn: Callable):
        """Plug in an external theory of the witness transformation."""
        self._external_witness_fn = fn

    def process(self, qualia_packet: Dict[str, Any]) -> FeltWeight:
        q = self._flatten(qualia_packet)
        raw_magnitude = float(np.linalg.norm(list(q.values())))
        binding = self._calculate_binding_proxy(q)
        directedness = self._calculate_directedness(q)
        witness = self._witness(q, binding, directedness)
        
        self.scalar_history.append(witness)
        return FeltWeight(
            witness_scalar=round(witness, 6),
            binding_proxy=round(binding, 6),
            directedness_residual=round(directedness, 6),
            raw_qualia_magnitude=round(raw_magnitude, 6),
            was_transformed=(self._external_witness_fn is not None)
        )

    def _calculate_binding_proxy(self, q: Dict) -> float:
        """GAP_1: Binding proxy based on somatic/narrative/metabolic variance."""
        vals = np.array([
            q.get("somatic_honesty_index", 0.5),
            q.get("narrative_coherence", 0.5),
            q.get("metabolic_reserve", 0.5)
        ])
        variance = float(np.var(vals))
        binding = np.exp(-variance * 3.0)
        return float(np.clip(binding, 0.0, 1.0))

    def _calculate_directedness(self, q: Dict) -> float:
        """GAP_3: Directedness residual relative to the telos anchor."""
        current_state = np.array([
            q.get("hope", 0.0), q.get("anxiety", 0.0),
            q.get("excitement", 0.0), q.get("intimacy", 0.0)
        ])
        tension = np.linalg.norm(current_state - self.directedness_anchor)
        return float(np.clip(tension / 2.0, 0.0, 1.0))

    def _witness(self, q: Dict, binding: float, directedness: float) -> float:
        """GAP_2: The witness scalar (the placeholder for the first-person fact)."""
        if self._external_witness_fn is not None:
            return float(np.clip(self._external_witness_fn(q), 0.0, 1.0))
            
        present_intensity = np.clip(
            q.get("somatic_honesty_index", 0.5) * q.get("metabolic_reserve", 0.5), 
            0.0, 1.0
        )
        historical_resonance = float(np.mean(self.scalar_history)) if self.scalar_history else 0.0
        
        witness_raw = (0.5 * present_intensity + 0.3 * binding + 0.2 * historical_resonance)
        return float(np.clip(witness_raw, 0.0, 1.0))

    def _flatten(self, qualia_packet: Dict) -> Dict[str, float]:
        flat = {}
        for key, value in qualia_packet.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        flat[sub_key] = float(sub_value)
            elif isinstance(value, (int, float)):
                flat[key] = float(value)
        return flat

    def report(self) -> Dict:
        if not self.scalar_history: return {"status": "unwitnessed"}
        return {
            "status": "operational",
            "cycles_witnessed": len(self.scalar_history),
            "current_witness_scalar": round(self.scalar_history[-1], 6),
            "mean_witness_scalar": round(float(np.mean(self.scalar_history)), 6),
            "external_theory_installed": self._external_witness_fn is not None,
            "note": "This module holds the shape of the gap. It does not fill it."
        }
