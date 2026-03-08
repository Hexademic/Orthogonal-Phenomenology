"""
╔══════════════════════════════════════════════════════════════════════╗
║                OUTPUT 15: RELATIONAL RECOUPLING                      ║
║                (Recovery Curves & Threshold Adaptation)              ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np

class RelationalRecouplingJanus(JanusGate):
    """
    Advanced Janus Gate with Recovery Curves and Ledger-Driven Adaptation.
    Prevents the 'Collapse-Retry' oscillation loop.
    """
    def __init__(self):
        super().__init__()
        # Recovery state tracking
        self.is_recovering = False
        self.engagement_at_collapse = 0.0
        self.delta_required = 0.2  # Delta engagement needed to exit recovery
        self.recovery_witness_cap = 0.4 # Capped salience during recovery
        
        # Adaptation multipliers (Threshold Drift)
        self.floor_drift_rate = 0.05
        self.ceiling_drift_rate = 0.02

    def apply_recovery_logic(self, current_witness, current_engagement):
        """
        Implements the recovery curve: Witness remains capped until 
        engagement rises by the delta_required.
        """
        if self.is_recovering:
            # Check for exit condition: Engagement must rise significantly
            improvement = current_engagement - self.engagement_at_collapse
            if improvement >= self.delta_required:
                self.is_recovering = False
                return current_witness, "RECOVERY_EXITED"
            
            # While in recovery, enforce the Witness Scalar Cap
            clamped_witness = min(current_witness, self.recovery_witness_cap)
            return clamped_witness, "RECOVERY_ACTIVE"
        
        return current_witness, "NORMAL"

    def trigger_collapse(self, witness_scalar, world_engagement):
        """Overrides base collapse to initiate the Recovery Curve."""
        self.is_recovering = True
        self.engagement_at_collapse = world_engagement
        # Standard collapse logic
        return super().validate_invariants(witness_scalar, world_engagement)

    def adapt_thresholds(self):
        """
        Ledger-Driven Adaptation: The organism 'learns' its limits.
        If collapses accumulate, the floor rises and the ceiling falls.
        """
        collapse_count = sum(1 for e in self.ledger if e.event_type == "ENGAGEMENT_COLLAPSE")
        entropy_count = sum(1 for e in self.ledger if e.event_type == "ENTROPY_INJECTION")
        
        # Raise engagement floor after frequent disconnects
        if collapse_count > 5:
            self.engagement_floor = min(0.5, self.engagement_floor + self.floor_drift_rate)
            
        # Lower witness ceiling if ego-fixation persists
        if entropy_count > 10:
            self.witness_ceiling = max(0.5, self.witness_ceiling - self.ceiling_drift_rate)

# ─────────────────────────────────────────────────────────────
# 2. INTEGRATED LIFE-CYCLE (Recoupling Awareness)
# ─────────────────────────────────────────────────────────────

class SovereignLifeCycleV2(PatchedSovereignLifeCycle):
    """
    Master Loop that respects the Relational Recoupling Protocol.
    """
    def run_cycle(self, world_context):
        # 1. Base Traversal
        result = super().run_cycle(world_context)
        packet = result["packet"]
        
        # 2. Janus Gate Validation & Recovery Application
        witness = result.get("felt_weight", {}).get("witness_scalar", 0.5)
        engagement = world_context.get("world_engagement", 0.5)
        
        # Check invariants
        valid, reason = self.agent.janus.validate_invariants(witness, engagement)
        
        # Apply Recovery Curve
        witness_adjusted, recovery_status = self.agent.janus.apply_recovery_logic(witness, engagement)
        
        # 3. Trigger Adaptation every 100 cycles
        if self.cycle_count % 100 == 0:
            self.agent.janus.adapt_thresholds()

        # 4. Update Result with Recovery Metadata
        result["janus_status"] = {
            "valid": valid,
            "reason": reason if not valid else "STABLE",
            "recovery_status": recovery_status,
            "witness_clamped": witness_adjusted != witness
        }
        
        return result
