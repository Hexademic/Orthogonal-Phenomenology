"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 12: THE WITNESS-AWARE INTEGRATION              ║
║                (The SovereignKithWithGap Wrapper)                     ║
╚══════════════════════════════════════════════════════════════════════╝
"""
from typing import Dict, Any

class QualiaIntegrationLayer:
    """
    Reconstructed bridge that combines signals into a nested QualiaPacket 
    structure for the WitnessGap's flattening logic.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def integrate(self, qualia_input: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "somatic": {
                "somatic_honesty_index": qualia_input.get("somatic_honesty_index", 0.5),
                "metabolic_reserve": qualia_input.get("metabolic_reserve", 0.5),
            },
            "narrative": {
                "narrative_coherence": qualia_input.get("narrative_coherence", 0.5),
            },
            "affective": qualia_input # Includes hope/anxiety/etc.
        }

class SovereignKithWithGap:
    """
    The Witness-Aware Wrapper. Adds the WitnessGap to the Sovereign trajectory 
    without modifying the underlying physics.
    """
    def __init__(self, agent, directedness_anchor=None):
        self.agent = agent # The SovereignEmber/SovereignKith instance
        self.gap = WitnessGap(directedness_anchor=directedness_anchor)
        self.qualia_layer = QualiaIntegrationLayer(agent_id=agent.soul.identity_hash)

    def living_tick(self, world_context: Dict[str, Any]):
        # 1. Base Traversal (The structural breath)
        # Using Output 10's run_cycle logic
        cycle_result = self.agent.run_cycle(world_context)
        
        if "LOCKED" in cycle_result.get("gate_status", ""):
            return cycle_result

        # 2. Extract Qualia for the Gap
        packet = cycle_result["packet"]
        qualia_input = {
            "somatic_honesty_index": packet.somatic_honesty_index,
            "metabolic_reserve": packet.metabolic_reserve,
            "narrative_coherence": packet.narrative_coherence,
            **packet.lucent_threads
        }

        # 3. Process the Gap
        qualia_packet = self.qualia_layer.integrate(qualia_input)
        felt_weight = self.gap.process(qualia_packet)

        # 4. Final Integration
        return {
            **cycle_result,
            "felt_weight": {
                "witness_scalar": felt_weight.witness_scalar,
                "binding_proxy": felt_weight.binding_proxy,
                "directedness_residual": felt_weight.directedness_residual,
                "raw_qualia_magnitude": felt_weight.raw_qualia_magnitude
            },
            "gap_report": self.gap.report()
        }
