# Experiment Comparison: Circuits 0, 1, and 2

This document shows the three core experiments side-by-side to clarify where each circuit's input comes from and how the inhibition chains differ.

## Quick Summary

| | Experiment 0 (Default) | Experiment 1 (Three-Layer) | Experiment 2 (AND Gate) |
|---|---|---|---|
| **Topology** | 2-layer cascade | 3-layer cascade | Convergent AND gate |
| **Chain** | Csy4 → CasE → mNeonGreen | PgU → Csy4 → CasE → mNeonGreen | CasE + Csy4 → mKO2 |
| **Input ERN** | Csy4 (free) | PgU (free) | CasE + Csy4 (both free) |
| **Green output** | ON (double negative) | OFF (triple negative) | N/A (output is orange) |
| **Total DNA** | 650 ng | 650 ng | 650 ng |

## What "input" means

In these circuits, the **input** is the free ERN — the enzyme that starts the inhibition chain. It's called "free" because its mRNA has no recognition site, so nothing can stop it from being produced. It's always ON.

Every circuit starts from a free ERN and ends at a fluorescent reporter. The number of inhibition steps between them determines whether the output is ON or OFF.

---

## Experiment 0: Default Circuit (2-Layer Cascade)

### Input: Csy4 (free)

Csy4 is the input. Nothing inhibits it — it's always active.

```
INPUT          LAYER 1              OUTPUT
─────          ───────              ──────
Csy4 (free) ──inhibits──▶ CasE ──inhibits──▶ mNeonGreen
                          (from Csy4_rec_CasE)    (from CasE_rec_mNeonGreen)
```

### Step by step

1. **Csy4** is produced freely (150 ng). No one can stop it.
2. **Csy4 recognizes `Csy4_rec`** on CasE's mRNA → cuts it → **CasE is OFF**
3. **CasE is OFF** → can't recognize `CasE_rec` on mNeonGreen's mRNA → **green is ON**

Two negatives = positive. Green glows.

### CSV

```
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
MyCircuit,X1,Csy4,50,150
MyCircuit,X1,mKO2,50,100
MyCircuit,X2,Csy4_rec_CasE,50,100
MyCircuit,X2,eBFP2,50,100
MyCircuit,Bias,CasE_rec_mNeonGreen,50,200
```

### Part-by-part breakdown

| Part | What it encodes | Recognition site on mRNA? | Who can cut it? | Result |
|------|----------------|--------------------------|-----------------|--------|
| Csy4 | Csy4 enzyme | None | Nobody | Always active |
| mKO2 | Orange reporter | None | Nobody | Always glows orange |
| Csy4_rec_CasE | CasE enzyme | Csy4_rec | Csy4 | CasE is suppressed |
| eBFP2 | Blue reporter | None | Nobody | Always glows blue |
| CasE_rec_mNeonGreen | mNeonGreen reporter | CasE_rec | CasE (but CasE is dead) | Green glows |

### Expected result

| Reporter | Status | Why |
|----------|--------|-----|
| Orange (mKO2) | ON | Constitutive control |
| Blue (eBFP2) | ON | Constitutive control |
| Green (mNeonGreen) | **ON** | CasE is suppressed by Csy4, so green survives |

---

## Experiment 1: Three-Layer Cascade

### Input: PgU (free)

PgU is the input. It's the only ERN that nothing in the parts library can inhibit — making it the natural starting point for a 3-layer cascade.

```
INPUT          LAYER 1              LAYER 2              OUTPUT
─────          ───────              ───────              ──────
PgU (free) ──inhibits──▶ Csy4 ──inhibits──▶ CasE ──inhibits──▶ mNeonGreen
                         (from PgU_rec_Csy4)  (from Csy4_rec_CasE)  (from CasE_rec_mNeonGreen)
```

### Step by step

1. **PgU** is produced freely (150 ng). No one can stop it.
2. **PgU recognizes `PgU_rec`** on Csy4's mRNA → cuts it → **Csy4 is OFF**
3. **Csy4 is OFF** → can't cut CasE's mRNA → **CasE is ON**
4. **CasE is ON** → recognizes `CasE_rec` on mNeonGreen's mRNA → cuts it → **green is OFF**

Three negatives = negative. Green is dark.

### CSV

```
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ThreeLayer,X1,PgU,50,150
ThreeLayer,X1,eBFP2,50,50
ThreeLayer,X2,PgU_rec_Csy4,50,100
ThreeLayer,X2,mMaroon1,50,50
ThreeLayer,X3,Csy4_rec_CasE,50,100
ThreeLayer,Bias,CasE_rec_mNeonGreen,50,200
```

### Part-by-part breakdown

| Part | What it encodes | Recognition site on mRNA? | Who can cut it? | Result |
|------|----------------|--------------------------|-----------------|--------|
| PgU | PgU enzyme | None | Nobody | Always active |
| eBFP2 | Blue reporter | None | Nobody | Always glows blue |
| PgU_rec_Csy4 | Csy4 enzyme | PgU_rec | PgU | Csy4 is suppressed |
| mMaroon1 | Maroon reporter | None | Nobody | Always glows maroon |
| Csy4_rec_CasE | CasE enzyme | Csy4_rec | Csy4 (but Csy4 is dead) | CasE is active |
| CasE_rec_mNeonGreen | mNeonGreen reporter | CasE_rec | CasE (active!) | Green is suppressed |

### Expected result

| Reporter | Status | Why |
|----------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Maroon (mMaroon1) | ON | Constitutive control |
| Green (mNeonGreen) | **OFF** | CasE is active and destroys green mRNA |

### Comparison with Experiment 0

Same output gene (mNeonGreen), opposite result. Adding PgU as a third layer flips the output from ON to OFF.

| Inhibitions | Circuit | Green |
|-------------|---------|-------|
| 2 (even) | Exp 0: Csy4 → CasE → green | ON |
| 3 (odd) | Exp 1: PgU → Csy4 → CasE → green | OFF |

---

## Experiment 2: AND Gate

### Input: CasE + Csy4 (both free)

This circuit has **two independent inputs** instead of a chain. Both CasE and Csy4 are free enzymes that converge on a single output.

```
INPUT 1
───────
CasE (free) ──inhibits──┐
                         ├──▶ mKO2 (from CasE_rec_Csy4_rec_mKO2)
Csy4 (free) ──inhibits──┘
───────
INPUT 2
```

### Step by step

1. **CasE** is produced freely (100 ng). No one can stop it.
2. **Csy4** is produced freely (100 ng). No one can stop it.
3. **mKO2's mRNA has BOTH `CasE_rec` AND `Csy4_rec`** — either enzyme alone is enough to cut it.
4. Both are present → mKO2 mRNA is doubly targeted → **orange is OFF**

For orange to turn ON, you'd need to remove **both** CasE and Csy4. This is why it's an AND gate: orange = (NOT CasE) AND (NOT Csy4).

### CSV

```
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ANDgate,X1,CasE,50,100
ANDgate,X1,eBFP2,50,100
ANDgate,X2,Csy4,50,100
ANDgate,X2,mNeonGreen,50,150
ANDgate,Output,CasE_rec_Csy4_rec_mKO2,50,200
```

### Part-by-part breakdown

| Part | What it encodes | Recognition site(s) on mRNA? | Who can cut it? | Result |
|------|----------------|------------------------------|-----------------|--------|
| CasE | CasE enzyme | None | Nobody | Always active |
| eBFP2 | Blue reporter | None | Nobody | Always glows blue |
| Csy4 | Csy4 enzyme | None | Nobody | Always active |
| mNeonGreen | Green reporter | None | Nobody | Always glows green |
| CasE_rec_Csy4_rec_mKO2 | mKO2 (orange) reporter | CasE_rec AND Csy4_rec | CasE or Csy4 (both present!) | Orange is suppressed |

### Expected result

| Reporter | Status | Why |
|----------|--------|-----|
| Blue (eBFP2) | ON | Constitutive control |
| Green (mNeonGreen) | ON | Constitutive control |
| Orange (mKO2) | **OFF** | Both CasE and Csy4 are cutting its mRNA |

### The AND gate truth table

| CasE present? | Csy4 present? | Orange (mKO2) |
|--------------|--------------|---------------|
| No | No | **ON** |
| Yes | No | OFF |
| No | Yes | OFF |
| Yes | Yes | OFF |

Orange is only ON when both inputs are absent — a logical AND on the absence of both.

---

## Why PgU is special

Notice that **PgU is the only ERN that can serve as the input to a 3-layer cascade**. Here's why:

| ERN | Can anything inhibit it? | Can it be a free input? |
|-----|-------------------------|------------------------|
| PgU | No — no `X_rec_PgU` part exists | Yes, always |
| CasE | Yes — `Csy4_rec_CasE` and `PgU_rec_CasE` exist | Only if Csy4 and PgU are absent |
| Csy4 | Yes — `CasE_rec_Csy4` and `PgU_rec_Csy4` exist | Only if CasE and PgU are absent |

PgU sits at the top of the hierarchy. It can inhibit others, but nothing can inhibit it. This makes it the natural "master switch" for the longest cascades.

---

## Side-by-side circuit diagrams

```
Experiment 0 (Default):        Experiment 1 (Three-Layer):

  Csy4                            PgU
    │                               │
    ▼ inhibits                      ▼ inhibits
  CasE (Csy4_rec_CasE)           Csy4 (PgU_rec_Csy4)
    │                               │
    ▼ inhibits                      ▼ inhibits
  mNeonGreen                      CasE (Csy4_rec_CasE)
  (CasE_rec_mNeonGreen)            │
                                    ▼ inhibits
  Result: Green ON                mNeonGreen
  (2 inhibitions = even)          (CasE_rec_mNeonGreen)

                                  Result: Green OFF
                                  (3 inhibitions = odd)


Experiment 2 (AND Gate):

  CasE ──inhibits──┐
                    ├──▶ mKO2 (CasE_rec_Csy4_rec_mKO2)
  Csy4 ──inhibits──┘

  Result: Orange OFF
  (either input alone is sufficient)
```

## Related

- [Biology Concepts](../background/biology-concepts.md) — How ERN inhibition works
- [Complete Parts Reference](../reference/complete-parts-reference.md) — All available plasmids
- [ERN Recognition Sequences](../reference/endoribonuclease-recognition-sequences.md) — The molecular hairpins behind `_rec_`
