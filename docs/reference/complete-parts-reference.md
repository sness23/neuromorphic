# Complete Parts Reference

## How to Read Part Names

The naming convention tells you the inhibition relationship:

- **`X_rec_Y`** = "Y's mRNA has a recognition sequence for X" = "X inhibits Y" = "if X is present, Y is destroyed"
- **`X_rec_Y_rec_Z`** = "Z's mRNA has recognition sequences for both X and Y" = "either X or Y can destroy Z"

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

These encode an ERN enzyme, but the mRNA has a recognition sequence for another ERN. The encoded enzyme is only active if its inhibitor is absent. The naming convention is `X_rec_Y`: X is the inhibitor, Y is the encoded protein.

| Part Name | Encodes | Inhibited by | Meaning |
|-----------|---------|-------------|---------|
| `PgU_rec_Csy4` | Csy4 enzyme | PgU | If PgU is present, Csy4 is not produced. If PgU is absent, Csy4 is produced and active. |
| `PgU_rec_CasE` | CasE enzyme | PgU | If PgU is present, CasE is not produced. If PgU is absent, CasE is produced and active. |
| `Csy4_rec_CasE` | CasE enzyme | Csy4 | If Csy4 is present, CasE is not produced. If Csy4 is absent, CasE is produced and active. |
| `CasE_rec_Csy4` | Csy4 enzyme | CasE | If CasE is present, Csy4 is not produced. If CasE is absent, Csy4 is produced and active. |

**Usage:** These create inhibitory wiring between ERNs. They are the "connections" in your neural network. Chain them together to create cascades.

**Note:** There is no part where PgU is the encoded protein being inhibited by another ERN. PgU can only appear as an inhibitor (in `PgU_rec_Csy4` and `PgU_rec_CasE`) or as a free enzyme. This constrains which cascade topologies are possible.

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
Inhibitor:      PgU            CasE            Csy4
                 │              │               │
Can inhibit:     ├─ Csy4        ├─ Csy4         ├─ CasE
                 │  (PgU_rec_   │  (CasE_rec_   │  (Csy4_rec_
                 │   Csy4)      │   Csy4)        │   CasE)
                 │              │               │
                 ├─ CasE        ├─ mNeonGreen   ├─ mNeonGreen
                 │  (PgU_rec_   │  (CasE_rec_   │  (Csy4_rec_
                 │   CasE)      │   mNeonGreen)  │   mNeonGreen)
                 │              │               │
                 ├─ mNeonGreen  └─ mKO2         └─ mKO2
                 │  (PgU_rec_      (CasE_rec_      (CasE_rec_
                 │   mNeonGreen)    Csy4_rec_       Csy4_rec_
                 │                  mKO2)           mKO2)
                 └─ (nothing else)
```

Note:
- PgU can inhibit 2 other ERNs (Csy4, CasE) and 1 reporter (mNeonGreen)
- CasE can inhibit 1 other ERN (Csy4) and 2 reporters (mNeonGreen, mKO2)
- Csy4 can inhibit 1 other ERN (CasE) and 2 reporters (mNeonGreen, mKO2)
- PgU cannot be inhibited by any ERN — it can only be used as a free enzyme
- mKO2 can only be inhibited by the dual-recognition part (requiring both CasE and Csy4 recognition sequences)
- mMaroon1 has no regulated version — it can only be used as a constitutive control

## Possible Circuit Topologies

Given the constraints of the parts library:

### 2-Layer Cascades
1. Csy4 → CasE → mNeonGreen (via Csy4_rec_CasE, CasE_rec_mNeonGreen) — green ON
2. CasE → Csy4 → mNeonGreen (via CasE_rec_Csy4, Csy4_rec_mNeonGreen) — green ON
3. PgU → CasE → mNeonGreen (via PgU_rec_CasE, CasE_rec_mNeonGreen) — green ON
4. PgU → Csy4 → mNeonGreen (via PgU_rec_Csy4, Csy4_rec_mNeonGreen) — green ON

### 3-Layer Cascades
5. PgU → Csy4 → CasE → mNeonGreen — green OFF (our Circuit 1)
6. PgU → CasE → Csy4 → mNeonGreen — green OFF (mirror of #5, using PgU_rec_CasE and CasE_rec_Csy4 instead)

Note: You cannot make a cascade longer than 3 because PgU cannot be inhibited by any ERN, so it must always be the free input at the start of the chain.

### Convergent (AND gate)
7. CasE + Csy4 → mKO2 (via CasE_rec_Csy4_rec_mKO2) — our Circuit 2

### Direct Inhibition
8. CasE → mNeonGreen (via CasE_rec_mNeonGreen) — green OFF
9. Csy4 → mNeonGreen (via Csy4_rec_mNeonGreen) — green OFF
10. PgU → mNeonGreen (via PgU_rec_mNeonGreen) — green OFF
