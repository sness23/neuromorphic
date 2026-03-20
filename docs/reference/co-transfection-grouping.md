# Co-Transfection Grouping

How plasmids in the same transfection group end up together inside cells, and why groups are independent from each other.

## The Physical Mechanism

Plasmids in the same transfection group are **physically mixed in the same tube** before Lipofectamine wraps them into nanoparticles. This is not a logical grouping — it is a physical one, enforced by the liquid handling protocol.

### Step by Step

**1. DNA Mixing**

The OT-2 robot pipettes all plasmids belonging to the same group into a single destination tube:

```
Source tubes                    Destination tube
┌──────────┐
│  CasE    │──── 2.4 µL ────┐
│  (X1)    │                 │
└──────────┘                 ▼
                        ┌──────────┐
                        │  X1 mix  │  ← CasE + eBFP2 DNA
                        │          │     in the same tube
┌──────────┐            └──────────┘
│  eBFP2   │──── 1.2 µL ────┘
│  (X1)    │
└──────────┘
```

Plasmids in different groups go to different tubes:

```
CasE + eBFP2     →  Tube B1  (Group X1)
Csy4 + mMaroon1  →  Tube B2  (Group X2)
CasE_rec_Csy4    →  Tube B3  (Group X3)
```

This is why plasmids in the same group share the same `DNA destination` value in the experiment config CSV.

**2. Lipid Nanoparticle Formation**

Opti-MEM, P3000, and L3000 are added to each tube separately. The Lipofectamine reagent self-assembles around whatever DNA is in the tube, forming lipid nanoparticles.

```
Tube B1 (CasE + eBFP2 DNA)
    + Opti-MEM + P3000
    + L3000
    ──────────────────►  Nanoparticles containing BOTH CasE and eBFP2
```

Each nanoparticle is a tiny lipid bubble (50–200 nm) carrying copies of all the plasmids that were in its tube. A nanoparticle from the X1 tube carries CasE DNA and eBFP2 DNA together.

**3. Delivery to Cells**

All nanoparticle tubes are pipetted onto the same well of cells:

```
X1 nanoparticles (CasE + eBFP2)    ──►  ┌─────────────┐
                                         │             │
X2 nanoparticles (Csy4 + mMaroon1) ──►  │  HEK293     │
                                         │  cells      │
X3 nanoparticles (CasE_rec_Csy4)   ──►  │             │
                                         └─────────────┘
```

Each cell absorbs a random number of nanoparticles from each group. The nanoparticles fuse with the cell membrane and release their DNA cargo inside.

## Correlation Within Groups, Independence Between Groups

This physical process creates two essential statistical properties:

### Within a group: Correlated

A cell that absorbs many X1 nanoparticles gets a lot of CasE AND a lot of eBFP2, because they are in the same particles. A cell that absorbs few X1 nanoparticles gets little of both.

```
Cell A:  absorbed 20 X1 nanoparticles  →  high CasE,  high eBFP2
Cell B:  absorbed 3 X1 nanoparticles   →  low CasE,   low eBFP2
Cell C:  absorbed 10 X1 nanoparticles  →  med CasE,   med eBFP2
```

The ratio of CasE to eBFP2 inside each cell matches the ratio in the tube (set by DNA amounts in the CSV). The absolute amount varies cell-to-cell, but the ratio is constant.

This is why eBFP2 intensity is a reliable **proxy** for CasE concentration in each cell. Measuring one tells you the other.

### Between groups: Independent

X1 nanoparticles and X2 nanoparticles are separate objects. They enter cells independently. A cell that absorbs many X1 nanoparticles does not necessarily absorb many or few X2 nanoparticles — the two are uncorrelated.

```
Cell A:  20 X1 particles, 5 X2 particles   →  high CasE, low Csy4
Cell B:  3 X1 particles, 18 X2 particles   →  low CasE,  high Csy4
Cell C:  10 X1 particles, 12 X2 particles  →  med CasE,  med Csy4
Cell D:  15 X1 particles, 14 X2 particles  →  high CasE, high Csy4
Cell E:  2 X1 particles, 3 X2 particles    →  low CasE,  low Csy4
```

Across thousands of cells, every combination of (X1 level, X2 level) is naturally sampled.

## Why This Matters for the Heatmap

The combination of within-group correlation and between-group independence is what makes the 2D heatmap possible from a single well:

```
                    ┌─────────────────────────────────────┐
                    │  Each cell = one point in 2D space   │
                    │                                     │
  high eBFP2       │  ●          ●    ●                  │
  (high X1)        │     ●    ●          ●   ●           │
                    │  ●     ●     ●  ●     ●            │
                    │    ●  ●   ●    ●   ●      ●        │
  low eBFP2        │       ●  ●   ●       ●             │
  (low X1)         │  ●         ●      ●                 │
                    └─────────────────────────────────────┘
                    low mMaroon1                high mMaroon1
                    (low X2)                    (high X2)
```

- **X-axis** (eBFP2): proxy for X1 input level — correlated with the ERN in X1
- **Y-axis** (mMaroon1): proxy for X2 input level — correlated with the ERN in X2
- **Color of each dot**: mNeonGreen intensity — the circuit output

The cells fill the 2D space because X1 and X2 are independent. If they were correlated (e.g., all plasmids in one tube), every cell would lie along a diagonal and you would only get a 1D slice, not a 2D map.

## What Would Break This

### If all plasmids were in one group

Putting everything in a single tube means all plasmids are correlated. A cell that gets a lot of DNA gets a lot of everything. You lose the ability to independently vary X1 and X2.

```
One group: CasE + eBFP2 + Csy4 + mMaroon1 + output

→ All intensities scale together
→ Only a 1D diagonal in the 2D space
→ Cannot reconstruct the full 2D heatmap
```

### If markers were in the wrong group

If eBFP2 were in X2 instead of X1, it would track Csy4 levels rather than CasE levels. The axes of the heatmap would be swapped, and the interpretation would be wrong.

### If a marker were unregulated in a separate group

A marker in its own group (e.g., mKO2 in a Control group) varies independently of both X1 and X2. It does not track any input and cannot serve as an axis for the heatmap. This is why the biocompiler API rejects free markers outside X1/X2 — they would add a third input dimension that the 2D heatmap cannot represent.

## Summary

| Property | Mechanism | Consequence |
|----------|-----------|-------------|
| Within-group correlation | Plasmids mixed in same tube, wrapped in same nanoparticles | Marker intensity tracks ERN concentration |
| Between-group independence | Separate tubes, separate nanoparticles, random uptake | Cells sample the full 2D input space |
| Stochastic transfection | Each cell absorbs a random number of particles | Thousands of cells = thousands of different (X1, X2) combinations |
| Multi-channel cytometry | Simultaneous measurement of all fluorescent proteins | One cell = one data point with (input1, input2, output) |

The transfection grouping is not just an organizational convenience — it is the foundation of the entire measurement strategy. The physical act of mixing plasmids in the same tube creates the correlation that makes markers work as input proxies, and the physical separation of groups creates the independence that makes the 2D heatmap possible.
