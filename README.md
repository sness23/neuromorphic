# Neuromorphic Genetic Circuits

**HTGAA 2026 - Week 7: Genetic Circuits II - Intracellular Artificial Neural Networks**

Build neural networks inside living human cells using endoribonuclease enzymes, fluorescent reporters, and an OT-2 liquid handling robot.

---

## What Is This?

This project designs and tests **intracellular artificial neural networks (IANNs)** — circuits built from plasmid DNA that perform analog computation inside HEK293 cells. The building blocks are:

- **ERN enzymes** (CasE, Csy4, PgU) that destroy specific mRNA, suppressing protein production
- **Wiring parts** that connect ERNs to each other via engineered recognition sequences
- **Fluorescent reporters** (green, orange, blue, maroon) that make the circuit output visible under a microscope

The key idea: `X_rec_Y` means "X inhibits Y." Chain enough of these together and you get a neural network performing computation inside a living cell.

---

## Quick Start

**1. Understand the biology**

Start with [The Big Picture](docs/background/the-big-picture.md) — it explains everything from scratch, no prior knowledge needed.

**2. Pick a circuit**

Read the [Group Decision Guide](docs/experiments/group-decision-guide.md) for a concise comparison of circuit options.

**3. Run the NeuromorphicWizard**

```bash
cd NeuromorphicWizard
conda create -n neuro_wiz python==3.10
conda activate neuro_wiz
pip install -r requirements.txt
python3 main.py
```

Opens at http://localhost:8080. Upload your CSV, simulate, and download the OT-2 protocol.

---

## Repository Layout

```
neuromorphic/
│
├── README.md                       ← you are here
│
├── docs/
│   ├── background/                 ← read these first
│   │   ├── the-big-picture.md          start here — full explanation from scratch
│   │   ├── overview.md                 course context, schedule, constraints
│   │   └── biology-concepts.md         ERNs, HEK293 cells, Lipofectamine
│   │
│   ├── experiments/                ← circuit designs and results
│   │   ├── group-decision-guide.md     compare options (share with your group)
│   │   ├── design-options.md           all four circuit options in detail
│   │   ├── default-circuit.md          analysis of the starter circuit
│   │   ├── experiment1-three-layer-cascade.md    Circuit 1: full writeup
│   │   ├── experiment2-and-gate.md               Circuit 2: full writeup
│   │   └── submission-summary.md       what we submitted
│   │
│   └── reference/                  ← look things up here
│       ├── available-parts.md          parts by category
│       ├── complete-parts-reference.md every part, inhibition map, all topologies
│       ├── design-template.md          how to fill out the CSV
│       ├── neuromorphic-wizard.md      tool docs and architecture
│       ├── ot2-protocol.md             OT-2 protocol and volume calculations
│       ├── physical-protocol-walkthrough.md  deck to microscope, step by step
│       └── glossary.md                 every term defined
│
├── experiments/
│   ├── inputs/                     ← CSV files for the NeuromorphicWizard
│   │   ├── three-layer-cascade.csv     Circuit 1 input
│   │   ├── and-gate.csv                Circuit 2 input
│   │   ├── HTGAA-design-template.csv   blank template from course
│   │   └── HTGAA-part-names.csv        available plasmid parts
│   │
│   ├── experiment0/                ← default circuit (2-layer, green ON)
│   ├── experiment1/                ← three-layer cascade (green OFF)
│   ├── experiment2/                ← AND gate (orange OFF)
│   │   Each contains:
│   │     experiment_config.csv
│   │     opentrons_protocol.py
│   │     plate_layouts.xlsx
│   │     biocompiler_format.json5
│   │
│   └── zips/                       ← ready-to-submit zip files
│       ├── neuromorphic_experiment0.zip
│       ├── neuromorphic_experiment1.zip
│       └── neuromorphic_experiment2.zip
│
├── NeuromorphicWizard/             ← the design tool (NiceGUI web app)
│   ├── main.py                         entry point → http://localhost:8080
│   ├── core/                           config, state, validation, layout
│   ├── ui/                             tabs (Build, Predict, Generate, Analyze)
│   ├── data/                           OT-2 protocol templates
│   ├── tests/                          unit, integration, regression tests
│   └── requirements.txt
│
└── orig/                           ← original course materials
    ├── doc.txt                         lab protocol text
    └── url.txt                         link to HTGAA lab page
```

---

## Our Circuits

### Circuit 1: Three-Layer Cascade

Uses all 3 available ERNs in a chain. Adding a third inhibition layer flips the output compared to the default 2-layer circuit.

```
PgU ──▶ Csy4 ──▶ CasE ──▶ mNeonGreen (green)
 ON      OFF      ON       OFF
```

**Expected:** Blue ON, Maroon ON, Green **OFF**

Input: [`experiments/inputs/three-layer-cascade.csv`](experiments/inputs/three-layer-cascade.csv)
Full writeup: [`docs/experiments/experiment1-three-layer-cascade.md`](docs/experiments/experiment1-three-layer-cascade.md)

### Circuit 2: AND Gate

Two ERNs converge on a single output. The dual-recognition part `CasE_rec_Csy4_rec_mKO2` requires both enzymes to be absent for orange to turn on.

```
CasE ──┐
       ├──▶ mKO2 (orange)
Csy4 ──┘
 ON       ON       OFF
```

**Expected:** Blue ON, Green ON, Orange **OFF**

Input: [`experiments/inputs/and-gate.csv`](experiments/inputs/and-gate.csv)
Full writeup: [`docs/experiments/experiment2-and-gate.md`](docs/experiments/experiment2-and-gate.md)

---

## Reading Order

| Step | Document | What you'll learn |
|------|----------|------------------|
| 1 | [The Big Picture](docs/background/the-big-picture.md) | What cells, plasmids, ERNs, and fluorescent proteins are. How inhibition chains work. Why this is "neuromorphic." |
| 2 | [Biology Concepts](docs/background/biology-concepts.md) | Deeper detail on ERNs, HEK293 cells, Lipofectamine mechanism, transfection parameters. |
| 3 | [Available Parts](docs/reference/available-parts.md) | The full plasmid library — what each part does and how to use it. |
| 4 | [Group Decision Guide](docs/experiments/group-decision-guide.md) | Side-by-side comparison of circuit options. Share this with your group. |
| 5 | [Experiment 1](docs/experiments/experiment1-three-layer-cascade.md) / [Experiment 2](docs/experiments/experiment2-and-gate.md) | Detailed writeup of each circuit — logic, CSV, volumes, deck layout, expected results. |
| 6 | [Physical Protocol Walkthrough](docs/reference/physical-protocol-walkthrough.md) | What physically happens from OT-2 deck setup through fluorescence readout. |
| 7 | [Glossary](docs/reference/glossary.md) | Look up any term you don't recognize. |

---

## Available Plasmid Parts

| Category | Parts | Purpose |
|----------|-------|---------|
| **ERNs** | CasE, Csy4, PgU | Enzymes that cut specific mRNA |
| **ERN→ERN wiring** | PgU_rec_Csy4, PgU_rec_CasE, Csy4_rec_CasE, CasE_rec_Csy4 | Inhibitory connections between enzymes |
| **ERN→Color wiring** | Csy4_rec_mNeonGreen, CasE_rec_mNeonGreen, PgU_rec_mNeonGreen, CasE_rec_Csy4_rec_mKO2 | Regulated fluorescent outputs |
| **Colors** | mKO2 (orange), eBFP2 (blue), mMaroon1 (maroon), mNeonGreen (green) | Unregulated reporters / controls |

Full reference with inhibition map: [Complete Parts Reference](docs/reference/complete-parts-reference.md)

---

## Design Rules

- Total DNA per circuit: **<= 650 ng**
- All concentrations: **50 ng/uL**
- Use part names exactly as listed in [`HTGAA-part-names.csv`](experiments/inputs/HTGAA-part-names.csv)
- Template format: [`HTGAA-design-template.csv`](experiments/inputs/HTGAA-design-template.csv)

---

## Links

- Lab page: https://2026a.htgaa.org/2026a/course-pages/weeks/week-07/lab/index.html
- NeuromorphicWizard: [`NeuromorphicWizard/`](NeuromorphicWizard/)
