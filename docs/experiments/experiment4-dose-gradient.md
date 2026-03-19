# Experiment 4: CasE Dose-Response Gradient

## Concept

Demonstrate the **analog nature** of ERN inhibition by varying CasE concentration across columns while keeping the target (CasE_rec_mNeonGreen) constant. This reveals the dose-response curve of a single inhibitory connection — the fundamental building block of every neuromorphic circuit.

All 24 wells are filled. Each column gets a different CasE dose. Each row is a biological replicate (4 replicates per dose). Blue (eBFP2) in every well serves as transfection control.

## The Pattern

```
Green channel (expected intensity gradient):
     Col 1    Col 2    Col 3    Col 4    Col 5    Col 6
     0 ng     25 ng    50 ng    75 ng    100 ng   150 ng   ← CasE dose
A  [BRIGHT] [ dim? ] [ dim  ] [ dim  ] [ dark ] [ DARK ]
B  [BRIGHT] [ dim? ] [ dim  ] [ dim  ] [ dark ] [ DARK ]
C  [BRIGHT] [ dim? ] [ dim  ] [ dim  ] [ dark ] [ DARK ]
D  [BRIGHT] [ dim? ] [ dim  ] [ dim  ] [ dark ] [ DARK ]

Blue channel (uniform control):
     1     2     3     4     5     6
A  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
B  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
C  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
D  [ ON] [ ON] [ ON] [ ON] [ ON] [ ON]
```

The exact brightness at each dose is unknown — that's what this experiment measures!

## Why This Matters

In digital electronics, signals are binary (0 or 1). In neuromorphic computing, signals are **analog** — the strength of inhibition depends on how much enzyme is present. This experiment maps out the transfer function of a single ERN-to-target connection:

```
                    Green fluorescence
                    ▲
           BRIGHT ──┤ ●
                    │   ●
                    │     ●
                    │       ● ← Where does the threshold sit?
                    │         ●
             DARK ──┤           ● ● ●
                    └──┬──┬──┬──┬──┬──▶ CasE dose (ng)
                       0  25 50 75 100 150
```

The shape of this curve tells us:
- **Threshold**: How much CasE is needed before green starts dropping?
- **Steepness**: Is the transition sharp (switch-like) or gradual (analog)?
- **Dynamic range**: What's the ratio between fully ON and fully OFF?

This information is critical for designing multi-layer circuits — if the curve is too gradual, signals degrade through cascade layers.

## Circuit Design

### All wells share the same base

| Plasmid | Amount | Role |
|---------|--------|------|
| CasE_rec_mNeonGreen | 200 ng | Encodes green; CasE inhibits |
| eBFP2 | 100 ng | Blue transfection control |

### CasE dose varies by column

| Column | CasE (ng) | Total DNA | What we expect |
|--------|-----------|-----------|---------------|
| 1 | 0 | 300 ng | Full green — no inhibitor present |
| 2 | 25 | 325 ng | Probably still bright — too little CasE to suppress |
| 3 | 50 | 350 ng | Might start dimming — approaching threshold |
| 4 | 75 | 375 ng | Partial suppression expected |
| 5 | 100 | 400 ng | Significant suppression — nearing full inhibition |
| 6 | 150 | 450 ng | Fully dark — enough CasE to destroy all mNeonGreen mRNA |

### DNA budget check

All wells are under 650 ng max. Column 6 (highest dose) uses 450 ng.

## Well-by-Well Assignment

| Well | CasE (ng) | CasE_rec_mNeonGreen (ng) | eBFP2 (ng) | Total (ng) |
|------|-----------|--------------------------|------------|------------|
| A1-D1 | 0 | 200 | 100 | 300 |
| A2-D2 | 25 | 200 | 100 | 325 |
| A3-D3 | 50 | 200 | 100 | 350 |
| A4-D4 | 75 | 200 | 100 | 375 |
| A5-D5 | 100 | 200 | 100 | 400 |
| A6-D6 | 150 | 200 | 100 | 450 |

4 rows x 6 columns = 24 wells, all filled.

## Tube Budget

| Resource | Count | Details |
|----------|-------|---------|
| Unique plasmid source tubes | 3 | CasE, CasE_rec_mNeonGreen, eBFP2 |
| DNA destination tubes | 24 | 1 per well |
| L3K/OM destination tubes | 24 | 1 per well |
| Reagent tubes (reserved) | 6 | D1-D6 on rack 3 |
| **Total tubes** | **57** | Out of 72 positions (66 available) |

## Expected Results

### Quantitative analysis

After imaging, measure mean green fluorescence intensity in each well. Normalize by blue intensity (to correct for transfection efficiency differences between wells). Plot:

```
Normalized green (green/blue ratio) vs. CasE dose (ng)
```

This gives you the **dose-response curve** for CasE inhibition of mNeonGreen.

### What the curve shape tells you

| Curve Shape | Interpretation | Circuit Implications |
|-------------|---------------|---------------------|
| Sharp sigmoid | Switch-like behavior; clear ON/OFF threshold | Good for digital-style logic gates |
| Gradual slope | Analog, graded response | Good for analog neuromorphic computation |
| Flat until high dose, then drops | CasE needs to accumulate past a threshold | Circuits need sufficient ERN expression |
| Linear decrease | Proportional inhibition | Predictable, easy to model |

### Troubleshooting

| Observation | Likely Cause |
|-------------|-------------|
| All wells equally bright | CasE not working; check plasmid |
| All wells equally dark | CasE_rec_mNeonGreen has very high sensitivity to CasE; even 25 ng is enough |
| High variability within same column | Transfection efficiency varies; normalize by blue |
| No blue anywhere | Transfection protocol failed |
| Green in column 6 but not column 1 | Plate loaded backwards (check orientation) |

## Variations

### Finer resolution around the threshold

If the first experiment shows a sharp transition between columns 3 and 5, repeat with finer dose steps in that range (e.g., 40, 50, 60, 70, 80, 90 ng).

### Compare ERNs

Run the same gradient with Csy4 + Csy4_rec_mNeonGreen, or PgU + PgU_rec_mNeonGreen, to compare the dose-response curves of different ERNs. Are some sharper switches than others?

### Vary the target instead

Keep CasE constant at 150 ng but vary CasE_rec_mNeonGreen from 50 to 300 ng. This measures whether excess target can "titrate out" the ERN — important for understanding circuit robustness.

### Two-ERN dose matrix

Use a 2D gradient: vary CasE across columns and Csy4 across rows, with `CasE_rec_Csy4_rec_mKO2` as the target. This maps the 2D dose-response surface of the AND gate.

## Connection to Neuromorphic Computing

In the neuromorphic framework, each ERN is a "neuron" and its inhibitory strength is the "synaptic weight." This experiment directly measures the weight transfer function — the relationship between how much signal (ERN) you put in and how much output (fluorescence) comes out.

Real neural networks work because neurons have nonlinear transfer functions (like sigmoids). If our ERN transfer function is also sigmoidal, it means the biological circuits can perform the same kinds of computations as artificial neural networks — but inside living cells.

## Files

- `experiment_config.csv` — Input CSV for the NeuromorphicWizard (minimal format)
- Run through the Wizard to auto-assign tube slots and generate the OT-2 protocol

## Related

- [Experiment 3: Checkerboard](experiment3-checkerboard.md) — Binary ON/OFF pattern (same parts, no gradient)
- [Biology Concepts](../background/biology-concepts.md) — How ERN inhibition works
- [ERN Recognition Sequences](../reference/endoribonuclease-recognition-sequences.md) — Molecular details of CasE
