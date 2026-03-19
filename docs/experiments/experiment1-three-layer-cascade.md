# Experiment 1: Three-Layer Cascade

## Circuit Name: ThreeLayer

## Design Rationale

The default example circuit uses a 2-layer inhibition chain (Csy4 → CasE → mNeonGreen), resulting in green being ON (double negative = positive). Our circuit extends this to a **3-layer chain** using all three available ERNs. Adding one more inhibition step flips the output: green is now OFF (triple negative = negative).

This creates a direct comparison: same output reporter (mNeonGreen), opposite predicted result. The contrast demonstrates that the number of inhibition layers determines the output state.

## Circuit Logic

```
PgU ──inhibits──▶ Csy4 ──inhibits──▶ CasE ──inhibits──▶ mNeonGreen (green)
    (PgU_rec_Csy4)    (Csy4_rec_CasE)    (CasE_rec_mNeonGreen)
```

### Step-by-step logic trace:

1. **PgU is expressed freely** (150 ng, highest dose) — no ERN is targeting it
2. **PgU cuts Csy4 mRNA** — the plasmid `PgU_rec_Csy4` encodes Csy4 but its mRNA has a PgU recognition sequence. PgU finds it and destroys it. Csy4 protein production is suppressed.
3. **Csy4 is gone, so CasE survives** — the plasmid `Csy4_rec_CasE` encodes CasE with a Csy4 recognition sequence. But Csy4 has been killed by PgU, so nothing is cutting CasE's mRNA. CasE is produced normally.
4. **CasE cuts mNeonGreen mRNA** — the plasmid `CasE_rec_mNeonGreen` encodes mNeonGreen with a CasE recognition sequence. CasE is active and destroys the mNeonGreen mRNA.
5. **mNeonGreen is OFF** — three layers of inhibition = odd number of negatives = negative output.

### Reporter logic:

- **eBFP2 (blue)**: Constitutive (no recognition sequence). Always ON. Serves as transfection control.
- **mMaroon1 (maroon)**: Constitutive (no recognition sequence). Always ON. Serves as transfection control.
- **mNeonGreen (green)**: Regulated by CasE. CasE is active → green is **OFF**.

## Input CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ThreeLayer,X1,PgU,50,150
ThreeLayer,X1,eBFP2,50,50
ThreeLayer,X2,PgU_rec_Csy4,50,100
ThreeLayer,X2,mMaroon1,50,50
ThreeLayer,X3,Csy4_rec_CasE,50,100
ThreeLayer,Bias,CasE_rec_mNeonGreen,50,200
```

Total DNA: 150 + 50 + 100 + 50 + 100 + 200 = **650 ng** (maximum)

## Transfection Groups

### Group X1: PgU + eBFP2 (co-transfected)

| Plasmid | Amount | Role |
|---------|--------|------|
| PgU | 150 ng | The dominant ERN enzyme. Input signal for the cascade. |
| eBFP2 | 50 ng | Blue fluorescent reporter. Constitutive control — confirms transfection worked. |

These two plasmids are mixed together in the same tube and delivered to the cell as a single lipid-DNA complex. PgU is given the highest dose (150 ng) to ensure strong suppression of its target (Csy4).

### Group X2: PgU_rec_Csy4 + mMaroon1 (co-transfected)

| Plasmid | Amount | Role |
|---------|--------|------|
| PgU_rec_Csy4 | 100 ng | Encodes Csy4 enzyme, but mRNA has PgU recognition site. PgU will cut this mRNA, preventing Csy4 production. |
| mMaroon1 | 50 ng | Maroon/red fluorescent reporter. Constitutive control — confirms transfection worked. |

Csy4 would normally be an active enzyme, but because its mRNA is tagged with a PgU recognition sequence, PgU from Group X1 destroys it. This is the first inhibition step.

### Group X3: Csy4_rec_CasE (single transfection)

| Plasmid | Amount | Role |
|---------|--------|------|
| Csy4_rec_CasE | 100 ng | Encodes CasE enzyme, but mRNA has Csy4 recognition site. If Csy4 were present, it would cut this mRNA. But Csy4 has been killed by PgU, so CasE is produced normally. |

This is the second layer of the cascade. CasE survives because its inhibitor (Csy4) has been suppressed by PgU. CasE is now free to act on its target.

### Group Bias: CasE_rec_mNeonGreen (single transfection)

| Plasmid | Amount | Role |
|---------|--------|------|
| CasE_rec_mNeonGreen | 200 ng | Encodes mNeonGreen (green fluorescent protein), but mRNA has CasE recognition site. CasE is active and cuts this mRNA, so mNeonGreen is NOT produced. |

This is the output of the cascade. mNeonGreen is given the highest dose (200 ng) among the regulated parts, but it doesn't matter — CasE is actively destroying its mRNA. The high dose means that if CasE *weren't* present, we'd see very strong green fluorescence. Its absence is the signal that the cascade is working.

## Biocompiler Ratios

The NeuromorphicWizard converts ng amounts to ratios of total DNA (650 ng) for simulation:

| Plasmid | ng | Ratio | Percentage |
|---------|-----|-------|-----------|
| PgU | 150 | 0.231 | 23.1% |
| eBFP2 | 50 | 0.077 | 7.7% |
| PgU_rec_Csy4 | 100 | 0.154 | 15.4% |
| mMaroon1 | 50 | 0.077 | 7.7% |
| Csy4_rec_CasE | 100 | 0.154 | 15.4% |
| CasE_rec_mNeonGreen | 200 | 0.308 | 30.8% |

## OT-2 Deck Layout

### Tube Rack 1 (Slot 4)

| Position | Contents | Purpose |
|----------|----------|---------|
| A1 | PgU DNA (50 ng/uL) | Source tube |
| A2 | eBFP2 DNA (50 ng/uL) | Source tube |
| A3 | PgU_rec_Csy4 DNA (50 ng/uL) | Source tube |
| A4 | mMaroon1 DNA (50 ng/uL) | Source tube |
| A5 | Csy4_rec_CasE DNA (50 ng/uL) | Source tube |
| A6 | CasE_rec_mNeonGreen DNA (50 ng/uL) | Source tube |
| B1 | Empty → X1 DNA mix (PgU + eBFP2) | DNA destination |
| B2 | Empty → X2 DNA mix (PgU_rec_Csy4 + mMaroon1) | DNA destination |
| B3 | Empty → X3 DNA mix (Csy4_rec_CasE) | DNA destination |
| B4 | Empty → Bias DNA mix (CasE_rec_mNeonGreen) | DNA destination |
| B5 | Empty → X1 L3K/OM tube | Lipofectamine destination |
| B6 | Empty → X2 L3K/OM tube | Lipofectamine destination |
| C1 | Empty → X3 L3K/OM tube | Lipofectamine destination |
| C2 | Empty → Bias L3K/OM tube | Lipofectamine destination |

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

All volumes include a 1.2x excess multiplier for pipetting error.

### DNA Volumes (per plasmid)

| Plasmid | ng wanted | Concentration | DNA Volume | Calculation |
|---------|-----------|---------------|------------|-------------|
| PgU | 150 | 50 ng/uL | 3.6 uL | (150/50) × 1.2 |
| eBFP2 | 50 | 50 ng/uL | 1.2 uL | (50/50) × 1.2 |
| PgU_rec_Csy4 | 100 | 50 ng/uL | 2.4 uL | (100/50) × 1.2 |
| mMaroon1 | 50 | 50 ng/uL | 1.2 uL | (50/50) × 1.2 |
| Csy4_rec_CasE | 100 | 50 ng/uL | 2.4 uL | (100/50) × 1.2 |
| CasE_rec_mNeonGreen | 200 | 50 ng/uL | 4.8 uL | (200/50) × 1.2 |

### Reagent Volumes (totals across all groups)

| Reagent | Formula | Total Volume |
|---------|---------|-------------|
| Opti-MEM (per mix) | total_ng × 0.05 × 1.2 | 46.8 uL |
| P3000 | total_ng × 0.0022 × 1.2 | 2.06 uL |
| L3000 | total_ng × 0.0022 × 1.2 | 2.06 uL |

Where total_ng = 650 ng.

## Physical Protocol Steps

### Step 1: Mix DNA (robot, ~5 minutes)

The robot pipettes DNA from source tubes into mixing tubes:

```
A1 (PgU, 3.6 uL)             ──┐
                                ├──▶ B1 (Group X1 mix)
A2 (eBFP2, 1.2 uL)           ──┘

A3 (PgU_rec_Csy4, 2.4 uL)    ──┐
                                  ├──▶ B2 (Group X2 mix)
A4 (mMaroon1, 1.2 uL)         ──┘

A5 (Csy4_rec_CasE, 2.4 uL)   ──▶ B3 (Group X3 mix)

A6 (CasE_rec_mNeonGreen, 4.8 uL) ──▶ B4 (Group Bias mix)
```

Uses the p20 pipette (left mount) for all transfers since volumes are under 20 uL. Each source tube is mixed 3x before aspiration. Co-transfection groups are mixed 3x after the last plasmid is added.

### PAUSE 1: Human adds Opti-MEM and P3000 to rack 3

### Step 2a: Prepare OM/P3K master mix (robot)

1. Robot pipettes 2.06 uL P3000 from D4 → D2
2. Robot pipettes 46.8 uL Opti-MEM from D6 → D2, mixes 3x
3. Robot distributes OM/P3K to each DNA tube:
   - 12.5 uL → B1 (X1)
   - 9.4 uL → B2 (X2)
   - 6.3 uL → B3 (X3)
   - 12.5 uL → B4 (Bias)

### PAUSE 2: Human adds L3000 to rack 3

### Step 2b: Prepare OM/L3K master mix (robot)

1. Robot pipettes 2.06 uL L3000 from D3 → D1
2. Robot pipettes 46.8 uL Opti-MEM from D6 → D1, mixes 3x
3. Robot distributes OM/L3K to empty Lipofectamine tubes:
   - 12.5 uL → B5 (for X1)
   - 9.4 uL → B6 (for X2)
   - 6.3 uL → C1 (for X3)
   - 12.5 uL → C2 (for Bias)

### Step 2c: Combine DNA+P3K with L3K (robot)

Robot pipettes DNA+OM+P3K mixtures into the L3K tubes:

```
B1 (X1 DNA+P3K)   ──▶ B5 (X1 lipid-DNA complexes form)
B2 (X2 DNA+P3K)   ──▶ B6 (X2 lipid-DNA complexes form)
B3 (X3 DNA+P3K)   ──▶ C1 (X3 lipid-DNA complexes form)
B4 (Bias DNA+P3K)  ──▶ C2 (Bias lipid-DNA complexes form)
```

Each tube is mixed 3x after combining. The lipids self-assemble around the DNA into nanoparticles.

### PAUSE 3: Human waits 10 minutes for complexes to form, then places cell plates on deck

### Step 3: Transfect cells (robot)

Robot pipettes each transfection mix onto HEK293 cells in well A1:

```
B5 (X1 mix, ~25 uL)    ──▶ Plate 1, Well A1
B6 (X2 mix, ~19 uL)    ──▶ Plate 1, Well A1
C1 (X3 mix, ~12 uL)    ──▶ Plate 1, Well A1
C2 (Bias mix, ~25 uL)  ──▶ Plate 1, Well A1
```

Dispense speed is reduced to 50 uL/sec (from 250) and clearance is raised to 2mm to avoid disturbing the cell monolayer.

## Post-Transfection Timeline

| Time | What happens |
|------|-------------|
| 0 hours | Plate goes into 37C / 5% CO2 incubator |
| 0-6 hours | Lipid nanoparticles fuse with cell membranes, delivering plasmid DNA into cells |
| 6-12 hours | Cells begin transcribing plasmids into mRNA and translating into proteins |
| 12-24 hours | ERN enzymes accumulate to functional levels. PgU starts cutting Csy4 mRNA. CasE starts cutting mNeonGreen mRNA. Circuit logic takes full effect. |
| 24-48 hours | Readout — examine plate under fluorescence microscope |

## Expected Results

### Fluorescence Microscopy of Well A1

| Filter/Channel | Reporter | Expected | Reason |
|---------------|----------|----------|--------|
| Blue | eBFP2 | **ON** (bright) | Constitutive. No ERN targets it. Confirms transfection. |
| Maroon/Red | mMaroon1 | **ON** (bright) | Constitutive. No ERN targets it. Confirms transfection. |
| Green | mNeonGreen | **OFF** (dark) | CasE is active and cutting its mRNA. This is the circuit output. |

### ERN Activity Summary

| ERN | Expressed from | Targeted by | Status | Effect |
|-----|---------------|-------------|--------|--------|
| PgU | PgU (free) | Nothing | **ACTIVE** | Cuts Csy4 mRNA |
| Csy4 | PgU_rec_Csy4 | PgU | **SUPPRESSED** | Cannot cut CasE mRNA |
| CasE | Csy4_rec_CasE | Csy4 (suppressed) | **ACTIVE** | Cuts mNeonGreen mRNA |

## Comparison with Default Circuit

| | Default (MyCircuit) | Ours (ThreeLayer) |
|---|---|---|
| Layers | 2 (Csy4 → CasE) | 3 (PgU → Csy4 → CasE) |
| ERNs used | 2 (Csy4, CasE) | 3 (PgU, Csy4, CasE) |
| Output reporter | mNeonGreen | mNeonGreen (same!) |
| Output state | **ON** (double negative) | **OFF** (triple negative) |
| Control reporters | mKO2 (orange), eBFP2 (blue) | eBFP2 (blue), mMaroon1 (maroon) |

The key insight: same output gene, opposite result. Adding one more inhibition layer flips the answer, just like multiplying by another negative number flips the sign.

## Control Experiments (if available)

To fully validate the cascade, ideal control experiments would be:

1. **Remove PgU**: Without PgU, Csy4 is free → Csy4 kills CasE → CasE can't kill mNeonGreen → green ON
2. **Remove PgU_rec_Csy4**: PgU has nothing to inhibit → Csy4_rec_CasE has no Csy4 to fear → CasE is active → green OFF (same as full circuit, but simpler)
3. **Remove Csy4_rec_CasE**: No CasE → nothing cuts mNeonGreen → green ON
4. **All reporters only**: Just eBFP2 + mMaroon1 + mNeonGreen, no ERNs → all three ON (baseline)
