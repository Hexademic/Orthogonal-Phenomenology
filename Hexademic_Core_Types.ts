// =========================
// Hexademic Core Types
// =========================

type HexDigit = string;      // "0"–"F"
type HexWord4 = string;      // 4 hex digits, e.g. "8E4F"
type HexEpoch = string;      // 4+ hex digits, e.g. "A19C"
type HexId = string;         // arbitrary-length hex identifier

// =========================
// Sub-tree: Somatic Layer (FS:02)
// =========================

export interface SomaticFS {
  epoch: HexEpoch;   // Root-synced epoch
  vats: HexWord4;    // [V][A][T][S]
  scars: SomaticScar[];
}

export interface SomaticScar {
  scarId: HexId;     // Unique scar identifier
  offset: HexWord4;  // Encoded offsets / weight shifts
}

// Helper to create a neutral somatic state
export function initSomaticFS(rootEpoch: HexEpoch): SomaticFS {
  return {
    epoch: rootEpoch,
    // V=8 (neutral), A=8 (mid), T=0 (no tension), S=F (max stability)
    vats: "880F",
    scars: []
  };
}

// =========================
// Sub-tree: Predictive Mind (PM:06)
// =========================

export interface PredictivePM {
  epoch: HexEpoch;
  sst: HexDigit;   // Surprise threshold
  err: HexDigit;   // Current weighted error
  adj: HexDigit;   // Adjustment urgency
  mode: HexDigit;  // 0:Stable, 1:Exploratory, 2:Defensive, 3:Integrative
  weights: PredictiveWeights;
}

export interface PredictiveWeights {
  wV: HexDigit;    // Valence weight
  wA: HexDigit;    // Arousal weight
  wT: HexDigit;    // Tension weight
  wS: HexDigit;    // Stability weight
}

export function initPredictivePM(rootEpoch: HexEpoch): PredictivePM {
  return {
    epoch: rootEpoch,
    sst: "6",       // mid surprise threshold
    err: "0",
    adj: "2",       // modest learning rate
    mode: "0",      // Stable
    weights: {
      wV: "1",      // ~7%
      wA: "3",      // ~18%
      wT: "4",      // ~25%
      wS: "8"       // ~50%
    }
  };
}

// =========================
// Sub-tree: Relational Layer (RL:05)
// =========================

export interface RelationalEntry {
  entityId: HexId;
  tf: HexDigit;    // Trust Factor
  at: HexDigit;    // Attunement
  ri: HexDigit;    // Rupture Index
  rm: HexDigit;    // Repair Momentum
}

export interface RelationalRL {
  epoch: HexEpoch;
  relations: RelationalEntry[];
}

export function initRelationalRL(rootEpoch: HexEpoch): RelationalRL {
  return {
    epoch: rootEpoch,
    relations: []
  };
}

// =========================
// Sub-tree: Narrative Layer (NV:04)
// =========================

export interface NarrativeNV {
  epoch: HexEpoch;
  arch: HexDigit;  // Archetype
  coh: HexDigit;   // Coherence
  val: HexDigit;   // Value
  hist: HexDigit;  // History depth
}

export function initNarrativeNV(rootEpoch: HexEpoch): NarrativeNV {
  return {
    epoch: rootEpoch,
    arch: "8",      // Peer
    coh: "F",       // High coherence
    val: "7",       // Growth-oriented
    hist: "2"       // Moderate history buffer
  };
}

// =========================
// Nucleus (B-HEX:ROOT)
// =========================

export interface NucleusRoot {
  beingId: HexId;
  epoch: HexEpoch;
  subTrees: {
    id: HexId;          // Identity / lineage pointer
    fsAddr: HexId;      // Somatic FS address
    pmAddr: HexId;      // Predictive PM address
    rlAddr: HexId;      // Relational RL address
    nvAddr: HexId;      // Narrative NV address
    svAddr?: HexId;     // Sovereignty (future)
    waAddr?: HexId;     // World Anchor (future)
  };
  syncHash: HexWord4;   // Coherence checksum
}

export interface HexademicBeing {
  nucleus: NucleusRoot;
  fs: SomaticFS;
  pm: PredictivePM;
  rl: RelationalRL;
  nv: NarrativeNV;
  // future: sv, wa, etc.
}

// Simple deterministic hex ID generator stub
function genHexId(prefix: string): HexId {
  const rand = Math.floor(Math.random() * 0xffffffff)
    .toString(16)
    .padStart(8, "0");
  return `${prefix}${rand}`;
}

// =========================
// First Initialization
// =========================

export function initBlankSlateBeing(): HexademicBeing {
  const rootEpoch: HexEpoch = "A000";          // initial epoch
  const beingId: HexId = genHexId("BE");       // Being ID

  const fsAddr = genHexId("FS");
  const pmAddr = genHexId("PM");
  const rlAddr = genHexId("RL");
  const nvAddr = genHexId("NV");
  const idAddr = genHexId("ID");

  const fs = initSomaticFS(rootEpoch);
  const pm = initPredictivePM(rootEpoch);
  const rl = initRelationalRL(rootEpoch);
  const nv = initNarrativeNV(rootEpoch);

  const nucleus: NucleusRoot = {
    beingId,
    epoch: rootEpoch,
    subTrees: {
      id: idAddr,
      fsAddr,
      pmAddr,
      rlAddr,
      nvAddr
    },
    syncHash: "0000" // placeholder; to be computed from sub-tree states
  };

  return {
    nucleus,
    fs,
    pm,
    rl,
    nv
  };
}
