# Complete Parts Reference

## How to Read Part Names

The naming convention tells you the inhibition relationship:

- **`A_rec_B`** = "B's mRNA has a recognition sequence for A" = "A inhibits B" = "if A is present, B is destroyed"
- **`A_rec_B_rec_C`** = "C's mRNA has recognition sequences for both A and B" = "either A or B can destroy C"

The word "rec" stands for "recognition sequence."

## All Available Parts

### Category 1: ERNs (Endoribonucleases)

These are standalone enzymes. Their mRNA has no engineered recognition sequences, so no other ERN can inhibit them. They are always active when expressed.

| Part Name | What it is | What it does |
|-----------|-----------|-------------|
| `CasE` | CRISPR-associated endoribonuclease | Scans all mRNA in the cell. Cuts any mRNA that contains a CasE recognition sequence. |
| `Csy4` | CRISPR-associated endoribonuclease | Scans all mRNA in the cell. Cuts any mRNA that contains a Csy4 recognition sequence. |
| `PgU` | Endoribonuclease | Scans all mRNA in the cell. Cuts any mRNA that contains a PgU recognition sequence. |

**Usage:** These are your "free" inputs. They are always ON. Use them as the starting signal in a cascade, or as inputs to a logic gate.

### Category 2: ERN_rec_ERN (Regulated Enzymes)

These encode an ERN enzyme, but the mRNA has a recognition sequence for another ERN. The encoded enzyme is only active if its inhibitor is absent.

| Part Name | Encodes | Inhibited by | Meaning |
|-----------|---------|-------------|---------|
| `PgU_rec_Csy4` | PgU enzyme | Csy4 | If Csy4 is present, PgU is not produced. If Csy4 is absent, PgU is produced and active. |
| `PgU_rec_CasE` | PgU enzyme | CasE | If CasE is present, PgU is not produced. If CasE is absent, PgU is produced and active. |
| `Csy4_rec_CasE` | Csy4 enzyme | CasE | If CasE is present, Csy4 is not produced. If CasE is absent, Csy4 is produced and active. |
| `CasE_rec_Csy4` | CasE enzyme | Csy4 | If Csy4 is present, CasE is not produced. If Csy4 is absent, CasE is produced and active. |

**Usage:** These create inhibitory wiring between ERNs. They are the "connections" in your neural network. Chain them together to create cascades.

**Note:** There is no `Csy4_rec_PgU` or `CasE_rec_PgU` in the library. PgU cannot directly inhibit another ERN — it can only inhibit reporters (mNeonGreen). This constrains which cascade topologies are possible.

### Category 3: ERN_rec_Color (Regulated Reporters)

These encode a fluorescent protein, but the mRNA has one or more recognition sequences. The reporter is only visible if all its inhibitors are absent.

| Part Name | Color | Inhibited by | Meaning |
|-----------|-------|-------------|---------|
| `Csy4_rec_mNeonGreen` | Green | Csy4 | Green is OFF if Csy4 is present. |
| `CasE_rec_mNeonGreen` | Green | CasE | Green is OFF if CasE is present. |
| `PgU_rec_mNeonGreen` | Green | PgU | Green is OFF if PgU is present. |
| `CasE_rec_Csy4_rec_mKO2` | Orange | CasE OR Csy4 | Orange is OFF if CasE is present OR if Csy4 is present OR if both are present. Orange is only ON if BOTH are absent. |

**Usage:** These are your circuit outputs — the visible readout. Choose which ERN controls which color to match your circuit design.

**Special note on `CasE_rec_Csy4_rec_mKO2`:** This is the only dual-recognition part in the library. It implements an AND gate on the absence of two inputs. It's the most complex single part available.

### Category 4: Colors (Unregulated Reporters)

These encode a fluorescent protein with no recognition sequences. No ERN can inhibit them. They are always ON when expressed.

| Part Name | Color | Wavelength range |
|-----------|-------|-----------------|
| `mKO2` | Orange | Ex: 551 nm, Em: 565 nm |
| `eBFP2` | Blue | Ex: 383 nm, Em: 448 nm |
| `mMaroon1` | Maroon/Red | Ex: 609 nm, Em: 657 nm |
| `mNeonGreen` | Green | Ex: 506 nm, Em: 517 nm |

**Usage:** Use as transfection controls. If these are visible, the cells received DNA and are expressing it. If these are dark, something went wrong with transfection.

## Inhibition Map

A complete map of who can inhibit whom:

```
                    ┌─── can be inhibited by ───┐
                    │                            │
Inhibitor:      CasE           Csy4            PgU
                 │              │               │
Can inhibit:     ├─ Csy4        ├─ CasE         ├─ mNeonGreen
                 │  (Csy4_rec_  │  (CasE_rec_   │  (PgU_rec_
                 │   CasE)      │   Csy4)        │   mNeonGreen)
                 │              │               │
                 ├─ PgU         ├─ PgU          └─ (nothing else)
                 │  (PgU_rec_   │  (PgU_rec_
                 │   CasE)      │   Csy4)
                 │              │
                 ├─ mNeonGreen  ├─ mNeonGreen
                 │  (CasE_rec_  │  (Csy4_rec_
                 │   mNeonGreen)│   mNeonGreen)
                 │              │
                 └─ mKO2        └─ mKO2
                    (CasE_rec_     (CasE_rec_
                     Csy4_rec_      Csy4_rec_
                     mKO2)          mKO2)
```

Note:
- CasE and Csy4 are the most versatile — each can inhibit 2 other ERNs and 2 reporters
- PgU can only inhibit 1 reporter (mNeonGreen) — it cannot inhibit other ERNs
- mKO2 can only be inhibited by the dual-recognition part (requiring both CasE and Csy4 recognition sequences)
- mMaroon1 has no regulated version — it can only be used as a constitutive control

## Possible Circuit Topologies

Given the constraints of the parts library:

### 2-Layer Cascades
1. CasE → Csy4 → mNeonGreen (via Csy4_rec_CasE, Csy4_rec_mNeonGreen) — green ON
2. CasE → PgU → mNeonGreen (via PgU_rec_CasE, PgU_rec_mNeonGreen) — green ON
3. Csy4 → CasE → mNeonGreen (via CasE_rec_Csy4, CasE_rec_mNeonGreen) — green ON
4. Csy4 → PgU → mNeonGreen (via PgU_rec_Csy4, PgU_rec_mNeonGreen) — green ON

### 3-Layer Cascades
5. CasE → Csy4 → PgU → mNeonGreen — green OFF (our Circuit 1)
6. Csy4 → CasE → PgU → mNeonGreen — green OFF (mirror of #5, using CasE_rec_Csy4 instead)

Note: You cannot make a cascade longer than 3 because PgU has no way to inhibit another ERN.

### Convergent (AND gate)
7. CasE + Csy4 → mKO2 (via CasE_rec_Csy4_rec_mKO2) — our Circuit 2

### Direct Inhibition
8. CasE → mNeonGreen (via CasE_rec_mNeonGreen) — green OFF
9. Csy4 → mNeonGreen (via Csy4_rec_mNeonGreen) — green OFF
10. PgU → mNeonGreen (via PgU_rec_mNeonGreen) — green OFF
