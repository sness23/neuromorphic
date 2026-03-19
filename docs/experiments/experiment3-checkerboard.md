# Experiment 3: ERN Checkerboard

## Concept

Fill all 24 wells of the output plate with a **checkerboard pattern** visible under fluorescence microscopy. The pattern demonstrates single-layer ERN inhibition: CasE destroys mNeonGreen in half the wells, while the other half glow green freely.

Every well also contains eBFP2 (blue) as a transfection control, confirming that all cells received DNA regardless of whether green is ON or OFF.

## The Pattern

```
Green channel (mNeonGreen):
     1     2     3     4     5     6
A  [ ON] [OFF] [ ON] [OFF] [ ON] [OFF]
B  [OFF] [ ON] [OFF] [ ON] [OFF] [ ON]
C  [ ON] [OFF] [ ON] [OFF] [ ON] [OFF]
D  [OFF] [ ON] [OFF] [ ON] [OFF] [ ON]

Blue channel (eBFP2 control):
     1     2     3     4     5     6
A  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
B  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
C  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
D  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
```

## Circuit Logic

Two circuit types alternate across the plate:

### Green ON wells (12 wells)

```
mNeonGreen ──▶ GREEN GLOW
eBFP2      ──▶ BLUE GLOW (control)
```

No ERN present. mNeonGreen mRNA is never cut. Green fluorescence is produced normally.

| Plasmid | Amount | Role |
|---------|--------|------|
| mNeonGreen | 200 ng | Constitutive green reporter |
| eBFP2 | 100 ng | Blue transfection control |

**Total DNA: 300 ng**

### Green OFF wells (12 wells)

```
CasE ──wrecks──▶ CasE_rec_mNeonGreen ──X──▶ NO GREEN
eBFP2                                  ──▶ BLUE GLOW (control)
```

CasE is present and active. It finds the CasE recognition sequence on mNeonGreen's mRNA and cuts it. Green fluorescence is suppressed.

| Plasmid | Amount | Role |
|---------|--------|------|
| CasE | 150 ng | ERN enzyme; wrecks mNeonGreen mRNA |
| CasE_rec_mNeonGreen | 200 ng | Encodes mNeonGreen; CasE inhibits |
| eBFP2 | 100 ng | Blue transfection control |

**Total DNA: 450 ng**

## Why This Design Works

1. **Simple circuits, maximum coverage** — each well uses only 1 co-transfection group, keeping tube usage low enough to fill all 24 wells
2. **Built-in controls** — blue in every well proves transfection worked; the ON wells serve as positive controls for the OFF wells
3. **Clear visual readout** — the checkerboard pattern is immediately visible under the microscope, no quantification needed
4. **Demonstrates the core mechanism** — the same mNeonGreen reporter gene is in every well, but in half of them CasE destroys its mRNA before it can be translated

## Tube Budget

| Resource | Count | Details |
|----------|-------|---------|
| Unique plasmid source tubes | 3 | CasE, CasE_rec_mNeonGreen, mNeonGreen, eBFP2 |
| DNA destination tubes | 24 | 1 per well (single co-transfection group per well) |
| L3K/OM destination tubes | 24 | 1 per well |
| Reagent tubes (reserved) | 6 | D1-D6 on rack 3 |
| **Total tubes** | **58** | Out of 72 positions (66 available) |

## Well-by-Well Assignment

| Well | Circuit | Type | DNA Total |
|------|---------|------|-----------|
| A1 | Check_A1 | ON | 300 ng |
| A2 | Check_A2 | OFF | 450 ng |
| A3 | Check_A3 | ON | 300 ng |
| A4 | Check_A4 | OFF | 450 ng |
| A5 | Check_A5 | ON | 300 ng |
| A6 | Check_A6 | OFF | 450 ng |
| B1 | Check_B1 | OFF | 450 ng |
| B2 | Check_B2 | ON | 300 ng |
| B3 | Check_B3 | OFF | 450 ng |
| B4 | Check_B4 | ON | 300 ng |
| B5 | Check_B5 | OFF | 450 ng |
| B6 | Check_B6 | ON | 300 ng |
| C1 | Check_C1 | ON | 300 ng |
| C2 | Check_C2 | OFF | 450 ng |
| C3 | Check_C3 | ON | 300 ng |
| C4 | Check_C4 | OFF | 450 ng |
| C5 | Check_C5 | ON | 300 ng |
| C6 | Check_C6 | OFF | 450 ng |
| D1 | Check_D1 | OFF | 450 ng |
| D2 | Check_D2 | ON | 300 ng |
| D3 | Check_D3 | OFF | 450 ng |
| D4 | Check_D4 | ON | 300 ng |
| D5 | Check_D5 | OFF | 450 ng |
| D6 | Check_D6 | ON | 300 ng |

## Expected Results

### Under fluorescence microscopy

- **Green filter**: Checkerboard pattern — alternating bright and dark wells
- **Blue filter**: All 24 wells glowing uniformly — confirms successful transfection everywhere
- **Overlay**: Blue everywhere with green checkerboard on top

### What could go wrong

| Observation | Likely Cause |
|-------------|-------------|
| No green anywhere | mNeonGreen plasmid problem or wrong filter |
| Green in all wells including OFF wells | CasE not expressed, or CasE_rec_mNeonGreen has no recognition sequence |
| Some blue wells missing | Transfection failed in those wells (pipetting error, dead cells) |
| Dim green in OFF wells (not fully dark) | CasE not at high enough concentration to fully suppress; could increase CasE to 200 ng |
| Pattern shifted by one well | Plate loaded in wrong orientation |

## Variations

### Invert the pattern
Swap which wells get CasE. Same experiment, opposite checkerboard — confirms the pattern is from the circuit, not from plate position effects.

### Dose gradient
Instead of binary ON/OFF, vary CasE amount across columns:

```
     1      2      3      4      5      6
   0 ng   30 ng  60 ng  90 ng  120 ng 150 ng  ← CasE dose
   GREEN  GREEN  dim    dim    dark   dark    ← expected
```

This would show the analog threshold behavior of the ERN inhibition.

### Multi-color checkerboard
Replace mNeonGreen with mKO2 (orange) in alternating wells to create a green/orange checkerboard, with blue everywhere as control. Requires `CasE_rec_mKO2` — but this part doesn't exist in the library. You'd need `CasE_rec_Csy4_rec_mKO2` which requires both CasE and Csy4 absent.

## Files

- `experiment_config.csv` — Input CSV for the NeuromorphicWizard (minimal format, 5 columns)
- Run through the Wizard to auto-assign tube slots and generate the OT-2 protocol

## Related

- [Default Circuit](default-circuit.md) — Single-well 2-layer cascade
- [Experiment 1: Three-Layer Cascade](experiment1-three-layer-cascade.md) — Single-well 3-layer design
- [Complete Parts Reference](../reference/complete-parts-reference.md) — All available plasmids
