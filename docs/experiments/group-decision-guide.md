# Circuit Design Options for HTGAA Week 7

## Quick Refresher

We're building a circuit inside living cells using three tools:
- **ERN enzymes** (Csy4, CasE, PgU) that destroy specific mRNA, preventing proteins from being made
- **Wiring parts** that connect ERNs to each other (e.g., `Csy4_rec_CasE` means Csy4 destroys CasE)
- **Fluorescent reporters** (green, orange, blue, maroon) so we can see what's happening

The naming rule: **`A_rec_B`** means "A destroys B." If A is present, B gets shut off.

Total DNA budget: **650 ng max.**

---

## Option A: Three-Layer Cascade (Recommended)

**Concept:** Chain all 3 ERNs together. The longest possible inhibition chain with our parts.

```
CasE ──kills──▶ Csy4 ──kills──▶ PgU ──kills──▶ mNeonGreen (green)
```

Three inhibitions = green is **OFF**. (Odd number of negatives = negative.)

**What we'd put in the cells:**

| Group | Plasmid | Amount | Role |
|-------|---------|--------|------|
| X1 | CasE | 150 ng | Input enzyme |
| X1 | eBFP2 | 50 ng | Blue control light |
| X2 | Csy4_rec_CasE | 100 ng | Csy4, killed by CasE |
| X2 | mMaroon1 | 50 ng | Maroon control light |
| X3 | PgU_rec_Csy4 | 100 ng | PgU, killed by Csy4 |
| Bias | PgU_rec_mNeonGreen | 200 ng | Green, killed by PgU |

**Expected result:** Blue ON, Maroon ON, Green **OFF**

**Why it's interesting:** Pairs with the default 2-layer circuit (green ON) as a direct comparison. Adding one more layer flips the output. Demonstrates that even vs. odd inhibition steps produce opposite results.

---

## Option B: AND Gate

**Concept:** Use the special part `CasE_rec_Csy4_rec_mKO2` — orange only turns on if **both** CasE and Csy4 are absent. Either one alone can shut it off.

```
CasE ──kills──┐
              ├──▶ mKO2 (orange)
Csy4 ──kills──┘
```

We include both ERNs, so orange is **OFF**.

| Group | Plasmid | Amount | Role |
|-------|---------|--------|------|
| X1 | CasE | 100 ng | Inhibitor 1 |
| X2 | Csy4 | 100 ng | Inhibitor 2 |
| Output | CasE_rec_Csy4_rec_mKO2 | 200 ng | Orange, killed by either |
| Control | eBFP2 | 100 ng | Blue control light |
| Control | mNeonGreen | 150 ng | Green control light |

**Expected result:** Blue ON, Green ON, Orange **OFF**

**Why it's interesting:** Demonstrates a biological AND gate — a fundamental logic element. Orange can only turn on when both inhibitors are removed, not just one.

---

## Option C: Competing Inhibitors

**Concept:** One dominant ERN (CasE, high dose) controls the whole network. It kills both Csy4 and the green output directly.

```
CasE (strong) ──kills──▶ Csy4 (weak, dies)
              ──kills──▶ mNeonGreen (green, OFF)

Csy4 (dead) ──can't kill──▶ PgU (survives, but has nothing to do)
```

| Group | Plasmid | Amount | Role |
|-------|---------|--------|------|
| X1 | CasE | 200 ng | Dominant enzyme |
| X1 | eBFP2 | 50 ng | Blue control light |
| X2 | Csy4_rec_CasE | 100 ng | Csy4, killed by CasE |
| X2 | mMaroon1 | 50 ng | Maroon control light |
| X3 | PgU_rec_Csy4 | 100 ng | PgU, freed because Csy4 is dead |
| Bias | CasE_rec_mNeonGreen | 150 ng | Green, killed by CasE |

**Expected result:** Blue ON, Maroon ON, Green **OFF**

**Why it's interesting:** Shows that dosage (ng amounts) determines who wins. You could run a second experiment with CasE reduced to 50 ng to see if the outcome changes — demonstrating the analog nature of the circuit.

---

## Option D: Double Negative + AND Gate

**Concept:** Combine a CasE→Csy4 inhibition chain with the AND gate output, plus three constitutive controls.

```
CasE ──kills──▶ Csy4

CasE ──kills──┐
              ├──▶ mKO2 (orange, OFF)
Csy4 (dead) ──┘
```

| Group | Plasmid | Amount | Role |
|-------|---------|--------|------|
| X1 | CasE | 150 ng | Input enzyme |
| X2 | Csy4_rec_CasE | 100 ng | Csy4, killed by CasE |
| Output | CasE_rec_Csy4_rec_mKO2 | 150 ng | Orange AND gate |
| Control1 | eBFP2 | 100 ng | Blue control light |
| Control2 | mMaroon1 | 50 ng | Maroon control light |
| Control3 | mNeonGreen | 100 ng | Green control light |

**Expected result:** Blue ON, Maroon ON, Green ON, Orange **OFF**

**Why it's interesting:** Most complex design — combines a chain with an AND gate. Three control colors give strong confirmation that transfection worked. CasE alone is enough to keep orange off even though Csy4 is already dead.

---

## Comparison

| | ERNs Used | Predicted Output | Complexity | Best Paired With |
|---|-----------|-----------------|------------|-----------------|
| **A: Cascade** | All 3 | Green OFF | Medium | Default circuit (green ON) |
| **B: AND Gate** | 2 | Orange OFF | Simple | Control with 0 or 1 ERN |
| **C: Competing** | All 3 | Green OFF | Medium | Same circuit, lower CasE dose |
| **D: Double+AND** | 2 (1 regulated) | Orange OFF | High | Control without CasE |

## Recommendation

**Option A** is the strongest choice:
- Uses all 3 available ERNs (most ambitious)
- Clear predicted outcome (green OFF)
- Direct comparison with the default circuit (green ON) — same output gene, opposite result
- Easy to explain: "we added a third layer and it flipped the answer"
