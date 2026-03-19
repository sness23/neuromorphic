# Physical Protocol Walkthrough

## What Actually Happens on the Plates

This document traces the complete physical process from OT-2 deck setup through to the final fluorescence readout.

## OT-2 Deck Layout

```
 ┌─────────────┬─────────────┬─────────────┐
 │ Slot 10     │ Slot 11     │             │
 │ 20uL tips   │ 300uL tips  │             │
 ├─────────────┼─────────────┼─────────────┤
 │ Slot 7      │ Slot 8      │ Slot 9      │
 │             │ 20uL tips   │ 300uL tips  │
 ├─────────────┼─────────────┼─────────────┤
 │ Slot 4      │ Slot 5      │ Slot 6      │
 │ Tube rack 1 │ Tube rack 2 │ Tube rack 3 │
 │ DNA tubes   │             │ Reagents    │
 ├─────────────┼─────────────┼─────────────┤
 │ Slot 1      │ Slot 2      │ Slot 3      │
 │             │ Cell plate 1│ Cell plate 2│
 └─────────────┴─────────────┴─────────────┘
```

## Before the Run: Human Setup

A human loads the deck:

**Tube rack 1 (slot 4)** — plasmid DNA source tubes and empty destination tubes:

| Position | Contents |
|----------|----------|
| A1 | Csy4 DNA (50 ng/uL stock) |
| A2 | mKO2 DNA (50 ng/uL stock) |
| A3 | Csy4_rec_CasE DNA (50 ng/uL stock) |
| A4 | eBFP2 DNA (50 ng/uL stock) |
| A5 | CasE_rec_mNeonGreen DNA (50 ng/uL stock) |
| A6 | Empty tube (X1 DNA mixing destination) |
| B1 | Empty tube (X2 DNA mixing destination) |
| B2 | Empty tube (Bias DNA mixing destination) |
| B3 | Empty tube (X1 Lipofectamine destination) |
| B4 | Empty tube (X2 Lipofectamine destination) |
| B5 | Empty tube (Bias Lipofectamine destination) |

**Tube rack 3 (slot 6)** — reagents:

| Position | Contents |
|----------|----------|
| D1 | Empty tube (OM/L3K master mix) |
| D2 | Empty tube (OM/P3K master mix) |
| D3 | L3000 reagent (added during pause) |
| D4 | P3000 reagent (added during pause) |
| D5-D6 | Opti-MEM medium |

**Plates (slots 2-3)** — 24-well plates already seeded with HEK293 cells. The cells have been growing for ~24 hours and form a monolayer (single layer of cells attached to the bottom of each well).

## Step 1: Mix DNA

The robot pipettes plasmid DNA from source tubes into destination mixing tubes, one per transfection group:

```
Source tubes                    Destination tubes
───────────                     ─────────────────
A1 (Csy4, 3.6 uL)      ──┐
                           ├──► A6 (Group X1 mix)
A2 (mKO2, 2.4 uL)      ──┘

A3 (Csy4_rec_CasE, 2.4 uL) ──┐
                                ├──► B1 (Group X2 mix)
A4 (eBFP2, 2.4 uL)          ──┘

A5 (CasE_rec_mNeonGreen, 4.8 uL) ──► B2 (Group Bias mix)
```

Volumes are calculated as: (DNA wanted in ng) / (concentration in ng/uL) * 1.2 excess.

For co-transfection groups, the robot mixes the tube 3 times with 20 uL after the last plasmid is added.

**ROBOT PAUSES** — Human places Opti-MEM and P3000 reagent tubes on the deck.

## Step 2: Add Lipofectamine Reagents

This step creates lipid-DNA nanoparticles that can enter cells. It happens in two sub-steps because the P3000 and L3000 must be prepared separately before combining.

### Step 2a: OM/P3K Master Mix → DNA Tubes

1. Robot pipettes P3000 into empty tube D2
2. Robot adds Opti-MEM to tube D2, mixes → this is the OM/P3K master mix
3. Robot distributes OM/P3K master mix into each DNA mixing tube:
   - OM/P3K → A6 (mixes with X1 DNA)
   - OM/P3K → B1 (mixes with X2 DNA)
   - OM/P3K → B2 (mixes with Bias DNA)

The P3000 enhancer reagent binds to the plasmid DNA.

**ROBOT PAUSES** — Human places L3000 reagent tube on the deck.

### Step 2b: OM/L3K Master Mix → Empty Tubes

1. Robot pipettes L3000 into empty tube D1
2. Robot adds Opti-MEM to tube D1, mixes → this is the OM/L3K master mix
3. Robot distributes OM/L3K master mix into the Lipofectamine destination tubes:
   - OM/L3K → B3 (for X1)
   - OM/L3K → B4 (for X2)
   - OM/L3K → B5 (for Bias)

### Step 2c: Combine DNA + Lipofectamine

Robot pipettes DNA+OM+P3K mixture into the L3K tubes:

```
DNA tubes (with P3K)     L3K tubes (combined)
────────────────────     ────────────────────
A6 (X1 DNA+P3K)   ──►   B3 (X1 lipid-DNA complexes)
B1 (X2 DNA+P3K)   ──►   B4 (X2 lipid-DNA complexes)
B2 (Bias DNA+P3K)  ──►   B5 (Bias lipid-DNA complexes)
```

When the DNA/P3000 mixture meets the L3000/Opti-MEM, the lipids self-assemble around the DNA into **lipid nanoparticles** (tiny fat bubbles containing plasmid DNA).

**ROBOT PAUSES** — Human waits **10 minutes** for lipid-DNA complexes to fully form, then places the cell plates on the deck.

## Step 3: Transfect Cells

The robot pipettes each transfection mix onto the HEK293 cells. It uses:
- Slower dispense speed (50 uL/sec instead of 250) to avoid disturbing the cell monolayer
- Higher clearance (2mm from bottom) so the pipette tip doesn't touch the cells

```
Transfection tubes         Cell plate well
──────────────────         ───────────────
B3 (X1 mix)         ──┐
B4 (X2 mix)         ──┼──► Plate 1, Well A1
B5 (Bias mix)        ──┘
```

All three groups go into **the same well (A1)**, so one population of HEK293 cells receives all 5 plasmids.

## After the Robot Finishes

### Hours 0-6: Uptake
The plate goes into a **37C / 5% CO2 incubator**. The lipid nanoparticles settle onto the cells and fuse with cell membranes, releasing the plasmid DNA inside. Each cell may take up different amounts of each plasmid.

### Hours 6-12: Expression Begins
The cells' machinery starts **transcribing** the plasmid DNA into mRNA, then **translating** the mRNA into proteins. All 5 proteins begin to accumulate:
- Csy4 enzyme
- mKO2 (orange fluorescent protein)
- CasE enzyme (from Csy4_rec_CasE)
- eBFP2 (blue fluorescent protein)
- mNeonGreen (from CasE_rec_mNeonGreen)

### Hours 12-24: Circuit Logic Takes Effect
As protein levels rise, the endoribonuclease enzymes start cutting their target mRNAs:

1. **Csy4 accumulates** (from group X1, 150 ng — the highest amount)
2. **Csy4 finds and cuts CasE mRNA** — because `Csy4_rec_CasE` means CasE's mRNA has a Csy4 recognition sequence. CasE protein levels drop.
3. **CasE cannot cut mNeonGreen mRNA** — because CasE is being suppressed. So `CasE_rec_mNeonGreen` just produces mNeonGreen normally.
4. **mKO2 and eBFP2 are unregulated** — they keep accumulating regardless of any ERN activity.

### Hours 24-48: Readout
The plate is taken to a **fluorescence microscope**. Using different excitation/emission filters, you image well A1:

```
┌─────────────────────────────────────────────┐
│                Well A1                       │
│                                              │
│  Filter: Orange (mKO2)     → GLOWS ✓        │
│  Filter: Blue (eBFP2)      → GLOWS ✓        │
│  Filter: Green (mNeonGreen) → GLOWS ✓       │
│                                              │
│  All three colors visible = circuit works    │
└─────────────────────────────────────────────┘
```

## What Each Color Tells You

| Color | Protein | Regulated? | What it means |
|-------|---------|------------|---------------|
| Orange | mKO2 | No (constitutive) | Transfection worked, cells are alive |
| Blue | eBFP2 | No (constitutive) | Transfection worked, cells are alive |
| Green | mNeonGreen | Yes (by CasE, which is inhibited by Csy4) | **Circuit logic is working** — double negative = positive |

## The Key Insight

Green is only ON because of **double inhibition**:

```
Csy4 ──(inhibits)──► CasE ──(inhibits)──► mNeonGreen

Csy4 is present → CasE is OFF → mNeonGreen is ON
```

If you ran a **control experiment** without Csy4 (removing it from group X1), you would expect:
- Orange: ON (still constitutive)
- Blue: ON (still constitutive)
- Green: **OFF** (CasE would be free to cut mNeonGreen mRNA)

This difference between the experimental and control conditions demonstrates that the neuromorphic circuit is performing analog computation inside living cells.

## Quantitative Readout

Beyond just ON/OFF, the fluorescence **intensity** of each color is proportional to protein expression levels. By adjusting the ng amounts of each plasmid in the design template, you tune the analog behavior of the circuit. The biocompiler simulation (from the Predict tab in NeuromorphicWizard) predicts these intensity levels based on the plasmid ratios.
