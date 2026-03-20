# Experiment Configuration Columns

The experiment configuration CSV is the central data format used by the NeuromorphicWizard. It has two forms:

1. **Input CSV** (5 columns) — what you write by hand to define your circuit design
2. **Output CSV** (10 columns) — what the Wizard generates after assigning physical locations on the OT-2 deck

This document explains every column.

---

## Input Columns (User-Defined)

These 5 columns are the minimum required. You fill these in to describe your circuit.

### Circuit name

The name of your circuit. All rows belonging to the same circuit share the same name.

- **Examples**: `MyCircuit`, `ThreeLayer`, `ANDgate`
- **Rules**: Free-form text. One CSV can contain multiple circuits (each gets its own well on the output plate).
- **Why it matters**: The Wizard groups rows by circuit name to determine which plasmids end up in the same cell. Each circuit gets its own output plate well.

### Transfection group

A label that groups plasmids that will be physically mixed together in the same tube before being delivered to cells.

- **Examples**: `X1`, `X2`, `X3`, `Bias`, `Output`, `Control`
- **Rules**: Free-form text. Rows with the same transfection group (within the same circuit) are co-transfected — their DNA is mixed into one tube, wrapped in a single set of lipid nanoparticles, and delivered to the cell together.
- **Why it matters**: Co-transfected plasmids are more likely to enter the same cell. Each group gets its own DNA mixing tube, its own Lipofectamine tube, and its own pipetting step onto the output plate.

**Example**: In the default circuit, group X1 contains Csy4 (150 ng) + mKO2 (100 ng). These are pipetted into the same mixing tube, mixed with Lipofectamine together, and delivered as one complex.

### Contents

The name of the plasmid (DNA part).

- **Examples**: `Csy4`, `PgU_rec_Csy4`, `CasE_rec_mNeonGreen`, `eBFP2`, `CasE_rec_Csy4_rec_mKO2`
- **Rules**: Must match a name from the HTGAA parts library. The naming convention encodes the biology:
  - **Plain name** (`CasE`, `Csy4`, `PgU`): An ERN enzyme with no recognition sequences on its mRNA — freely expressed.
  - **`X_rec_Y`** (`PgU_rec_Csy4`): Encodes protein Y, but the mRNA has a recognition sequence for enzyme X. X can cut this mRNA and suppress Y.
  - **`X_rec_Y_rec_Z`** (`CasE_rec_Csy4_rec_mKO2`): Encodes protein Z, but the mRNA has recognition sequences for both X and Y. Either enzyme can suppress Z.
  - **Color names** (`mNeonGreen`, `mKO2`, `eBFP2`, `mMaroon1`): Fluorescent reporter proteins with no recognition sequences — constitutive controls.

### Concentration (ng/uL)

The stock concentration of the plasmid DNA in the source tube.

- **Value**: Always `50` for this course (all plasmids are provided at 50 ng/uL).
- **Why it matters**: Used to calculate pipetting volumes. Volume = DNA wanted / Concentration.

### DNA wanted (ng)

How many nanograms of this plasmid to include in the circuit.

- **Examples**: `50`, `100`, `150`, `200`
- **Rules**: All rows within a circuit must sum to **<= 650 ng** (the maximum DNA budget per circuit, accounting for Lipofectamine capacity). In practice, the actual hard limit in the code is 800 ng, but the course recommends 650 ng.
- **Why it matters**: Higher amounts mean more copies of that plasmid enter the cell, leading to higher expression of that protein. The **ratio** between plasmids is what determines circuit behavior — a dominant ERN should get more DNA than its target.

---

## Output Columns (Wizard-Generated)

These 5 columns are added by the NeuromorphicWizard when it generates the experiment configuration. They map the abstract circuit design to physical locations on the OT-2 liquid handling robot's deck.

### Position Notation

All position columns use the format **`WellPosition.SlotNumber`**:

- **`A1.1`** = Well A1 on the labware in Slot 1
- **`B3.4`** = Well B3 on the tube rack in Slot 4
- **`C1.6`** = Well C1 on the rack/plate in Slot 6

**Slot assignments** (24-tube rack layout):

| Slot | Labware | Purpose |
|------|---------|---------|
| 4 | 24-tube rack | Primary tube rack (DNA sources, mixing tubes, Lipofectamine tubes) |
| 5 | 24-tube rack | Overflow tube rack (used when Slot 4 is full) |
| 6 | 24-tube rack | Reagent rack (Opti-MEM, P3000, L3000, master mix tubes) |
| 2 | 24-well plate | Output plate #1 (cells receive transfection mixes here) |
| 3 | 24-well plate | Output plate #2 (overflow, if needed) |

### DNA source

The physical tube position where the stock DNA for this plasmid is located on the OT-2 deck. This is where the human places the DNA tube before starting the protocol.

- **Example**: `A1.1` (well A1 on rack in slot 4... but note: the `.1` here actually refers to an internal rack numbering, see below)
- **Assignment rule**: One unique position per unique plasmid name. If the same plasmid appears in multiple rows (e.g., same DNA used in two circuits), they share the same DNA source.
- **Protocol step**: The robot aspirates DNA from this position.

**Important**: The `.N` suffix in these positions refers to the rack number within the layout's input rack list (1-indexed), not the OT-2 slot number directly. Rack 1 = Slot 4, Rack 2 = Slot 5, Rack 3 = Slot 6 in the 24-tube layout. So `A1.1` = position A1 on the rack in Slot 4.

### DNA destination

The physical tube position where the robot pipettes the DNA for mixing. All plasmids in the same transfection group are pipetted into the same destination tube.

- **Example**: `B1.1` (position B1 on rack in Slot 4)
- **Assignment rule**: One unique position per unique (Circuit name, Transfection group) pair. Co-transfected plasmids share the same DNA destination.
- **Protocol step**: The robot dispenses DNA here, then later adds Opti-MEM + P3000 master mix to this same tube. The DNA + OM/P3K mixture is then transferred to the L3K/OM tube.

**Example from ThreeLayer circuit**:
```
PgU      → DNA source A1.1 → DNA destination B1.1  (group X1)
eBFP2    → DNA source A2.1 → DNA destination B1.1  (group X1, same tube)
PgU_rec_Csy4 → DNA source A3.1 → DNA destination B2.1  (group X2)
```
PgU and eBFP2 share destination B1.1 because they are both in group X1.

### L3K/OM MM destination

The physical tube position where the Lipofectamine 3000 / Opti-MEM master mix is prepared for this transfection group. "L3K/OM MM" stands for "Lipofectamine 3000 / Opti-MEM Master Mix."

- **Example**: `B5.1` (position B5 on rack in Slot 4)
- **Assignment rule**: One unique position per unique (Circuit name, Transfection group) pair — mirrors the DNA destination grouping.
- **Protocol step**:
  1. Robot dispenses Opti-MEM + L3000 master mix into this tube
  2. Robot transfers the DNA + OM/P3K mixture (from the DNA destination tube) into this tube
  3. The DNA and lipids self-assemble into lipid nanoparticles (10-minute incubation)
  4. Robot pipettes the final lipid-DNA complex from this tube onto the cell plate

This is the tube where the actual transfection complex forms — the critical step where DNA gets wrapped in lipid nanoparticles.

### Plate destination

The well on the output plate where the final transfection mix is dispensed onto cells.

- **Example**: `A1.1` (well A1 on the plate in Slot 2)
- **Assignment rule**: One unique position per unique circuit. All transfection groups within the same circuit go to the same well (the same cell population receives all groups).
- **Protocol step**: Robot pipettes each transfection group's lipid-DNA complex into this well, where HEK293 cells are growing in culture medium.

**Example from ThreeLayer circuit**: All four groups (X1, X2, X3, Bias) have plate destination `A1.1` — they all converge on the same well of cells. If you had a second circuit in the same CSV, it would get a different well (e.g., `A2.1`).

### Diluted source

The physical tube position for a pre-diluted version of a DNA stock, used **only** when the required pipetting volume is too small for the robot to handle accurately.

- **Example**: `C3.1` (position C3 on rack in Slot 4), or empty if no dilution is needed
- **Trigger**: Dilution is required when `DNA wanted (ng) < 2 * Concentration (ng/uL)`. With a concentration of 50 ng/uL, any row requesting less than 100 ng of DNA would need a volume less than 2 uL — below the OT-2's accurate pipetting range with a P20 tip. (Note: the actual threshold is `MIN_PIPETTE_VOLUME_UL = 2 uL`.)
- **Assignment rule**: One unique position per unique plasmid name that requires dilution. The robot first dilutes the stock DNA with water into this tube, then pipettes from this diluted tube instead of the original source.

**Example from ThreeLayer circuit**:
```
eBFP2    → 50 ng wanted / 50 ng/uL = 1.0 uL (< 2 uL!) → Diluted source: C3.1
mMaroon1 → 50 ng wanted / 50 ng/uL = 1.0 uL (< 2 uL!) → Diluted source: C4.1
PgU      → 150 ng wanted / 50 ng/uL = 3.0 uL (>= 2 uL) → Diluted source: (empty)
```

When dilution is needed, the robot:
1. Pipettes water from the reagent rack into the diluted source tube
2. Pipettes stock DNA from the DNA source into the diluted source tube, mixes
3. Pipettes from the diluted source tube (larger volume, more accurate) into the DNA destination

---

## Complete Example

Here is the full experiment configuration for the ThreeLayer circuit, showing how the input columns map to the generated output columns:

```
Circuit name | Transfection group | Contents             | Conc | DNA ng | DNA source | DNA dest | L3K/OM dest | Plate dest | Diluted source
-------------|--------------------|-----------------------|------|--------|------------|----------|-------------|------------|---------------
ThreeLayer   | X1                 | PgU                  | 50   | 150    | A1.1       | B1.1     | B5.1        | A1.1       |
ThreeLayer   | X1                 | eBFP2                | 50   | 50     | A2.1       | B1.1     | B5.1        | A1.1       | C3.1
ThreeLayer   | X2                 | PgU_rec_Csy4         | 50   | 100    | A3.1       | B2.1     | B6.1        | A1.1       |
ThreeLayer   | X2                 | mMaroon1             | 50   | 50     | A4.1       | B2.1     | B6.1        | A1.1       | C4.1
ThreeLayer   | X3                 | Csy4_rec_CasE        | 50   | 100    | A5.1       | B3.1     | C1.1        | A1.1       |
ThreeLayer   | Bias               | CasE_rec_mNeonGreen  | 50   | 200    | A6.1       | B4.1     | C2.1        | A1.1       |
```

Key observations:
- **DNA source**: Each plasmid gets its own unique source tube (A1–A6)
- **DNA destination**: Groups X1 (PgU + eBFP2) share B1.1; groups X2 (PgU_rec_Csy4 + mMaroon1) share B2.1; X3 and Bias each get their own
- **L3K/OM destination**: Mirrors the grouping — one Lipofectamine tube per transfection group
- **Plate destination**: All rows share A1.1 — everything goes to the same well
- **Diluted source**: Only eBFP2 and mMaroon1 need dilution (50 ng at 50 ng/uL = 1 uL, below the 2 uL threshold)

---

## Flow Summary

The columns trace the physical journey of each DNA plasmid through the protocol:

```
[DNA source]           Human places stock DNA tubes on the rack
       │
       ▼ (robot pipettes DNA, or dilutes first if needed)
[Diluted source]       Robot dilutes low-volume DNA with water (if < 2 uL)
       │
       ▼ (robot pipettes DNA into mixing tubes, grouped by transfection group)
[DNA destination]      DNA mixing tube — co-transfected plasmids combined here
       │                  + Opti-MEM + P3000 added
       │
       ▼ (robot transfers DNA+P3K mix into Lipofectamine tube)
[L3K/OM destination]   Lipofectamine tube — lipid-DNA complexes form (10 min)
       │
       ▼ (robot pipettes final complex onto cells)
[Plate destination]    Output well — HEK293 cells receive the transfection mix
```
