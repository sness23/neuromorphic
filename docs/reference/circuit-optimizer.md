# Circuit Optimizer

A tool that searches for genetic circuits whose predicted heatmaps match a target 2D function. It generates random valid circuits, scores them against the target via the biocompiler prediction API, and keeps the best matches.

## Quick Start

```bash
# Find circuits that produce a center dot pattern (200 iterations)
python circuit-optimizer.py --target center_dot --iterations 200 --top 10

# Try to make a heart shape (1000 iterations, more concurrent requests)
python circuit-optimizer.py --target heart --iterations 1000 --top 20 --concurrency 8

# Reproducible run with a fixed seed
python circuit-optimizer.py --target ring --iterations 500 --seed 42
```

## How It Works

### 1. Define a Target Function

The target is a mathematical function f(x, y) → [0, 1] defined over the unit square. It represents the ideal heatmap you want the circuit to produce. The optimizer includes several built-in targets:

| Target | Description | Shape |
|--------|-------------|-------|
| `center_dot` | Gaussian peak at (0.5, 0.5) | Bright spot in the center |
| `ring` | Annular Gaussian at radius 0.3 | Donut/ring shape |
| `letter_z` | Three bars: top, diagonal, bottom | Z letterform |
| `letter_s` | Two semicircles with connecting bars | S letterform |
| `heart` | Implicit heart curve | Filled heart shape |
| `diagonal` | Gaussian along the anti-diagonal | Bright band from top-left to bottom-right |
| `corners` | Four Gaussians at corners | Bright in all four corners |

The target function is sampled onto a 32×32 grid to match the biocompiler API's resolution.

### 2. Generate Random Circuits

Each iteration generates a random valid circuit by:

1. **Picking a marker pair** for X1 and X2 (e.g., eBFP2 + mMaroon1)
2. **Picking ERNs** for X1 and X2 (CasE and Csy4 in random order)
3. **Choosing a topology** from a weighted random distribution:

| Topology | Description | Weight |
|----------|-------------|--------|
| `self_inhibit` | Output parts in same group as their inhibitor ERN | 20% |
| `cross_inhibit` | Output parts in opposite group from their inhibitor ERN | 20% |
| `cascade` | ERN→ERN wiring part + separate output part | 15% |
| `cascade_plus_output` | ERN→ERN wiring + output in an input group | 15% |
| `simple_output` | Just one output part in Bias | 10% |
| `dual_rec` | CasE_rec_Csy4_rec_mKO2 dual-recognition AND gate | 10% |
| `three_ern` | All three ERNs (CasE, Csy4, PgU) with wiring | 10% |

4. **Assigning random DNA amounts** — each part gets at least 50 ng (pipetting minimum), randomized with the total constrained to 650 ng

### 3. Validate Constraints

Generated circuits must satisfy all biocompiler constraints:

- Each ERN recognition prefix (`CasE_rec`, `Csy4_rec`, `PgU_rec`) appears on at most one target mRNA (no split sequestrons)
- No free marker proteins outside X1/X2 groups (API only supports 2D)
- No `PgU_rec` targeting fluorescent reporters (not supported by prediction model)
- X1 and X2 each contain exactly one marker protein
- Every part has at least 50 ng of DNA
- Total DNA per circuit does not exceed 650 ng
- At least one output part (ERN_rec_color) is present

Invalid circuits are discarded before making API calls. Roughly 50% of random circuits hit a constraint that only the biocompiler server can detect (such as split sequestrons in complex topologies), resulting in API errors that are silently skipped.

### 4. Call the Biocompiler API

Each valid circuit is converted to a biocompiler recipe and sent to the prediction API:

```
POST https://biocomp-api.rachael.jdisset.com/v1/predict/heatmap
Body: {"recipe": <recipe>, "resolution": 32}
Response: {"heatmap": {"z": [[32x32 matrix]]}, "meta": {...}}
```

Requests are made concurrently (default 5, configurable up to 8+) for throughput.

### 5. Score Against Target

The predicted heatmap is normalized to [0, 1] and compared to the target using mean squared error (MSE):

```
score = mean((normalized_heatmap - target)²)
```

Lower MSE means the circuit's predicted heatmap more closely matches the target function. A score of 0.0 would be a perfect match. In practice, scores around 0.10–0.15 indicate a reasonable approximation given the constraints of ERN inhibition circuits.

### 6. Keep the Best

The top N circuits (by MSE score) are retained across all iterations. Results are saved to disk.

## Command Line Options

```
python circuit-optimizer.py [OPTIONS]

Options:
  --target TARGET      Target function to match (default: center_dot)
  --iterations N       Number of random circuits to try (default: 100)
  --top N              Keep top N circuits (default: 5)
  --concurrency N      Concurrent API requests (default: 5)
  --seed N             Random seed for reproducibility
```

### Choosing Iteration Count

| Iterations | Time (~) | Successful Predictions (~) | Use Case |
|-----------|----------|--------------------------|----------|
| 50 | 1 min | ~25 | Quick test |
| 200 | 3 min | ~100 | Moderate search |
| 1000 | 15 min | ~500 | Thorough search |
| 5000 | 1 hour | ~2500 | Exhaustive search |

About 50% of generated circuits pass all constraints and return a valid prediction. The success rate depends on topology mix — simple topologies succeed more often than complex ones.

## Output Files

All results are saved to `experiments/experiment-optimizer/`:

### `top-{target}.csv`

Standard experiment CSV compatible with the NeuromorphicWizard. Upload it directly in the Build tab to visualize any of the top circuits in the Predict tab.

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
Opt0097,X1,CasE,50,100
Opt0097,X1,mKO2,50,150
Opt0097,X2,Csy4,50,75
Opt0097,X2,mMaroon1,50,200
Opt0097,X3,Csy4_rec_CasE,50,50
Opt0097,Bias,CasE_rec_mNeonGreen,50,75
```

### `results-{target}.json`

Detailed results including full recipes, scores, and part breakdowns:

```json
[
  {
    "rank": 1,
    "name": "Opt0097",
    "score_mse": 0.105047,
    "total_dna": 650,
    "parts": [
      {"group": "X1", "part": "CasE", "ng": 100},
      {"group": "X1", "part": "mKO2", "ng": 150},
      ...
    ],
    "recipe": { ... }
  }
]
```

### `heatmaps-{target}.npz`

Numpy archive containing the predicted heatmap matrix for each top circuit plus the target matrix. Load with:

```python
import numpy as np
data = np.load("experiments/experiment-optimizer/heatmaps-center_dot.npz")
target = data["target"]          # 32x32 target function
best = data["Opt0097"]           # 32x32 predicted heatmap
print(list(data.keys()))         # all available matrices
```

## Understanding the Results

### What the Optimizer Can Find

The optimizer searches over circuit topologies AND DNA ratios simultaneously. It can find non-obvious combinations, such as:

- Putting output parts in input groups (self-inhibiting or cross-inhibiting)
- Using three ERNs with cascaded wiring
- Asymmetric DNA ratios that shift the response curve
- Combining the dual-recognition AND gate with cascades

### What the Optimizer Cannot Do

The search is random, not gradient-based. It does not:

- Guarantee finding the global optimum
- Learn from previous iterations (each circuit is independent)
- Modify circuits incrementally (no mutation/crossover)

For better results, run more iterations. The random search is effective because the circuit space is relatively small (a few hundred valid topologies × continuous DNA ratios).

### Interpreting MSE Scores

| MSE Range | Interpretation |
|-----------|---------------|
| < 0.05 | Excellent match — heatmap closely resembles target |
| 0.05–0.10 | Good match — recognizable similarity |
| 0.10–0.15 | Moderate match — some features align |
| 0.15–0.20 | Weak match — general trend correct |
| > 0.20 | Poor match — topology produces a very different shape |

Some target functions (like `center_dot` or `ring`) are inherently harder to match because they require bandpass behavior in both dimensions, which is difficult with purely inhibitory ERN circuits. Targets like `corners` or `diagonal` may be easier to approximate.

### Why Some Targets Are Hard

ERN circuits are fundamentally **inhibitory** — enzymes cut mRNA to suppress protein production. This makes certain patterns easier or harder:

- **Easy**: Bright corner (low ERN = no inhibition = output ON), gradients, anti-diagonals
- **Medium**: Bright edges, XOR-like patterns (cross-inhibition creates asymmetry)
- **Hard**: Center dot (requires bandpass — output ON only at intermediate levels), ring, heart

Bandpass behavior requires the output to be OFF at both low AND high input levels. With only inhibition available:

- At low input: output should be OFF → needs a "default inhibitor" that keeps output suppressed
- At medium input: output should be ON → needs the input to relieve the default inhibition
- At high input: output should be OFF → needs the input to also suppress the output

Cascades and self-inhibiting topologies can approximate this by creating competing production and inhibition pathways with different dose-response curves. The biocompiler model captures these non-linear dynamics, which is why the optimizer sometimes finds circuits with surprisingly good bandpass-like behavior.

## Example Workflow

### 1. Run the optimizer

```bash
python circuit-optimizer.py --target center_dot --iterations 500 --top 10
```

### 2. Upload to NeuromorphicWizard

Open the Wizard, go to the Build tab, and upload `experiments/experiment-optimizer/top-center_dot.csv`.

### 3. Predict each circuit

Switch to the Predict tab. Select each circuit from the dropdown (Opt0097, Opt0110, etc.) and click Predict. Compare the heatmaps visually.

### 4. Pick the best and generate a protocol

Select the circuit you like best. Go to the Generate tab to produce an OT-2 protocol for wet lab execution.

### 5. Iterate

If none of the results are satisfying, run the optimizer again with more iterations or a different seed:

```bash
python circuit-optimizer.py --target center_dot --iterations 2000 --seed 123
```

## Adding Custom Target Functions

Edit the `TARGETS` dictionary in `circuit-optimizer.py`:

```python
def target_my_pattern(x, y):
    """My custom pattern. x and y range from 0 to 1. Return 0 to 1."""
    # Example: bright horizontal band in the middle
    return math.exp(-((y - 0.5)**2) / 0.02)

TARGETS["my_pattern"] = target_my_pattern
```

Then run:

```bash
python circuit-optimizer.py --target my_pattern --iterations 200
```

The function takes (x, y) coordinates in [0, 1] × [0, 1] and should return a value in [0, 1] where 1 is maximum brightness and 0 is dark.
