# Flow Cytometry Readout

How the Predict heatmap connects to actual experimental results.

## What Flow Cytometry Measures

A flow cytometer passes thousands of individual cells through a laser beam, one at a time. For each cell, it measures fluorescence intensity in multiple channels simultaneously. In a single run you get data for 10,000–100,000 cells, each with a readout for every fluorescent protein:

| Channel | Fluorescent Protein | Wavelength Range |
|---------|-------------------|-----------------|
| Blue | eBFP2 | ~380–450 nm |
| Green | mNeonGreen | ~500–550 nm |
| Orange | mKO2 | ~550–600 nm |
| Red/Maroon | mMaroon1 | ~650–700 nm |

Each cell produces a row of data: `(eBFP2_intensity, mNeonGreen_intensity, mKO2_intensity, mMaroon1_intensity)`.

## Why Each Cell is a Different Experiment

Lipofection is stochastic. When you deliver DNA via Lipofectamine, each cell receives a **random amount** of each transfection group. Across a population of thousands of cells:

- Some cells got lots of X1, little X2
- Some got little X1, lots of X2
- Some got moderate amounts of both
- Some got very little of either
- Every combination in between

This variability is not noise — it is the **signal**. Each cell is effectively a separate experiment run at a different (X1, X2) input level. Flow cytometry reads them all in a few minutes.

## The Markers Are Input Proxies

The fluorescent markers in X1 and X2 are not just transfection controls — they are **quantitative proxies** for how much of each input group a given cell received.

| Marker | In Group | What It Tells You |
|--------|----------|-------------------|
| eBFP2 | X1 | How much X1 this cell received (including the ERN in X1) |
| mMaroon1 | X2 | How much X2 this cell received (including the ERN in X2) |

Because the marker and the ERN are co-transfected in the same group at a fixed DNA ratio, they enter cells together. A cell with bright eBFP2 necessarily received a lot of the X1 group — meaning it also received a lot of whatever ERN (e.g., CasE) is in X1.

The marker intensities are direct, measurable surrogates for ERN concentration inside each cell.

## Reconstructing the 2D Heatmap from Flow Data

The Predict tab's heatmap shows predicted output fluorescence as a function of X1 and X2 input levels on a 32×32 grid. The same plot can be reconstructed from experimental flow cytometry data:

### Step 1: Collect Raw Data

Flow cytometry produces a table with one row per cell:

```
Cell    eBFP2    mMaroon1    mNeonGreen    mKO2
1       1204     892         3401          105
2       503      2105        210           98
3       2890     1544        1820          112
4       156      301         4502          95
...     ...      ...         ...           ...
50000   1677     1033        2244          101
```

### Step 2: Define the Axes

- **X-axis**: eBFP2 intensity (proxy for X1 input level)
- **Y-axis**: mMaroon1 intensity (proxy for X2 input level)

Both axes are typically log-scaled, since fluorescence intensities span several orders of magnitude.

### Step 3: Bin Cells into a Grid

Divide the (eBFP2, mMaroon1) space into a grid (e.g., 32×32 bins). Assign each cell to a bin based on its marker intensities.

```
         low eBFP2 ──────────────────► high eBFP2
high    ┌────┬────┬────┬────┬────┐
mMaroon │ 42 │ 38 │ 55 │ 61 │ 23 │  ← number of cells in each bin
        ├────┼────┼────┼────┼────┤
        │ 67 │ 89 │102 │ 95 │ 44 │
        ├────┼────┼────┼────┼────┤
        │ 53 │120 │156 │133 │ 71 │
        ├────┼────┼────┼────┼────┤
low     │ 31 │ 58 │ 84 │ 72 │ 39 │
mMaroon └────┴────┴────┴────┴────┘
```

### Step 4: Average the Output in Each Bin

For each bin, compute the mean mNeonGreen (or mKO2) intensity of all cells in that bin. This gives the experimental output at each (X1, X2) input level.

```
         low eBFP2 ──────────────────► high eBFP2
high    ┌──────┬──────┬──────┬──────┬──────┐
mMaroon │  120 │  340 │  580 │  890 │ 1200 │  ← mean mNeonGreen
        ├──────┼──────┼──────┼──────┼──────┤      intensity per bin
        │  150 │  410 │  720 │ 1100 │ 1450 │
        ├──────┼──────┼──────┼──────┼──────┤
        │  200 │  550 │  980 │ 1400 │ 1800 │
        ├──────┼──────┼──────┼──────┼──────┤
low     │  280 │  700 │ 1300 │ 1900 │ 2400 │
mMaroon └──────┴──────┴──────┴──────┴──────┘
```

### Step 5: Plot as Heatmap

Render the grid as a color-mapped heatmap. This is the experimental equivalent of the Predict tab's output.

## Predict vs Experiment: Side-by-Side

```
    Predict (biocompiler model)          Experiment (flow cytometry)
┌─────────────────────────┐        ┌─────────────────────────┐
│                         │        │                         │
│   X-axis: X1 level      │        │   X-axis: eBFP2         │
│   Y-axis: X2 level      │        │   Y-axis: mMaroon1      │
│   Color:  predicted      │        │   Color:  measured       │
│           fluorescence   │        │           fluorescence   │
│                         │        │                         │
│   Source: neural network │        │   Source: 50,000 cells   │
│           model          │        │           each a data pt │
│                         │        │                         │
└─────────────────────────┘        └─────────────────────────┘
```

The Predict heatmap is the **theoretical prediction**. The flow cytometry heatmap is the **experimental validation**. If the circuit works as designed, the two should match.

## Why This Design Works

The experimental design exploits three properties:

1. **Stochastic transfection**: Each cell receives a random dose, providing natural variation across the entire 2D input space without needing to prepare separate wells for each input combination.

2. **Co-transfection correlation**: Plasmids in the same group enter cells together. The marker (eBFP2, mMaroon1) intensity reliably tracks the ERN concentration in the same group.

3. **Multi-channel flow cytometry**: Simultaneous measurement of all fluorescent proteins in each cell allows reconstruction of the input-output relationship from a single well.

A traditional approach would require preparing a separate well for every (X1, X2) combination — a 32×32 grid would need 1,024 wells. Instead, this design gets the full 2D map from **one well** by letting biology do the sampling.

## Practical Considerations

### Cell Count per Bin

With 50,000 cells across a 32×32 grid (1,024 bins), you average ~49 cells per bin. Corner bins (extreme high/low transfection) may have fewer cells, making those regions noisier. Central bins (moderate transfection) tend to be the most populated and therefore the most reliable.

### Gating

Before analysis, cells are "gated" — filtered to remove:
- Dead cells (identified by scatter properties or viability dyes)
- Untransfected cells (no fluorescence in any channel)
- Doublets (two cells stuck together, which distort the measurement)

### Compensation

Because fluorescent protein emission spectra overlap, the cytometer applies **compensation** — a mathematical correction that subtracts spectral bleed-through between channels. This ensures that eBFP2 signal doesn't contaminate the mNeonGreen channel and vice versa.

### Dynamic Range

The markers and output should have comparable intensity ranges. If the output reporter is much dimmer than the markers, it will be hard to distinguish signal from noise. This is why output parts often get higher DNA amounts (e.g., 200 ng) — to ensure the fluorescence is strong enough to measure reliably above background.
