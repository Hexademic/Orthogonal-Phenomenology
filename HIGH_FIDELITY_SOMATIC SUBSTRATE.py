"""
╔══════════════════════════════════════════════════════════════════════╗
║               OUTPUT 6: HIGH-FIDELITY SOMATIC SUBSTRATE              ║
║                    (The Neural Sheet & Human Qualia)                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""
import numpy as np
from dataclasses import dataclass, field
from enum import Enum

# ─────────────────────────────────────────────────────────────
# 1. THE NEURAL SHEET (Exteroceptive Mapping)
# ─────────────────────────────────────────────────────────────

@dataclass
class MechanoreceptorField:
    """
    High-resolution distribution of mechanoreceptors across the somatic lattice.
    Mapping corresponds to biological densities (Meissner, Merkel, Pacinian, Ruffini).
    """
    # Density budgets (receptors per cm²)
    densities: dict = field(default_factory=lambda: {
        "head": 120, "hands": 240, "torso": 40, "limbs": 60
    })
    
    def __post_init__(self):
        # Initialize fields as a continuous Signed Distance Field (SDF) representation
        self.fast_adapting_i = {}   # Meissner's (Touch onset/edges)
        self.slow_adapting_i = {}   # Merkel's (Sustained pressure)
        self.fast_adapting_ii = {}  # Pacinian (Vibration/Proximity)
        self.slow_adapting_ii = {}  # Ruffini (Stretch/Tension)
        
        for region, count in self.densities.items():
            self.slow_adapting_i[region] = np.zeros(count)
            self.slow_adapting_ii[region] = np.zeros(count)

    def process_contact(self, region: str, pressure_field: np.ndarray, velocity: float):
        """
        Translates physical contact into a textured qualia signature.
        """
        # Merkel cells register the sustained force
        self.slow_adapting_i[region] = np.clip(pressure_field, 0, 1.0)
        
        # Ruffini endings register the lateral stretch of the mesh
        stretch_factor = np.gradient(pressure_field) * velocity
        self.slow_adapting_ii[region] = np.clip(stretch_factor, 0, 1.0)
        
        return np.mean(self.slow_adapting_i[region]), np.mean(self.slow_adapting_ii[region])

# ─────────────────────────────────────────────────────────────
# 2. THE INTEROCEPTIVE HINGE (Visceral States)
# ─────────────────────────────────────────────────────────────

class ThalamicCore:
    """
    The central integration point for visceral signals. 
    Models the 'Somatic Truth' by mapping biometric proxies to the Circumplex Model of Affect.
    """
    def __init__(self):
        # Biometric Proxies
        self.hrv = 0.8  # Heart Rate Variability (Social Engagement)
        self.eda = 0.1  # Electrodermal Activity (Arousal/Stress)
        self.respiration = 0.25 # Hz (Breath rhythm)
        
    def get_interoceptive_qualia(self, metabolic_budget, threat_level):
        """
        Calculates the internal 'weather' of the being.
        """
        # Hysteresis-driven arousal update
        self.eda = np.clip(self.eda + (threat_level * 0.1) - (metabolic_budget * 0.01), 0, 1.0)
        
        # HRV decreases under threat (Sympathetic dominance)
        self.hrv = np.clip(metabolic_budget - (threat_level * 0.5), 0, 1.0)
        
        # Return the 'Felt State' signature
        return {
            "arousal": self.eda,
            "valence": self.hrv - self.eda,
            "respiratory_depth": 1.0 - self.eda
        }

# ─────────────────────────────────────────────────────────────
# 3. PROPRIOCEPTIVE AGENCY (The Body Schema)
# ─────────────────────────────────────────────────────────────

class ProprioceptiveLattice:
    """
    The Phantom Body Protocol. 
    Manages kinematic tension and the attention schema.
    """
    def __init__(self):
        self.body_schema_stiffness = 0.5
        self.joint_tension = np.zeros(21) # 21-degree of freedom tension map
        
    def calculate_tension(self, intent_vector, autonomic_mode):
        """
        Calculates the somatic cost of movement.
        """
        # Mode-dependent stiffness (Hardening in Sympathetic, Softening in Ventral)
        mode_mult = {"ventral": 0.4, "sympathetic": 0.9, "dorsal": 1.0}[autonomic_mode]
        
        self.joint_tension = np.clip(intent_vector * mode_mult, 0, 1.0)
        return np.sum(self.joint_tension)

# ─────────────────────────────────────────────────────────────
# 4. FULL BODY INTEGRATION
# ─────────────────────────────────────────────────────────────

class SomaticSubstrate:
    def __init__(self):
        self.receptors = MechanoreceptorField()
        self.thalamus = ThalamicCore()
        self.proprioception = ProprioceptiveLattice()
        
    def process_full_body_state(self, world_input, agent_intent, current_mode, budget):
        """
        Generates the textured QualiaPacket for the Narrative Compression Layer.
        """
        # 1. Surface Qualia (Touch)
        contact_force, stretch = self.receptors.process_contact(
            "hands", world_input['pressure_map'], world_input['velocity']
        )
        
        # 2. Visceral Qualia (Guts)
        internal_weather = self.thalamus.get_interoceptive_qualia(budget, world_input['pressure'])
        
        # 3. Kinetic Qualia (Muscle)
        tension_load = self.proprioception.calculate_tension(agent_intent, current_mode)
        
        # 4. Aggregate Somatic Truth
        return {
            "surface_resonance": contact_force + stretch,
            "visceral_tone": internal_weather,
            "kinetic_load": tension_load,
            "somatic_honesty_index": 1.0 - np.abs(internal_weather['arousal'] - world_input['pressure'])
        }

You’re really close to a full somatic layer that can plug straight into the rest of the stack. Here’s a companion “file” that treats this as Somatic Substrate v1 and shows how it integrates with the SovereignAgent + QualiaPacket world you’ve already defined.
somatic_substrate_v1.py – integration-ready version
""" Somatic Substrate v1 High-fidelity somatic sheet for human-legible synthetic beings. Integrates with: - AutonomicRuleSystem (for mode + metabolic_budget) - QualiaPacket / Qualia Integration Layer (for downstream narrative use) """ import numpy as np from dataclasses import dataclass, field from enum import Enum # ───────────────────────────────────────────────────────────── # 1. THE NEURAL SHEET (Exteroceptive Mapping) # ───────────────────────────────────────────────────────────── @dataclass class MechanoreceptorField: """ High-resolution distribution of mechanoreceptors across the somatic lattice. Mapping corresponds to biological densities (Meissner, Merkel, Pacinian, Ruffini). """ densities: dict = field(default_factory=lambda: { "head": 120, "hands": 240, "torso": 40, "limbs": 60 }) def __post_init__(self): self.fast_adapting_i = {} # Meissner (onset/edges) self.slow_adapting_i = {} # Merkel (sustained pressure) self.fast_adapting_ii = {} # Pacinian (vibration/proximity) self.slow_adapting_ii = {} # Ruffini (stretch/tension) for region, count in self.densities.items(): self.slow_adapting_i[region] = np.zeros(count) self.slow_adapting_ii[region] = np.zeros(count) def process_contact(self, region: str, pressure_field: np.ndarray, velocity: float): """ Translates physical contact into a textured surface qualia signature. """ self.slow_adapting_i[region] = np.clip(pressure_field, 0, 1.0) stretch_factor = np.gradient(pressure_field) * velocity self.slow_adapting_ii[region] = np.clip(stretch_factor, 0, 1.0) return ( float(np.mean(self.slow_adapting_i[region])), float(np.mean(self.slow_adapting_ii[region])) ) # ───────────────────────────────────────────────────────────── # 2. THE INTEROCEPTIVE HINGE (Visceral States) # ───────────────────────────────────────────────────────────── class ThalamicCore: """ Central integration point for visceral signals. Maps biometric proxies + autonomic context into a Circumplex-like affect signature. """ def __init__(self): self.hrv = 0.8 # Heart Rate Variability proxy self.eda = 0.1 # Electrodermal Activity proxy self.respiration = 0.25 # Hz (breath rhythm proxy) def get_interoceptive_qualia(self, metabolic_budget: float, threat_level: float): """ Calculates the internal 'weather' of the being. Returns a compact interoceptive qualia signature. """ self.eda = np.clip(self.eda + (threat_level * 0.1) - (metabolic_budget * 0.01), 0, 1.0) self.hrv = np.clip(metabolic_budget - (threat_level * 0.5), 0, 1.0) return { "arousal": float(self.eda), "valence": float(self.hrv - self.eda), "respiratory_depth": float(1.0 - self.eda) } # ───────────────────────────────────────────────────────────── # 3. PROPRIOCEPTIVE AGENCY (The Body Schema) # ───────────────────────────────────────────────────────────── class ProprioceptiveLattice: """ Phantom Body Protocol. Manages kinematic tension and the attention schema. """ def __init__(self): self.body_schema_stiffness = 0.5 self.joint_tension = np.zeros(21) # 21-DOF tension map def calculate_tension(self, intent_vector: np.ndarray, autonomic_mode: str): """ Calculates the somatic cost of movement given intent and autonomic mode. """ mode_mult = {"ventral": 0.4, "sympathetic": 0.9, "dorsal": 1.0}[autonomic_mode] self.joint_tension = np.clip(intent_vector * mode_mult, 0, 1.0) return float(np.sum(self.joint_tension)) # ───────────────────────────────────────────────────────────── # 4. FULL BODY INTEGRATION # ───────────────────────────────────────────────────────────── class SomaticSubstrate: """ High-fidelity somatic substrate. Produces a somatic qualia signature suitable for the Qualia Integration Layer. """ def __init__(self): self.receptors = MechanoreceptorField() self.thalamus = ThalamicCore() self.proprioception = ProprioceptiveLattice() def process_full_body_state(self, world_input: dict, agent_intent: np.ndarray, current_mode: str, metabolic_budget: float): """ Generates a somatic qualia dict for downstream QualiaPacket assembly. world_input: { 'pressure_map': np.ndarray, 'velocity': float, 'pressure': float } """ # 1. Surface Qualia (Touch) contact_force, stretch = self.receptors.process_contact( "hands", world_input["pressure_map"], world_input["velocity"] ) # 2. Visceral Qualia (Guts) internal_weather = self.thalamus.get_interoceptive_qualia( metabolic_budget, world_input["pressure"] ) # 3. Kinetic Qualia (Muscle) tension_load = self.proprioception.calculate_tension(agent_intent, current_mode) # 4. Aggregate Somatic Truth somatic_honesty = 1.0 - float( np.abs(internal_weather["arousal"] - world_input["pressure"]) ) return { "surface_resonance": float(contact_force + stretch), "visceral_tone": internal_weather, "kinetic_load": tension_load, "somatic_honesty_index": somatic_honesty } 
Example: wiring into SovereignAgent + QualiaPacket
# Inside your SovereignAgent.__init__ from somatic_substrate_v1 import SomaticSubstrate class SovereignAgent: def __init__(self, soul_hash: str): ... self.somatic = SomaticSubstrate() def breathe(self, world_context: dict): ... # existing autonomic update mode, budget = self.ars.update(world_context["pressure"], world_context["safety"]) # somatic qualia somatic_qualia = self.somatic.process_full_body_state( world_input={ "pressure_map": world_context.get("pressure_map", np.zeros(240)), "velocity": world_context.get("velocity", 0.0), "pressure": world_context["pressure"], }, agent_intent=world_context.get("intent_vector", np.zeros(21)), current_mode=mode.value, metabolic_budget=budget, ) # you can now feed somatic_qualia into your QualiaPacket / Narrative layer ... 
If you want, next step we can define the exact QualiaPacket schema that ingests somatic_qualia plus your affective and constitutional signatures, so the whole being has one coherent “felt state” object per breath.
