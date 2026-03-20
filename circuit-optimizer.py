#!/usr/bin/env python3
"""
Circuit Optimizer — find genetic circuits that match a target 2D function.

Generates random valid circuits, predicts their heatmaps via the biocompiler API,
and scores them against a target function. Keeps the best matches.

Usage:
    python circuit-optimizer.py --target center_dot --iterations 100
    python circuit-optimizer.py --target letter_z --iterations 200 --top 10
    python circuit-optimizer.py --target custom --iterations 50
"""

import argparse
import asyncio
import csv
import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
import numpy as np

# ── API Configuration ──────────────────────────────────────────────────────────

BIOCOMPILER_API_BASE = "https://biocomp-api.rachael.jdisset.com"
PREDICT_ENDPOINT = f"{BIOCOMPILER_API_BASE}/v1/predict/heatmap"
RESOLUTION = 32
API_TIMEOUT = 60.0

# ── Parts Library ──────────────────────────────────────────────────────────────

ERNS = ["CasE", "Csy4", "PgU"]

# ERN→ERN wiring: (part_name, rec_prefix, target_protein)
ERN_REC_ERN = [
    ("PgU_rec_Csy4", "PgU_rec", "Csy4"),
    ("PgU_rec_CasE", "PgU_rec", "CasE"),
    ("Csy4_rec_CasE", "Csy4_rec", "CasE"),
    ("CasE_rec_Csy4", "CasE_rec", "Csy4"),
]

# ERN→Color outputs: (part_name, rec_prefixes, target_protein)
ERN_REC_COLOR = [
    ("Csy4_rec_mNeonGreen", ["Csy4_rec"], "mNeonGreen"),
    ("CasE_rec_mNeonGreen", ["CasE_rec"], "mNeonGreen"),
    # PgU_rec_mNeonGreen excluded — not supported by prediction model
    ("CasE_rec_Csy4_rec_mKO2", ["CasE_rec", "Csy4_rec"], "mKO2"),
]

# Available markers for X1/X2 groups
MARKERS = ["mKO2", "eBFP2", "mMaroon1", "mNeonGreen"]

# Marker pairs (X1_marker, X2_marker) — must be different
MARKER_PAIRS = [
    ("eBFP2", "mMaroon1"),
    ("eBFP2", "mNeonGreen"),
    ("eBFP2", "mKO2"),
    ("mKO2", "mMaroon1"),
    ("mKO2", "mNeonGreen"),
    ("mMaroon1", "mNeonGreen"),
]

MIN_DNA_PER_PART = 50  # ng, minimum to avoid pipetting issues
MAX_TOTAL_DNA = 650    # ng per circuit


# ── Target Functions ───────────────────────────────────────────────────────────

def target_center_dot(x, y):
    """Gaussian peak in the center."""
    cx, cy = 0.5, 0.5
    sigma = 0.18
    return math.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))


def target_ring(x, y):
    """Ring/donut shape."""
    cx, cy = 0.5, 0.5
    r = math.sqrt((x - cx)**2 + (y - cy)**2)
    r_target = 0.3
    sigma = 0.08
    return math.exp(-((r - r_target)**2) / (2 * sigma**2))


def target_letter_z(x, y):
    """Z shape: top bar, diagonal, bottom bar."""
    score = 0.0
    bar_width = 0.12
    # Top bar (y ≈ 0.85)
    if abs(y - 0.85) < bar_width:
        score = max(score, 1.0 - abs(y - 0.85) / bar_width)
    # Bottom bar (y ≈ 0.15)
    if abs(y - 0.15) < bar_width:
        score = max(score, 1.0 - abs(y - 0.15) / bar_width)
    # Diagonal from top-right to bottom-left
    diag = 1.0 - x  # y = 1 - x
    if abs(y - diag) < bar_width:
        score = max(score, 1.0 - abs(y - diag) / bar_width)
    return score


def target_letter_s(x, y):
    """S shape using two semicircles."""
    score = 0.0
    tube_width = 0.12
    # Top bar
    if abs(y - 0.85) < tube_width and x > 0.3:
        score = max(score, 1.0)
    # Bottom bar
    if abs(y - 0.15) < tube_width and x < 0.7:
        score = max(score, 1.0)
    # Upper right curve (semicircle centered at x=0.65, y=0.65, r=0.2)
    r1 = math.sqrt((x - 0.65)**2 + (y - 0.65)**2)
    if abs(r1 - 0.2) < tube_width and x > 0.5:
        score = max(score, 1.0)
    # Middle connector
    if abs(x - 0.5) < tube_width and 0.4 < y < 0.6:
        score = max(score, 1.0)
    # Lower left curve (semicircle centered at x=0.35, y=0.35, r=0.2)
    r2 = math.sqrt((x - 0.35)**2 + (y - 0.35)**2)
    if abs(r2 - 0.2) < tube_width and x < 0.5:
        score = max(score, 1.0)
    return score


def target_heart(x, y):
    """Heart shape."""
    # Transform to centered coordinates
    tx = (x - 0.5) * 2.5
    ty = (y - 0.4) * 2.5
    # Heart implicit equation: (x^2 + y^2 - 1)^3 - x^2 * y^3 < 0
    val = (tx**2 + ty**2 - 1)**3 - tx**2 * ty**3
    if val < 0:
        return 1.0
    # Soft falloff outside
    return max(0.0, math.exp(-val * 2))


def target_diagonal(x, y):
    """Bright anti-diagonal band."""
    dist = abs(x + y - 1.0) / math.sqrt(2)
    sigma = 0.12
    return math.exp(-(dist**2) / (2 * sigma**2))


def target_corners(x, y):
    """Bright in all four corners."""
    return max(
        math.exp(-((x**2 + y**2)) / 0.08),
        math.exp(-(((x-1)**2 + y**2)) / 0.08),
        math.exp(-((x**2 + (y-1)**2)) / 0.08),
        math.exp(-(((x-1)**2 + (y-1)**2)) / 0.08),
    )


TARGETS = {
    "center_dot": target_center_dot,
    "ring": target_ring,
    "letter_z": target_letter_z,
    "letter_s": target_letter_s,
    "heart": target_heart,
    "diagonal": target_diagonal,
    "corners": target_corners,
}


def make_target_matrix(func, resolution=RESOLUTION):
    """Generate a target matrix from a function."""
    matrix = np.zeros((resolution, resolution))
    for iy in range(resolution):
        for ix in range(resolution):
            x = ix / (resolution - 1)
            y = iy / (resolution - 1)
            matrix[iy, ix] = func(x, y)
    return matrix


# ── Circuit Generation ─────────────────────────────────────────────────────────

@dataclass
class CircuitPart:
    group: str
    part_name: str
    dna_ng: int


@dataclass
class Circuit:
    name: str
    parts: list = field(default_factory=list)
    score: float = float('inf')
    heatmap: Optional[np.ndarray] = None

    def total_dna(self):
        return sum(p.dna_ng for p in self.parts)

    def to_csv_rows(self):
        rows = []
        for p in self.parts:
            rows.append({
                "Circuit name": self.name,
                "Transfection group": p.group,
                "Contents": p.part_name,
                "Concentration (ng/uL)": 50,
                "DNA wanted (ng)": p.dna_ng,
            })
        return rows

    def to_recipe(self):
        """Convert to biocompiler API recipe format."""
        # Group parts by transfection group
        groups = {}
        for p in self.parts:
            groups.setdefault(p.group, []).append(p)

        # Find markers in X1 and X2
        input_order = []
        for g in ["X1", "X2"]:
            for p in groups.get(g, []):
                if p.part_name in MARKERS:
                    input_order.append(p.part_name)
                    break

        # Sort group names
        def sort_key(name):
            if name == "Bias":
                return (999, name)
            if name.startswith("X"):
                try:
                    return (int(name[1:]), name)
                except ValueError:
                    pass
            return (1000, name)

        sorted_groups = sorted(groups.keys(), key=sort_key)

        content = []
        for group_name in sorted_groups:
            group_parts = groups[group_name]
            group_total = sum(p.dna_ng for p in group_parts)

            units = []
            ratios = []
            for p in group_parts:
                unit_type = _get_unit_type(p.part_name)
                unit_name = f"{group_name.lower()}_{unit_type}"

                if unit_type == "output":
                    parsed = _parse_output_name(p.part_name)
                    if len(parsed) > 2:
                        # Dual-rec: split into separate units
                        receptors = parsed[:-1]
                        fluorescent = parsed[-1]
                        ratio = p.dna_ng / group_total if group_total > 0 else 0
                        for ri, rec in enumerate(receptors):
                            units.append({
                                "name": f"{unit_name}_{ri+1}",
                                "slots": ["hEF1a", rec, fluorescent, "L0.T_4560"],
                            })
                            ratios.append(ratio / len(receptors))
                        continue
                    slots = ["hEF1a"] + parsed + ["L0.T_4560"]
                else:
                    slots = ["hEF1a", p.part_name, "L0.T_4560"]

                unit = {"name": unit_name, "slots": slots}
                if unit_type == "marker":
                    unit["no_masking"] = True
                units.append(unit)
                ratios.append(p.dna_ng / group_total if group_total > 0 else 0)

            content.append({
                "name": group_name.lower(),
                "units": units,
                "ratios": ratios,
            })

        return {
            "name": self.name,
            "input_order": input_order,
            "content": content,
        }


def _get_unit_type(name):
    if "rec_" in name:
        return "output"
    if name in {"CasE", "Csy4", "PgU"}:
        return "ern"
    return "marker"


def _parse_output_name(name):
    parts = []
    remaining = name
    while True:
        idx = remaining.find("_rec_")
        if idx == -1:
            break
        parts.append(remaining[:idx + 4])
        remaining = remaining[idx + 5:]
    if parts:
        parts.append(remaining)
        return parts
    return [name]


def generate_random_circuit(circuit_id: int) -> Optional[Circuit]:
    """Generate a random valid circuit."""
    name = f"Opt{circuit_id:04d}"

    # Pick marker pair
    x1_marker, x2_marker = random.choice(MARKER_PAIRS)

    # Pick ERNs for X1 and X2
    x1_ern, x2_ern = random.sample(["CasE", "Csy4"], 2)

    # Track which rec prefixes are used
    used_prefixes = set()

    parts = []

    # X1: ERN + marker (always)
    parts.append(CircuitPart("X1", x1_ern, 0))
    parts.append(CircuitPart("X1", x1_marker, 0))

    # X2: ERN + marker (always)
    parts.append(CircuitPart("X2", x2_ern, 0))
    parts.append(CircuitPart("X2", x2_marker, 0))

    # Decide on circuit topology (weighted random choice)
    topology = random.choices(
        ["simple_output", "cascade", "self_inhibit", "cross_inhibit",
         "dual_rec", "cascade_plus_output", "three_ern"],
        weights=[10, 15, 20, 20, 10, 15, 10],
        k=1
    )[0]

    available_outputs = list(ERN_REC_COLOR)
    available_wiring = list(ERN_REC_ERN)

    if topology == "simple_output":
        # Just add one output part to Bias
        random.shuffle(available_outputs)
        for part_name, prefixes, target in available_outputs:
            if all(p not in used_prefixes for p in prefixes):
                parts.append(CircuitPart("Bias", part_name, 0))
                used_prefixes.update(prefixes)
                break

    elif topology == "dual_rec":
        # Use the dual-rec AND gate part
        parts.append(CircuitPart("Bias", "CasE_rec_Csy4_rec_mKO2", 0))
        used_prefixes.update(["CasE_rec", "Csy4_rec"])

    elif topology == "cascade":
        # Add one ERN→ERN wiring + one output
        random.shuffle(available_wiring)
        for part_name, prefix, target in available_wiring:
            if prefix not in used_prefixes:
                group = random.choice(["X3", "Bias"])
                parts.append(CircuitPart(group, part_name, 0))
                used_prefixes.add(prefix)
                break
        random.shuffle(available_outputs)
        for part_name, prefixes, target in available_outputs:
            if all(p not in used_prefixes for p in prefixes):
                parts.append(CircuitPart("Bias", part_name, 0))
                used_prefixes.update(prefixes)
                break

    elif topology == "self_inhibit":
        # Put output parts IN the input groups (self-inhibiting)
        # X1 gets an output inhibited by x1_ern, X2 gets one inhibited by x2_ern
        x1_prefix = f"{x1_ern}_rec"
        x2_prefix = f"{x2_ern}_rec"
        for part_name, prefixes, target in available_outputs:
            if len(prefixes) == 1 and prefixes[0] == x1_prefix and x1_prefix not in used_prefixes:
                parts.append(CircuitPart("X1", part_name, 0))
                used_prefixes.add(x1_prefix)
                break
        for part_name, prefixes, target in available_outputs:
            if len(prefixes) == 1 and prefixes[0] == x2_prefix and x2_prefix not in used_prefixes:
                parts.append(CircuitPart("X2", part_name, 0))
                used_prefixes.add(x2_prefix)
                break

    elif topology == "cross_inhibit":
        # Put output parts in OPPOSITE input groups
        x1_prefix = f"{x1_ern}_rec"
        x2_prefix = f"{x2_ern}_rec"
        # X1 gets an output inhibited by x2_ern
        for part_name, prefixes, target in available_outputs:
            if len(prefixes) == 1 and prefixes[0] == x2_prefix and x2_prefix not in used_prefixes:
                parts.append(CircuitPart("X1", part_name, 0))
                used_prefixes.add(x2_prefix)
                break
        # X2 gets an output inhibited by x1_ern
        for part_name, prefixes, target in available_outputs:
            if len(prefixes) == 1 and prefixes[0] == x1_prefix and x1_prefix not in used_prefixes:
                parts.append(CircuitPart("X2", part_name, 0))
                used_prefixes.add(x1_prefix)
                break

    elif topology == "cascade_plus_output":
        # ERN→ERN wiring + output in an input group
        random.shuffle(available_wiring)
        for part_name, prefix, target in available_wiring:
            if prefix not in used_prefixes:
                group = random.choice(["X1", "X2", "X3", "Bias"])
                parts.append(CircuitPart(group, part_name, 0))
                used_prefixes.add(prefix)
                break
        random.shuffle(available_outputs)
        for part_name, prefixes, target in available_outputs:
            if all(p not in used_prefixes for p in prefixes):
                group = random.choice(["X1", "X2", "Bias"])
                parts.append(CircuitPart(group, part_name, 0))
                used_prefixes.update(prefixes)
                break

    elif topology == "three_ern":
        # Add PgU as a third ERN in X3 or Bias, plus wiring
        third_ern = [e for e in ERNS if e not in (x1_ern, x2_ern)][0]
        parts.append(CircuitPart("X3", third_ern, 0))
        # Add one wiring part
        random.shuffle(available_wiring)
        for part_name, prefix, target in available_wiring:
            if prefix not in used_prefixes:
                group = random.choice(["X3", "Bias"])
                parts.append(CircuitPart(group, part_name, 0))
                used_prefixes.add(prefix)
                break
        # Add one output
        random.shuffle(available_outputs)
        for part_name, prefixes, target in available_outputs:
            if all(p not in used_prefixes for p in prefixes):
                parts.append(CircuitPart("Bias", part_name, 0))
                used_prefixes.update(prefixes)
                break

    # Check we have at least one output/wiring part
    has_output = any(_get_unit_type(p.part_name) == "output" for p in parts)
    if not has_output:
        return None

    # Assign random DNA amounts (minimum 50ng each, total <= 650ng)
    n_parts = len(parts)
    if n_parts * MIN_DNA_PER_PART > MAX_TOTAL_DNA:
        return None

    remaining = MAX_TOTAL_DNA - n_parts * MIN_DNA_PER_PART
    # Random allocation of the remaining DNA
    weights = [random.random() for _ in range(n_parts)]
    total_weight = sum(weights)
    for i, p in enumerate(parts):
        extra = int(remaining * weights[i] / total_weight) if total_weight > 0 else 0
        # Round to nearest 25ng for cleaner values
        extra = (extra // 25) * 25
        p.dna_ng = MIN_DNA_PER_PART + extra

    # Adjust total to hit exactly 650 (distribute remainder)
    diff = MAX_TOTAL_DNA - sum(p.dna_ng for p in parts)
    if diff > 0:
        # Add remainder to a random part (in increments of 25)
        idx = random.randint(0, n_parts - 1)
        parts[idx].dna_ng += diff

    circuit = Circuit(name=name, parts=parts)
    if circuit.total_dna() > MAX_TOTAL_DNA:
        return None

    return circuit


# ── API Call ───────────────────────────────────────────────────────────────────

async def predict_circuit(client: httpx.AsyncClient, circuit: Circuit) -> Optional[np.ndarray]:
    """Call biocompiler API and return heatmap matrix."""
    recipe = circuit.to_recipe()
    try:
        response = await client.post(
            PREDICT_ENDPOINT,
            json={"recipe": recipe, "resolution": RESOLUTION},
        )
        response.raise_for_status()
        data = response.json()
        return np.array(data["heatmap"]["z"])
    except (httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException, KeyError) as e:
        return None


# ── Scoring ────────────────────────────────────────────────────────────────────

def score_circuit(heatmap: np.ndarray, target: np.ndarray) -> float:
    """Score a heatmap against target. Lower is better (MSE)."""
    # Normalize heatmap to [0, 1]
    hmin, hmax = heatmap.min(), heatmap.max()
    if hmax - hmin < 1e-10:
        normalized = np.zeros_like(heatmap)
    else:
        normalized = (heatmap - hmin) / (hmax - hmin)
    return float(np.mean((normalized - target) ** 2))


# ── Main Loop ──────────────────────────────────────────────────────────────────

async def run_optimizer(target_name: str, iterations: int, top_k: int, concurrency: int):
    """Run the optimization loop."""
    if target_name not in TARGETS:
        print(f"Unknown target '{target_name}'. Available: {', '.join(TARGETS.keys())}")
        sys.exit(1)

    target_func = TARGETS[target_name]
    target_matrix = make_target_matrix(target_func)

    print(f"Target: {target_name}")
    print(f"Iterations: {iterations}")
    print(f"Concurrency: {concurrency}")
    print(f"Keeping top {top_k} circuits")
    print()

    best_circuits = []
    total_attempted = 0
    total_api_calls = 0
    total_api_errors = 0
    start_time = time.time()

    async with httpx.AsyncClient(timeout=API_TIMEOUT) as client:
        for batch_start in range(0, iterations, concurrency):
            batch_size = min(concurrency, iterations - batch_start)

            # Generate batch of valid circuits
            circuits = []
            attempts = 0
            while len(circuits) < batch_size and attempts < batch_size * 10:
                c = generate_random_circuit(total_attempted + attempts)
                attempts += 1
                if c is not None:
                    circuits.append(c)
            total_attempted += attempts

            if not circuits:
                continue

            # Call API concurrently
            tasks = [predict_circuit(client, c) for c in circuits]
            results = await asyncio.gather(*tasks)

            for circuit, heatmap in zip(circuits, results):
                total_api_calls += 1
                if heatmap is None:
                    total_api_errors += 1
                    continue

                circuit.score = score_circuit(heatmap, target_matrix)
                circuit.heatmap = heatmap

                # Insert into top-k list
                best_circuits.append(circuit)
                best_circuits.sort(key=lambda c: c.score)
                best_circuits = best_circuits[:top_k]

            # Progress update
            elapsed = time.time() - start_time
            successful = total_api_calls - total_api_errors
            best_score = best_circuits[0].score if best_circuits else float('inf')
            rate = successful / elapsed if elapsed > 0 else 0

            print(
                f"  [{batch_start + batch_size:4d}/{iterations}] "
                f"API: {successful} ok, {total_api_errors} err | "
                f"Best MSE: {best_score:.6f} | "
                f"Rate: {rate:.1f}/s | "
                f"Elapsed: {elapsed:.0f}s"
            )

    print()
    print(f"{'='*60}")
    print(f"DONE — {total_api_calls - total_api_errors} successful predictions")
    print(f"{'='*60}")
    print()

    if not best_circuits:
        print("No successful circuits found.")
        return

    # Output results
    output_dir = Path("experiments/experiment-optimizer")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save top circuits as CSV
    csv_path = output_dir / f"top-{target_name}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Circuit name", "Transfection group", "Contents",
            "Concentration (ng/uL)", "DNA wanted (ng)",
        ])
        writer.writeheader()
        for circuit in best_circuits:
            for row in circuit.to_csv_rows():
                writer.writerow(row)

    # Save detailed results
    results_path = output_dir / f"results-{target_name}.json"
    results_data = []
    for i, circuit in enumerate(best_circuits):
        parts_desc = []
        for p in circuit.parts:
            parts_desc.append({"group": p.group, "part": p.part_name, "ng": p.dna_ng})
        results_data.append({
            "rank": i + 1,
            "name": circuit.name,
            "score_mse": circuit.score,
            "total_dna": circuit.total_dna(),
            "parts": parts_desc,
            "recipe": circuit.to_recipe(),
        })

    with open(results_path, "w") as f:
        json.dump(results_data, f, indent=2)

    # Save heatmaps as numpy arrays
    heatmaps_path = output_dir / f"heatmaps-{target_name}.npz"
    heatmap_dict = {}
    for circuit in best_circuits:
        if circuit.heatmap is not None:
            heatmap_dict[circuit.name] = circuit.heatmap
    heatmap_dict["target"] = target_matrix
    np.savez(heatmaps_path, **heatmap_dict)

    print(f"Results saved to {output_dir}/")
    print(f"  CSV:      {csv_path}")
    print(f"  Details:  {results_path}")
    print(f"  Heatmaps: {heatmaps_path}")
    print()

    # Print top results
    print(f"Top {len(best_circuits)} circuits for target '{target_name}':")
    print(f"{'Rank':<6} {'Name':<12} {'MSE':<12} {'DNA':<8} {'Parts'}")
    print("-" * 70)
    for i, circuit in enumerate(best_circuits):
        parts_summary = ", ".join(
            f"{p.part_name}({p.group},{p.dna_ng})"
            for p in circuit.parts
            if _get_unit_type(p.part_name) in ("output", "ern")
        )
        print(f"{i+1:<6} {circuit.name:<12} {circuit.score:<12.6f} {circuit.total_dna():<8} {parts_summary}")


def main():
    parser = argparse.ArgumentParser(description="Optimize genetic circuits to match target 2D functions")
    parser.add_argument("--target", default="center_dot", choices=list(TARGETS.keys()),
                        help="Target function to match")
    parser.add_argument("--iterations", type=int, default=100,
                        help="Number of random circuits to try")
    parser.add_argument("--top", type=int, default=5,
                        help="Keep top N circuits")
    parser.add_argument("--concurrency", type=int, default=5,
                        help="Concurrent API requests")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducibility")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    asyncio.run(run_optimizer(args.target, args.iterations, args.top, args.concurrency))


if __name__ == "__main__":
    main()
