# Submission Summary

## Group Submission for HTGAA 2026 Week 7: Genetic Circuits II

### Two Circuits Submitted

We are submitting two circuits that demonstrate fundamentally different neuromorphic architectures using the same plasmid library.

---

## Circuit 1: Three-Layer Cascade ("ThreeLayer")

**File:** `neuromorphic_experiment1.zip`

**Architecture:** Linear chain of 3 ERNs

```
PgU ──▶ Csy4 ──▶ CasE ──▶ mNeonGreen (green)
  |         |        |          |
ACTIVE   KILLED   ACTIVE      OFF
```

**Parts used:** PgU, eBFP2, PgU_rec_Csy4, mMaroon1, Csy4_rec_CasE, CasE_rec_mNeonGreen

**Total DNA:** 650 ng

**Expected result:**
- Blue: ON (control)
- Maroon: ON (control)
- Green: **OFF** (circuit output — triple inhibition)

**What it demonstrates:** An odd number of inhibition layers produces a negative output. Directly comparable to the default 2-layer circuit where green is ON.

---

## Circuit 2: AND Gate ("ANDgate")

**File:** `neuromorphic_experiment2.zip`

**Architecture:** Two ERNs converge on one output

```
CasE ──┐
       ├──▶ mKO2 (orange) ── OFF
Csy4 ──┘
```

**Parts used:** CasE, Csy4, CasE_rec_Csy4_rec_mKO2, eBFP2, mNeonGreen

**Total DNA:** 650 ng

**Expected result:**
- Blue: ON (control)
- Green: ON (control)
- Orange: **OFF** (AND gate output — both ERNs targeting it)

**What it demonstrates:** The dual-recognition part creates a biological AND gate. Orange requires the absence of both CasE AND Csy4 to turn on.

---

## Why These Two Circuits

| Aspect | Circuit 1 | Circuit 2 |
|--------|-----------|-----------|
| Architecture | Serial (chain) | Parallel (convergent) |
| ERNs | All 3 (PgU, Csy4, CasE) | 2 (CasE, Csy4) |
| Logic type | Cascade/sequential | Logic gate |
| Output reporter | Green (mNeonGreen) | Orange (mKO2) |
| Key concept | Chain length flips output | Multiple inputs on one target |
| Comparison to default | Same reporter, opposite result | Different architecture entirely |

Together, they explore the two main ways to wire neuromorphic circuits:
1. **Chains** — information flows sequentially through multiple layers
2. **Gates** — multiple signals converge on a single decision point

These correspond to the two fundamental motifs in neural networks: serial processing (deep networks) and parallel integration (wide layers).

---

## Files Included

### Experiment 1 (neuromorphic_experiment1.zip)
- `experiment_config.csv` — Circuit design with slot assignments
- `opentrons_protocol.py` — OT-2 robot instructions
- `plate_layouts.xlsx` — Visual plate layout
- `biocompiler_format.json5` — Biocompiler simulation input

### Experiment 2 (neuromorphic_experiment2.zip)
- `experiment_config.csv` — Circuit design with slot assignments
- `opentrons_protocol.py` — OT-2 robot instructions
- `plate_layouts.xlsx` — Visual plate layout
- `biocompiler_format.json5` — Biocompiler simulation input

### Input CSVs
- `three-layer-cascade.csv` — Design template input for Circuit 1
- `and-gate.csv` — Design template input for Circuit 2

---

## Simulation Results

Both circuits passed OT-2 simulation successfully in the NeuromorphicWizard:

- **Circuit 1:** 6 source tubes → 4 mixing groups → 4 Lipofectamine tubes → Well A1
- **Circuit 2:** 5 source tubes → 4 mixing groups → 4 Lipofectamine tubes → Well A1

No errors, no volume violations, all DNA concentrations within pipettable range (>= 1 uL).
