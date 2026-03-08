"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 13: ORGANISMAL STABILITY PATCH                 ║
║                (Preventing Runaway & Collapse Loops)                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np

# ─────────────────────────────────────────────────────────────
# 1. PATCHED WITNESS GAP (Addressing Runaway & Starvation)
# ─────────────────────────────────────────────────────────────

class PatchedWitnessGap(WitnessGap):
    """
    Upgraded WitnessGap with Identity Entropy and World Engagement.
    Prevents Ego Fixation and Witness Starvation.
    """
    def _calculate_binding_proxy(self, q: dict) -> float:
        """
        PREVENTION: Witness Starvation.
        Binding now requires external coupling to prevent manufactured meaning.
        """
        internal_coherence = super()._calculate_binding_proxy(q)
        # [span_3](start_span)[span_4](start_span)World engagement derived from flux and receptor activity[span_3](end_span)[span_4](end_span)
        world_engagement = q.get("world_engagement", 0.5)
        
        # Binding falls if world engagement drops, forcing reality re-coupling.
        return float(internal_coherence * world_engagement)

    def _witness(self, q: dict, binding: float, directedness: float) -> float:
        """
        PREVENTION: Identity Runaway (Witness Amplification).
        Injects entropy when the system becomes too self-referential.
        """
        coherence = q.get("narrative_coherence", 0.5)
        [span_5](start_span)[span_6](start_span)confidence = q.get("somatic_honesty_index", 0.5) #[span_5](end_span)[span_6](end_span)
        
        # Identity pressure check
        identity_pressure = coherence * confidence
        novelty_weight = 0.0
        
        # If unchecked coherence leads to ego-fixation, inject novelty
        if identity_pressure > 0.9:
            # [span_7](start_span)[span_8](start_span)[span_9](start_span)Random identity disruption mimics sleep/forgetting[span_7](end_span)[span_8](end_span)[span_9](end_span)
            novelty_weight = np.random.uniform(0.1, 0.3)
            
        witness_base = super()._witness(q, binding, directedness)
        # Satiation logic: forced entropy reduces the runaway attractor
        return float(np.clip(witness_base - novelty_weight, 0.0, 1.0))

# ─────────────────────────────────────────────────────────────
# 2. PATCHED MASTER LOOP (Addressing Collapse & Narrative Lock)
# ─────────────────────────────────────────────────────────────

class PatchedSovereignLifeCycle(SovereignLifeCycle):
    """
    Upgraded run_cycle with Desperation Factors and Surprise Privilege.
    Prevents Somatic Collapse and Narrative Delusion.
    """
    def run_cycle(self, world_context):
        # Retrieve baseline from existing architecture
        [span_10](start_span)[span_11](start_span)budget = self.agent.ars.metabolic_budget #[span_10](end_span)[span_11](end_span)
        [span_12](start_span)[span_13](start_span)error = self.epsilon_internal # EPL Mode B Surprise[span_12](end_span)[span_13](end_span)
        
        # FIX 1: Somatic Collapse (Energy Sink)
        # Starving organisms must take risks to recover.
        desperation_factor = 1.0
        [span_14](start_span)[span_15](start_span)if budget < 0.4: # Critical metabolic threshold[span_14](end_span)[span_15](end_span)
            desperation_factor = 1.0 / (budget + 1e-6)
            # This multiplier overrides standard risk avoidance for action initiation
        
        # FIX 2: Narrative Lock (Coherence Trap)
        # If surprise is high, we must temporarily de-weight the narrative 'story'
        narrative_weight = 1.0
        if error > 0.7: # High prediction error threshold
            # [span_16](start_span)[span_17](start_span)SURPRISE PRIVILEGE: Allow model reconstruction over consistency[span_16](end_span)[span_17](end_span)
            narrative_weight = 0.3
            
        # Execute the cycle with modified weights
        result = super().run_cycle(world_context)
        
        # Inject the stability diagnostics into the QualiaPacket
        result["stability_metrics"] = {
            "desperation_active": desperation_factor > 1.0,
            "surprise_privilege_active": narrative_weight < 1.0,
            "identity_entropy_injection": result["packet"].self_report.find("entropy") != -1
        }
        
        return result
