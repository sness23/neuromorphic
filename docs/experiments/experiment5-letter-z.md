# Experiment 5: Letter Z — Maximum Complexity Circuits

## Goal

Go wild. Use as many parts as possible to create the most complex circuits we can, exploring different topologies to see what patterns the biocompiler predicts. Three circuits with increasing complexity, all designed to produce interesting heatmap patterns in the Predict tab.

## Circuits

### ZDual — Dual-Recognition AND Gate

The simplest of the three. Uses the `CasE_rec_Csy4_rec_mKO2` dual-recognition part where both CasE and Csy4 converge on the same output.

```
CasE (X1) ──inhibits──┐
                       ├──▶ mKO2 (orange) ── OFF when either is present
Csy4 (X2) ──inhibits──┘
           (CasE_rec_Csy4_rec_mKO2)
```

| Group | Contents | ng | Role |
|-------|----------|-----|------|
| X1 | CasE | 100 | Free ERN input #1 |
| X1 | eBFP2 | 50 | Blue marker (X-axis on heatmap) |
| X2 | Csy4 | 100 | Free ERN input #2 |
| X2 | mNeonGreen | 50 | Green marker (Y-axis on heatmap) |
| Bias | CasE_rec_Csy4_rec_mKO2 | 200 | Dual-rec output — either ERN kills it |
| Control | mMaroon1 | 150 | Transfection control |

**Total: 650 ng**

**Expected heatmap**: mKO2 should only be ON in the bottom-left corner (low X1 = low CasE, low X2 = low Csy4). Everywhere else at least one ERN is present to kill it. Should produce a bright corner fading to dark — like a quarter-circle or triangle.

---

### ZCross — Mutual Inhibition with Dual Output

The middle complexity circuit. Features **mutual cross-inhibition** between CasE and Csy4 (each inhibits the other via regulated versions), plus **two independent output reporters** both targeting mNeonGreen.

```
CasE (X1) ──inhibits──▶ Csy4 (from CasE_rec_Csy4, in X3)
    │                         │
    │                         ▼ inhibits
    │                    mNeonGreen (from Csy4_rec_mNeonGreen)
    │
    ▼ inhibits
mNeonGreen (from CasE_rec_mNeonGreen)

Csy4 (X2) ──inhibits──▶ CasE (from Csy4_rec_CasE, in X3)
    │
    ▼ inhibits
mNeonGreen (from Csy4_rec_mNeonGreen)
```

| Group | Contents | ng | Role |
|-------|----------|-----|------|
| X1 | CasE | 100 | Free ERN input #1 |
| X1 | eBFP2 | 50 | Blue marker (X-axis) |
| X2 | Csy4 | 100 | Free ERN input #2 |
| X2 | mMaroon1 | 50 | Maroon marker (Y-axis) |
| X3 | CasE_rec_Csy4 | 50 | CasE kills this extra Csy4 source |
| X3 | Csy4_rec_CasE | 50 | Csy4 kills this extra CasE source |
| Bias | CasE_rec_mNeonGreen | 100 | CasE inhibits this mNeonGreen |
| Bias | Csy4_rec_mNeonGreen | 100 | Csy4 inhibits this mNeonGreen |
| Control | mKO2 | 50 | Transfection control |

**Total: 650 ng**

**Key features:**
- **Mutual inhibition in X3**: CasE_rec_Csy4 provides extra Csy4 that CasE kills. Csy4_rec_CasE provides extra CasE that Csy4 kills. This creates a competitive toggle — whichever ERN (from X1/X2) is more abundant suppresses the other's reinforcement.
- **Dual output targeting**: Both CasE and Csy4 independently target mNeonGreen. Green is only ON when both are absent. The cross-inhibition in X3 adds a non-linear twist.
- **Expected heatmap**: Non-trivial pattern due to the feedback from X3. The cross-inhibition should create sharper transitions or asymmetric patterns compared to ZDual.

---

### ZFull — Maximum Complexity (All Three ERNs)

Uses **all three ERNs** (CasE, Csy4, PgU), **all four ERN→ERN wiring parts**, **two output reporters**, and **all four colors**. This is the most complex circuit possible with the available parts library.

```
                    PgU (X3) ──inhibits──▶ Csy4 (from PgU_rec_Csy4, in X3)
                       │
                       └──inhibits──▶ CasE (from PgU_rec_CasE, in X3)

CasE (X1) ──inhibits──▶ Csy4 (from CasE_rec_Csy4, in X4)
    │
    ▼ inhibits
mNeonGreen (from CasE_rec_mNeonGreen)

Csy4 (X2) ──inhibits──▶ CasE (from Csy4_rec_CasE, in X4)
    │
    ▼ inhibits
mNeonGreen (from Csy4_rec_mNeonGreen)
```

| Group | Contents | ng | Role |
|-------|----------|-----|------|
| X1 | CasE | 80 | Free ERN input #1 |
| X1 | mKO2 | 40 | Orange marker (X-axis) |
| X2 | Csy4 | 80 | Free ERN input #2 |
| X2 | eBFP2 | 40 | Blue marker (Y-axis) |
| X3 | PgU | 60 | Third ERN — free, always active |
| X3 | PgU_rec_Csy4 | 40 | PgU kills this Csy4 source |
| X3 | PgU_rec_CasE | 40 | PgU kills this CasE source |
| X4 | CasE_rec_Csy4 | 40 | CasE kills this Csy4 source |
| X4 | Csy4_rec_CasE | 40 | Csy4 kills this CasE source |
| Bias | CasE_rec_mNeonGreen | 60 | CasE inhibits mNeonGreen |
| Bias | Csy4_rec_mNeonGreen | 60 | Csy4 inhibits mNeonGreen |
| Control | mMaroon1 | 70 | Transfection control |

**Total: 650 ng**

**Key features:**
- **All 3 ERNs active**: PgU is always active (no one targets it). CasE and Csy4 vary with X1/X2.
- **Triple-layered inhibition network**:
  - X3: PgU suppresses backup copies of both CasE and Csy4
  - X4: CasE and Csy4 mutually suppress each other's backup copies
  - The net effect of CasE/Csy4 depends on the X1/X2 inputs PLUS the cross-inhibition from X3/X4
- **All 4 ERN→ERN parts used**: PgU_rec_Csy4, PgU_rec_CasE, CasE_rec_Csy4, Csy4_rec_CasE
- **All 4 colors used**: mKO2 (X1), eBFP2 (X2), mNeonGreen (output), mMaroon1 (control)
- **Expected heatmap**: Complex non-linear pattern. PgU in X3 is always present and kills the backup ERN copies, making the X3 group mostly inert. But the X4 mutual inhibition adds an extra competitive layer on top of the direct X1/X2 effects. Should produce a more complex shape than ZCross.

## Parts Inventory

All parts used across the three circuits:

| Category | Parts Used | Count |
|----------|-----------|-------|
| ERNs | CasE, Csy4, PgU | 3/3 |
| ERN→ERN | PgU_rec_Csy4, PgU_rec_CasE, Csy4_rec_CasE, CasE_rec_Csy4 | 4/4 |
| ERN→Color | CasE_rec_mNeonGreen, Csy4_rec_mNeonGreen, CasE_rec_Csy4_rec_mKO2 | 3/4 |
| Colors | mKO2, eBFP2, mMaroon1, mNeonGreen | 4/4 |
| **Total unique parts** | | **14/15** |

The only part NOT used is `PgU_rec_mNeonGreen` (PgU inhibiting a fluorescent reporter is not supported by the prediction model).

## How to Use

1. Upload `experiments/inputs/letter-z.csv` in the **Build** tab
2. Switch to the **Predict** tab
3. Select each circuit (ZDual, ZCross, ZFull) from the dropdown
4. Click **Predict** to see the heatmap for each

Each heatmap shows predicted fluorescence as X1 and X2 input levels vary across a 32x32 grid. The topology of the circuit determines the shape of the response surface.

## Input CSV

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
ZDual,X1,CasE,50,100
ZDual,X1,eBFP2,50,50
ZDual,X2,Csy4,50,100
ZDual,X2,mNeonGreen,50,50
ZDual,Bias,CasE_rec_Csy4_rec_mKO2,50,200
ZDual,Control,mMaroon1,50,150
ZCross,X1,CasE,50,100
ZCross,X1,eBFP2,50,50
ZCross,X2,Csy4,50,100
ZCross,X2,mMaroon1,50,50
ZCross,X3,CasE_rec_Csy4,50,50
ZCross,X3,Csy4_rec_CasE,50,50
ZCross,Bias,CasE_rec_mNeonGreen,50,100
ZCross,Bias,Csy4_rec_mNeonGreen,50,100
ZCross,Control,mKO2,50,50
ZFull,X1,CasE,50,80
ZFull,X1,mKO2,50,40
ZFull,X2,Csy4,50,80
ZFull,X2,eBFP2,50,40
ZFull,X3,PgU,50,60
ZFull,X3,PgU_rec_Csy4,50,40
ZFull,X3,PgU_rec_CasE,50,40
ZFull,X4,CasE_rec_Csy4,50,40
ZFull,X4,Csy4_rec_CasE,50,40
ZFull,Bias,CasE_rec_mNeonGreen,50,60
ZFull,Bias,Csy4_rec_mNeonGreen,50,60
ZFull,Control,mMaroon1,50,70
```
