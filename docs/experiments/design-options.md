# Circuit Design Options

These are possible circuits you could build using the available parts. All designs must total ≤ 650 ng of DNA.

## Available Parts Reference

**ERNs:** CasE, Csy4, PgU

**Wiring (ERN_rec_ERN):** PgU_rec_Csy4, PgU_rec_CasE, Csy4_rec_CasE, CasE_rec_Csy4

**Outputs (ERN_rec_color):** Csy4_rec_mNeonGreen, CasE_rec_mNeonGreen, PgU_rec_mNeonGreen, CasE_rec_Csy4_rec_mKO2

**Colors:** mKO2, eBFP2, mMaroon1, mNeonGreen

---

## Option A: Three-Layer Cascade

Use all 3 ERNs in a chain to demonstrate triple inhibition.

### Logic

```
CasE ──inhibits──► Csy4 ──inhibits──► PgU ──inhibits──► mNeonGreen
     (Csy4_rec_CasE)   (PgU_rec_Csy4)    (PgU_rec_mNeonGreen)
```

- CasE is present → kills Csy4
- Csy4 is gone → can't kill PgU
- PgU is present → kills mNeonGreen
- **Green is OFF** (three negatives = negative)

### CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ThreeLayer,X1,CasE,50,150
ThreeLayer,X1,eBFP2,50,50
ThreeLayer,X2,Csy4_rec_CasE,50,100
ThreeLayer,X2,mMaroon1,50,50
ThreeLayer,X3,PgU_rec_Csy4,50,100
ThreeLayer,Bias,PgU_rec_mNeonGreen,50,200
```

Total: 150 + 50 + 100 + 50 + 100 + 200 = **650 ng**

### Expected Result

| Color | Status | Why |
|-------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Maroon (mMaroon1) | ON | Constitutive control |
| Green (mNeonGreen) | **OFF** | PgU is active and cutting it |

### What Makes This Interesting

- Uses all 3 ERNs in the library
- Demonstrates a 3-layer inhibition cascade
- Contrast with the default circuit (2 layers, green ON) — here adding a third layer flips the output
- Good control experiment: remove CasE from X1 and green should turn ON (Csy4 would survive, kill PgU, free mNeonGreen)

---

## Option B: AND Gate Using Dual-Recognition Part

The part `CasE_rec_Csy4_rec_mKO2` has recognition sequences for **both** CasE and Csy4. Orange is only ON if **neither** enzyme is present. If either one is there, it cuts the mKO2 mRNA.

### Logic

```
         CasE ──inhibits──┐
                           ├──► mKO2 (orange)
         Csy4 ──inhibits──┘
         (via CasE_rec_Csy4_rec_mKO2)

PgU ──inhibits──► CasE    (via CasE_rec_... wait)
```

The challenge: to get orange ON, you need to suppress **both** CasE and Csy4. But looking at the available wiring parts:
- PgU_rec_Csy4 — Csy4 inhibits PgU (not what we want)
- PgU_rec_CasE — CasE inhibits PgU (not what we want)
- Csy4_rec_CasE — CasE inhibits Csy4 ✓
- CasE_rec_Csy4 — Csy4 inhibits CasE ✓

Problem: to suppress both CasE and Csy4, you'd need something that inhibits both. But CasE and Csy4 inhibit *each other* — they can't both be suppressed at the same time by each other.

### Workaround: Use PgU to suppress one, and chain to suppress the other

```
PgU (free, strong)
  └── not inhibited by anything (just expressed directly)

CasE_rec_Csy4: Csy4 inhibits CasE... but we need to also remove Csy4

This doesn't work cleanly with the available parts.
```

### Simpler AND Gate Demo

Instead of trying to get orange ON, demonstrate the AND gate by showing orange is OFF:

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ANDgate,X1,CasE,50,100
ANDgate,X2,Csy4,50,100
ANDgate,Output,CasE_rec_Csy4_rec_mKO2,50,200
ANDgate,Control,eBFP2,50,100
ANDgate,Control,mNeonGreen,50,150
```

Total: 100 + 100 + 200 + 100 + 150 = **650 ng**

### Expected Result

| Color | Status | Why |
|-------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Green (mNeonGreen) | ON | Constitutive control, no one cutting it |
| Orange (mKO2) | **OFF** | Both CasE and Csy4 are present, either one cuts it |

### What Makes This Interesting

- Demonstrates the AND gate part — orange requires absence of both inhibitors
- Both CasE and Csy4 are present, so orange is doubly suppressed
- Compare with a control that has only one ERN: orange should still be OFF (either one is sufficient)
- To see orange ON, you'd run a control with neither CasE nor Csy4

---

## Option C: Competing Inhibitors

Two ERNs compete over the same target. The dominant one determines the output.

### Logic

```
CasE (strong, 200 ng) ──inhibits──► Csy4 (via Csy4_rec_CasE)
                       ──inhibits──► mNeonGreen (via CasE_rec_mNeonGreen)

Csy4 (if it survives) ──inhibits──► PgU (via PgU_rec_Csy4)
```

CasE is the "dominant input." It suppresses both Csy4 and mNeonGreen directly.

### CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
Compete,X1,CasE,50,200
Compete,X1,eBFP2,50,50
Compete,X2,Csy4_rec_CasE,50,100
Compete,X2,mMaroon1,50,50
Compete,X3,PgU_rec_Csy4,50,100
Compete,Bias,CasE_rec_mNeonGreen,50,150
```

Total: 200 + 50 + 100 + 50 + 100 + 150 = **650 ng**

### Expected Result

| Color | Status | Why |
|-------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Maroon (mMaroon1) | ON | Constitutive control |
| Green (mNeonGreen) | **OFF** | CasE is strong and directly inhibits it |

### What Makes This Interesting

- CasE dominates the network — it's the strongest signal (200 ng)
- CasE kills Csy4, so PgU is free (Csy4 can't inhibit it) — but PgU has nothing to act on in this circuit
- Demonstrates that signal strength (ng amount) determines network behavior
- Interesting variant: reduce CasE to 50 ng and increase Csy4_rec_CasE to 200 ng — does Csy4 survive enough to change the outcome?

---

## Option D: Double Negative with AND Gate Readout

Combine a double-negative chain with the dual-recognition AND gate output.

### Logic

```
CasE (input) ──inhibits──► Csy4 (via Csy4_rec_CasE)

AND gate output: CasE_rec_Csy4_rec_mKO2
  - CasE present → cuts mKO2 mRNA → orange OFF
  - Csy4 absent (killed by CasE) → can't cut mKO2 mRNA
  - But CasE alone is enough to kill it → orange OFF
```

### CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
DoubleNeg,X1,CasE,50,150
DoubleNeg,X2,Csy4_rec_CasE,50,100
DoubleNeg,Output,CasE_rec_Csy4_rec_mKO2,50,150
DoubleNeg,Control1,eBFP2,50,100
DoubleNeg,Control2,mMaroon1,50,50
DoubleNeg,Control3,mNeonGreen,50,100
```

Total: 150 + 100 + 150 + 100 + 50 + 100 = **650 ng**

### Expected Result

| Color | Status | Why |
|-------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Maroon (mMaroon1) | ON | Constitutive control |
| Green (mNeonGreen) | ON | Constitutive, no one cutting it |
| Orange (mKO2) | **OFF** | CasE is present and cuts it (AND gate — one input is enough) |

### What Makes This Interesting

- Shows the AND gate in action alongside a double-negative chain
- CasE kills Csy4 AND kills mKO2 — demonstrates that one active inhibitor is sufficient for the AND gate
- To get orange ON, you'd need a circuit where something kills CasE AND something kills Csy4 simultaneously
- Three constitutive controls give strong confirmation that transfection worked

---

## Summary: Choosing a Circuit

| Option | ERNs Used | Key Feature | Output |
|--------|-----------|-------------|--------|
| A: Three-Layer Cascade | All 3 | Longest inhibition chain | Green OFF |
| B: AND Gate | CasE + Csy4 | Dual-recognition part | Orange OFF |
| C: Competing Inhibitors | All 3 | Signal strength matters | Green OFF |
| D: Double Neg + AND | CasE (+ Csy4 regulated) | AND gate + chain combo | Orange OFF |

**Option A is recommended** — it uses all 3 ERNs, has a clear predicted outcome, and pairs well with the default circuit as a comparison (2-layer = green ON vs. 3-layer = green OFF).
