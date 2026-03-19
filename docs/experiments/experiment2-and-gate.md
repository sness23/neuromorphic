# Experiment 2: AND Gate

## Circuit Name: ANDgate

## Design Rationale

This circuit demonstrates a fundamentally different architecture from the Three-Layer Cascade. Instead of a linear chain of inhibitions, two ERNs **converge** on a single output. The special part `CasE_rec_Csy4_rec_mKO2` has recognition sequences for **both** CasE and Csy4, meaning either enzyme alone is sufficient to destroy its mRNA. Orange (mKO2) is only produced when both enzymes are absent.

This implements a biological **AND gate** — specifically, an AND gate on the *absence* of the inputs. In Boolean terms: output = NOT(CasE) AND NOT(Csy4). Since both are present, the output is OFF.

## Circuit Logic

```
CasE ──inhibits──┐
                  ├──▶ mKO2 (orange) ── OFF
Csy4 ──inhibits──┘
      (via CasE_rec_Csy4_rec_mKO2)
```

### Step-by-step logic trace:

1. **CasE is expressed freely** (100 ng) — no ERN targets it, no recognition sequences on its mRNA
2. **Csy4 is expressed freely** (100 ng) — no ERN targets it, no recognition sequences on its mRNA
3. **Both CasE and Csy4 scan all mRNA in the cell** — they find `CasE_rec_Csy4_rec_mKO2` mRNA, which has recognition sequences for both
4. **Either enzyme alone is sufficient to destroy mKO2 mRNA** — with both present, the mRNA is doubly targeted and efficiently destroyed
5. **mKO2 is OFF** — no orange fluorescence

### Reporter logic:

- **eBFP2 (blue)**: Constitutive (no recognition sequence). Always ON. Transfection control.
- **mNeonGreen (green)**: Constitutive (no recognition sequence). Always ON. Transfection control.
- **mKO2 (orange)**: Regulated by both CasE and Csy4 via dual recognition sequences. Both are present → orange is **OFF**.

## Input CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ANDgate,X1,CasE,50,100
ANDgate,X2,Csy4,50,100
ANDgate,Output,CasE_rec_Csy4_rec_mKO2,50,200
ANDgate,Control,eBFP2,50,100
ANDgate,Control,mNeonGreen,50,150
```

Total DNA: 100 + 100 + 200 + 100 + 150 = **650 ng** (maximum)

## Transfection Groups

### Group X1: CasE (single transfection)

| Plasmid | Amount | Role |
|---------|--------|------|
| CasE | 100 ng | ERN enzyme #1. Freely expressed. Scans for CasE recognition sequences on mRNA. |

CasE is one of two inputs to the AND gate. It is delivered alone in its own transfection group.

### Group X2: Csy4 (single transfection)

| Plasmid | Amount | Role |
|---------|--------|------|
| Csy4 | 100 ng | ERN enzyme #2. Freely expressed. Scans for Csy4 recognition sequences on mRNA. |

Csy4 is the second input to the AND gate. It is delivered alone in its own transfection group. Both ERNs are given equal amounts (100 ng each) since neither is more "important" than the other in this design.

### Group Output: CasE_rec_Csy4_rec_mKO2 (single transfection)

| Plasmid | Amount | Role |
|---------|--------|------|
| CasE_rec_Csy4_rec_mKO2 | 200 ng | Encodes mKO2 (orange fluorescent protein), but mRNA has recognition sequences for BOTH CasE and Csy4. Either enzyme can cut it. |

This is the AND gate element. The dual recognition sequence means:
- If only CasE is present → orange OFF (CasE cuts it)
- If only Csy4 is present → orange OFF (Csy4 cuts it)
- If both CasE and Csy4 are present → orange OFF (both cut it)
- If neither CasE nor Csy4 is present → **orange ON** (nothing cuts it)

Given the highest dose (200 ng) to ensure strong fluorescence if it were ever to be expressed. In this circuit, it won't be — but the high dose makes the absence of orange a stronger signal.

### Group Control: eBFP2 + mNeonGreen (co-transfected)

| Plasmid | Amount | Role |
|---------|--------|------|
| eBFP2 | 100 ng | Blue fluorescent reporter. Constitutive. Transfection control. |
| mNeonGreen | 150 ng | Green fluorescent reporter. Constitutive. Transfection control. |

Two constitutive reporters co-transfected in the same group. Neither has any recognition sequences, so neither is affected by CasE or Csy4. They serve as positive controls to confirm that the cells received DNA and are expressing it. mNeonGreen gets a higher dose (150 ng) to ensure it's clearly visible.

## Biocompiler Ratios

| Plasmid | ng | Ratio | Percentage |
|---------|-----|-------|-----------|
| CasE | 100 | 0.154 | 15.4% |
| Csy4 | 100 | 0.154 | 15.4% |
| CasE_rec_Csy4_rec_mKO2 | 200 | 0.308 | 30.8% |
| eBFP2 | 100 | 0.154 | 15.4% |
| mNeonGreen | 150 | 0.231 | 23.1% |

## OT-2 Deck Layout

### Tube Rack 1 (Slot 4)

| Position | Contents | Purpose |
|----------|----------|---------|
| A1 | CasE DNA (50 ng/uL) | Source tube |
| A2 | Csy4 DNA (50 ng/uL) | Source tube |
| A3 | CasE_rec_Csy4_rec_mKO2 DNA (50 ng/uL) | Source tube |
| A4 | eBFP2 DNA (50 ng/uL) | Source tube |
| A5 | mNeonGreen DNA (50 ng/uL) | Source tube |
| A6 | Empty → X1 DNA mix (CasE) | DNA destination |
| B1 | Empty → X2 DNA mix (Csy4) | DNA destination |
| B2 | Empty → Output DNA mix (CasE_rec_Csy4_rec_mKO2) | DNA destination |
| B3 | Empty → Control DNA mix (eBFP2 + mNeonGreen) | DNA destination |
| B4 | Empty → X1 L3K/OM tube | Lipofectamine destination |
| B5 | Empty → X2 L3K/OM tube | Lipofectamine destination |
| B6 | Empty → Output L3K/OM tube | Lipofectamine destination |
| C1 | Empty → Control L3K/OM tube | Lipofectamine destination |

### Tube Rack 3 (Slot 6) — Reagents

| Position | Contents |
|----------|----------|
| D1 | Empty → OM/L3K master mix |
| D2 | Empty → OM/P3K master mix |
| D3 | L3000 reagent (added during pause) |
| D4 | P3000 reagent (added during pause) |
| D6 | Opti-MEM medium |

### Output Plate (Slot 2)

| Position | Contents |
|----------|----------|
| A1 | All 4 transfection groups combined onto HEK293 cells |

## Volume Calculations

All volumes include a 1.2x excess multiplier.

### DNA Volumes

| Plasmid | ng wanted | DNA Volume | Calculation |
|---------|-----------|------------|-------------|
| CasE | 100 | 2.4 uL | (100/50) × 1.2 |
| Csy4 | 100 | 2.4 uL | (100/50) × 1.2 |
| CasE_rec_Csy4_rec_mKO2 | 200 | 4.8 uL | (200/50) × 1.2 |
| eBFP2 | 100 | 2.4 uL | (100/50) × 1.2 |
| mNeonGreen | 150 | 3.6 uL | (150/50) × 1.2 |

### Reagent Volumes

| Reagent | Total Volume |
|---------|-------------|
| Opti-MEM (per mix) | 46.8 uL |
| P3000 | 2.06 uL |
| L3000 | 2.06 uL |

## Physical Protocol Steps

### Step 1: Mix DNA

```
A1 (CasE, 2.4 uL)                    ──▶ A6 (Group X1)

A2 (Csy4, 2.4 uL)                    ──▶ B1 (Group X2)

A3 (CasE_rec_Csy4_rec_mKO2, 4.8 uL)  ──▶ B2 (Group Output)

A4 (eBFP2, 2.4 uL)               ──┐
                                     ├──▶ B3 (Group Control)
A5 (mNeonGreen, 3.6 uL)          ──┘
```

Groups X1, X2, and Output each have a single plasmid. The Control group has two co-transfected plasmids (eBFP2 + mNeonGreen mixed together).

### PAUSE 1: Human adds Opti-MEM and P3000

### Step 2a: OM/P3K master mix → DNA tubes

Robot distributes OM/P3K to each DNA mixing tube (A6, B1, B2, B3).

### PAUSE 2: Human adds L3000

### Step 2b: OM/L3K master mix → Lipofectamine tubes

Robot distributes OM/L3K to empty tubes (B4, B5, B6, C1).

### Step 2c: Combine DNA+P3K with L3K

```
A6 (X1 DNA+P3K)       ──▶ B4 (X1 lipid-DNA complexes)
B1 (X2 DNA+P3K)       ──▶ B5 (X2 lipid-DNA complexes)
B2 (Output DNA+P3K)   ──▶ B6 (Output lipid-DNA complexes)
B3 (Control DNA+P3K)  ──▶ C1 (Control lipid-DNA complexes)
```

### PAUSE 3: 10-minute incubation, then add cell plates

### Step 3: Transfect cells

```
B4 (X1 mix, ~12 uL)       ──▶ Plate 1, Well A1
B5 (X2 mix, ~12 uL)       ──▶ Plate 1, Well A1
B6 (Output mix, ~25 uL)   ──▶ Plate 1, Well A1
C1 (Control mix, ~31 uL)  ──▶ Plate 1, Well A1
```

All four groups converge on the same well. Total volume added to well A1: ~80 uL.

## Post-Transfection Timeline

| Time | What happens |
|------|-------------|
| 0 hours | Plate into 37°C / 5% CO2 incubator |
| 0-6 hours | Lipid nanoparticles deliver DNA into cells |
| 6-12 hours | All 5 proteins begin to be produced |
| 12-24 hours | CasE and Csy4 reach functional levels. Both start scanning for their recognition sequences. Both find CasE_rec_Csy4_rec_mKO2 mRNA and cut it. mKO2 production drops to near zero. |
| 24-48 hours | Readout under fluorescence microscope |

## Expected Results

### Fluorescence Microscopy of Well A1

| Filter/Channel | Reporter | Expected | Reason |
|---------------|----------|----------|--------|
| Blue | eBFP2 | **ON** (bright) | Constitutive. No ERN targets it. |
| Green | mNeonGreen | **ON** (bright) | Constitutive. No ERN targets it. |
| Orange | mKO2 | **OFF** (dark) | Both CasE and Csy4 are cutting its mRNA. |

### AND Gate Truth Table

This is the theoretical truth table for the `CasE_rec_Csy4_rec_mKO2` part. Our experiment tests one row (both inputs present):

| CasE present? | Csy4 present? | mKO2 mRNA cut by | mKO2 (orange) |
|--------------|--------------|-------------------|---------------|
| No | No | Nothing | **ON** |
| Yes | No | CasE | **OFF** |
| No | Yes | Csy4 | **OFF** |
| **Yes** | **Yes** | **Both** | **OFF** ← our experiment |

To fully characterize the AND gate, you would need 4 experiments (one per row). Our experiment demonstrates the "both present" case.

## Control Experiments (if available)

To fully validate the AND gate behavior:

1. **Remove CasE (keep Csy4 only)**: Csy4 alone should still kill mKO2 → orange OFF
2. **Remove Csy4 (keep CasE only)**: CasE alone should still kill mKO2 → orange OFF
3. **Remove both CasE and Csy4**: Nothing cuts mKO2 → **orange ON** (this is the critical test)
4. **CasE_rec_Csy4_rec_mKO2 only**: Same as #3 — should see orange ON

Control #3 is the most important — it would prove that the AND gate output is functional when both inputs are absent.

## Comparison with Experiment 1

| | Experiment 1 (ThreeLayer) | Experiment 2 (ANDgate) |
|---|---|---|
| Architecture | Linear chain (serial) | Convergent (parallel inputs) |
| ERNs used | 3 (CasE, Csy4, PgU) | 2 (CasE, Csy4) |
| Number of inhibition steps | 3 sequential | 2 parallel on same target |
| Output reporter | mNeonGreen (green) | mKO2 (orange) |
| Output state | OFF | OFF |
| Special parts used | None | CasE_rec_Csy4_rec_mKO2 (dual recognition) |
| Key concept | Chain length determines output | Multiple inputs can converge |
| Control reporters | eBFP2, mMaroon1 | eBFP2, mNeonGreen |
