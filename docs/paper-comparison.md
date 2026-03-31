# From Perceptgenes to ERN Networks: Evolution of Neuromorphic Computing in Living Cells

## Overview

This document compares two approaches to building artificial neural networks inside living cells:

1. **Rizik et al. (2022)** — "Synthetic neuromorphic computing in living cells," Nature Communications. From Ron Weiss's lab at MIT (with Ramez Daniel at Technion). Implements perceptgene circuits in *E. coli*.

2. **HTGAA 2026 Week 7** — Intracellular artificial neural networks (IANNs) using endoribonuclease (ERN) enzymes in human HEK293 cells.

Both share the core vision: build neural network-like computation inside living cells. But they differ fundamentally in organism, mechanism, and design philosophy.

---

## Side-by-Side Comparison

| Dimension | Rizik et al. 2022 (Perceptgenes) | HTGAA 2026 (ERN Networks) |
|---|---|---|
| **Organism** | *E. coli* (bacteria) | HEK293 (human cells) |
| **Computing mechanism** | Transcription factors binding promoters | Endoribonucleases (CasE, Csy4, PgU) cleaving mRNA |
| **Regulation level** | Transcriptional (promoter activity) | Post-transcriptional (mRNA destruction) |
| **Signal domain** | Logarithmic — power-law and multiplication | Analog inhibition — concentration-dependent |
| **Wiring method** | Combinatorial promoters + auto-feedback loops | Engineered recognition sequences on mRNA (`X_rec_Y`) |
| **Inputs** | Small molecule inducers (IPTG, aTc, AHL, Arabinose) | DNA quantities (ng of each plasmid) |
| **Weight control** | Chemical concentrations, promoter mutations, degradation tags, protein sequestration | Plasmid stoichiometry (ratio of DNA amounts) |
| **Readout** | GFP, mCherry | 4 fluorescent proteins (mNeonGreen, mKO2, eBFP2, mMaroon1) |
| **Demonstrated complexity** | Multi-layer: 3-input majority, 2-bit ADC, ternary switch, backpropagation | 2-3 layer cascades, AND gates, inhibition chains |
| **Optimization method** | Wet-lab gradient descent / backpropagation | In silico simulation (NeuromorphicWizard) |
| **Parts for majority function** | ~15 biological parts | Not yet attempted |
| **Design time** | Weeks-months of promoter engineering | Hours with CSV-based design tool |

---

## The 2022 Paper: Perceptgenes in E. coli

### Key Innovation
The **perceptgene** is a perceptron redesigned for the logarithmic domain. In standard neural networks, a perceptron computes a weighted sum of inputs and passes it through an activation function. The perceptgene transforms this: scalar multiplication becomes exponentiation (power-law), and summation becomes multiplication. This matches how biology naturally works — gene expression responds to fold-changes, not absolute concentration differences.

### How It Works
- **Power-law functions** are implemented via auto-negative feedback loops (e.g., LacI repressing its own promoter PlacO, induced by IPTG). The feedback linearizes the log-domain response and broadens dynamic range.
- **Multiplication** is achieved with combinatorial promoters that have binding sites for multiple transcription factors (e.g., PlacO/tetO regulated by both LacI and TetR).
- **Activation functions** use the PBAD/AraC system. By tuning Arabinose concentration, the activation can be switched between negative rectifier (minimum), positive rectifier (maximum), and linear (average).
- **Weights** are modified by: changing promoter sequences (number of binding sites), tuning inducer concentrations, adding degradation tags, or using protein sequestration.

### Demonstrated Circuits
1. **Single perceptgene computations:** minimum, maximum, and average of two analog inputs
2. **Soft majority function:** 3-input, 2-layer network — output is "1" when 2+ of 3 inputs are high
3. **2-bit analog-to-digital converter:** converts continuous AHL concentration into 2 digital bits (MSB + LSB)
4. **Ternary switch:** 3-level output from a single analog input
5. **Programmable logic:** OR-to-AND switching via small molecule induction (ExsA/ExsD sequestration)
6. **Backpropagation:** experimental gradient descent optimization across a 2D weight space (6 Arabinose levels x 4 Plux mutants = 24 weight combinations, 576 total measurements)

### Strengths
- Mathematically rigorous — full theoretical framework with log-domain perceptron algebra
- Demonstrated multi-layer networks with real optimization algorithms
- Efficient resource usage (e.g., 2-bit ADC needs only 2 transcription factors vs. ~10 parts digitally)

### Limitations
- Deeply entangled with *E. coli* transcriptional machinery
- Weight tuning requires promoter mutations or new genetic constructs
- Each new circuit requires extensive characterization (576 samples for majority optimization)
- Limited to bacterial applications

---

## The HTGAA 2026 Approach: ERN Networks in Human Cells

### Key Innovation
Uses **endoribonucleases** (ERNs) — enzymes that cut specific RNA sequences — as the computational primitive. Instead of controlling whether a gene is transcribed (promoter-level), ERNs control whether mRNA survives long enough to be translated into protein. This is a fundamentally different and simpler abstraction.

### How It Works
- **ERN enzymes** (CasE, Csy4, PgU) each recognize and cut a specific RNA sequence
- **Wiring parts** like `Csy4_rec_CasE` encode CasE protein but include a Csy4 recognition sequence on the mRNA — so if Csy4 is present, it destroys CasE's mRNA before it can be translated
- **Inhibition chains** create logic: odd number of inhibitions = output OFF, even = output ON
- **Weights** are set by DNA amounts — how many nanograms of each plasmid you transfect into cells
- **Readout** uses 4 fluorescent reporters visible under microscopy

### Demonstrated Circuits
1. **Default 2-layer cascade:** Csy4 inhibits CasE, CasE can't inhibit mNeonGreen → green ON
2. **3-layer cascade:** PgU → Csy4 → CasE → mNeonGreen → green OFF
3. **AND gate:** CasE and Csy4 both converge on mKO2 via dual-recognition part

### Strengths
- Works in **human cells** (HEK293) — directly relevant to therapeutic applications
- Simple, modular abstraction — `X_rec_Y` is the only wiring primitive needed
- Weights set by pipetting amounts, not genetic engineering
- Rapid design iteration with computational tools (NeuromorphicWizard)
- Accessible to students and newcomers

### Limitations
- Currently limited to 3 ERNs (CasE, Csy4, PgU) — constrains network depth
- Less mathematical formalism than the perceptgene framework
- Analog behavior less precisely characterized
- Haven't yet demonstrated optimization/learning algorithms

---

## What's Genuinely New

### 1. Human Cells
The 2022 paper worked exclusively in *E. coli*. Moving to HEK293 cells opens the door to biomedical applications — diagnostics, therapeutics, cell-based therapies — where bacterial systems can't go.

### 2. Post-Transcriptional Computation
The perceptgene framework depends entirely on transcriptional regulation: promoter binding, transcription factor interactions, Hill coefficients of DNA-protein binding. The ERN approach operates at the mRNA level, which:
- Avoids the complexity of engineering promoter-transcription factor pairs
- May be faster (mRNA degradation is quicker than transcriptional repression)
- Is orthogonal to the host's native transcription — less interference with cellular functions

### 3. Simplified Weight Control
In the 2022 paper, changing a weight required either: mutating a promoter, changing an inducer concentration, adding a degradation tag, or engineering protein sequestration. In the ERN approach, weights are set by how much DNA you add — a purely quantitative, not genetic, adjustment.

### 4. Modular Design Tools
The NeuromorphicWizard provides simulation-before-fabrication, automated OT-2 protocol generation, and plate layout visualization. The 2022 paper relied on manual experimental iteration.

---

## Ron Weiss and Ramez Daniel: The Research Lineage

### Ron Weiss — MIT
Ron Weiss is Professor of Biological Engineering and EECS at MIT, directing the **Synthetic Biology Group** within MIT's Research Laboratory of Electronics (RLE). He is one of the pioneers of synthetic biology, having been engaged in the field since 1996 as a graduate student at MIT. His lab uses computer engineering principles — abstraction, composition, interface specifications — to program cells with sensors and actuators controlled by analog and digital logic circuitry.

Weiss teaches **Genetic Circuits Part II: Neuromorphic Circuits** in the HTGAA (How To Grow Almost Anything) course at MIT, directly connecting his research to the ERN-based lab module. This means the HTGAA Week 7 lab is not just inspired by the 2022 paper — it's the next step in Weiss's own research program, translated into a teaching context.

### Ramez Daniel — Technion
Ramez Daniel is faculty in the Department of Biomedical Engineering at the **Technion — Israel Institute of Technology**. He was the corresponding/senior author on the 2022 Nature Communications paper. His lab focuses on synthetic gene circuits, biological computing, and neural-network-inspired genetic architectures. Daniel is also involved in the [NeuCHiP](https://neuchip.eu/) EU project on neuromorphic computing.

### Key Publications in This Lineage

**2020:** Weiss lab published ["An endoribonuclease-based feedforward controller for decoupling resource-limited genetic modules in mammalian cells"](https://www.nature.com/articles/s41467-020-19126-9) (Nature Communications). This earlier work already used **CasE endoribonuclease in mammalian cells** as a feedforward controller — a direct precursor to the ERN-based neural networks in HTGAA 2026. This paper established that ERNs could be used as precise, orthogonal regulators in human cells.

**2022:** ["Synthetic neuromorphic computing in living cells"](https://www.nature.com/articles/s41467-022-33288-8) (Nature Communications) — the perceptgene paper in *E. coli*, establishing the theoretical and experimental framework.

**2025 (December, preprint):** ["Design principles of neuromorphic computing using genetic circuits"](https://www.biorxiv.org/content/10.64898/2025.12.01.691482v1) (bioRxiv) — a new preprint formalizing the design principles, identifying the key feature that enables a chemical reaction network to function as a perceptron: an input-output mapping with a tunable threshold. Identifies four fundamental circuit motifs: molecular sequestration, catalytic degradation, activation/deactivation cycles, and competitive binding.

**2026 (February):** ["Harnessing synthetic biology for energy-efficient bioinspired electronics: applications for logarithmic data converters"](https://www.nature.com/articles/s44172-026-00589-5) (Communications Engineering) — takes the perceptgene's logarithmic encoding and maps it into **electronic hardware**. A bio-inspired logarithmic ADC compresses 80 dB dynamic range into 3 bits while consuming <1 uW and occupying 0.02 mm^2. This shows the ideas flowing *back* from biology into electronics.

---

## The Trajectory

The progression shows a clear research arc across multiple labs and years:

**2020:** Prove ERNs work in mammalian cells (Weiss lab, endoribonuclease feedforward controller in HEK293).

**2022:** Prove neuromorphic computing works in cells with full mathematical framework, in *E. coli* (Weiss + Daniel, perceptgene paper).

**2025:** Formalize the design principles — what makes any chemical reaction network capable of perceptron-like computation (bioRxiv preprint).

**2026 (course):** Make it practical and accessible — move to human cells, use ERN-based post-transcriptional regulation, build design tools, teach it in HTGAA. Ron Weiss himself teaches this module.

**2026 (electronics):** Close the loop — map biological circuit principles back into ultra-low-power electronic hardware (logarithmic ADC paper).

The deep theory from the perceptgene paper (log-domain algebra, backpropagation, weight optimization) is being formalized into general design principles. Meanwhile, the ERN approach demonstrated in HTGAA brings the vision into human cells with a simpler, more modular abstraction. And the electronics paper shows these ideas have legs beyond biology entirely.

The fact that Weiss teaches this HTGAA module himself suggests this isn't just a pedagogical exercise — it's the frontier of where his research is heading: neuromorphic computation in mammalian cells using post-transcriptional (ERN-based) regulation, with the theoretical framework from the *E. coli* work providing the mathematical backbone.

---

## References

- Weiss Lab Publications: https://weiss-lab.mit.edu/publications/
- Rizik, L., Danial, L., Habib, M., Weiss, R. & Daniel, R. Synthetic neuromorphic computing in living cells. *Nature Communications* **13**, 5602 (2022). https://www.nature.com/articles/s41467-022-33288-8
- Jones, R.D. et al. An endoribonuclease-based feedforward controller for decoupling resource-limited genetic modules in mammalian cells. *Nature Communications* **11**, 5690 (2020). https://www.nature.com/articles/s41467-020-19126-9
- Bisso, F.B. et al. Design principles of neuromorphic computing using genetic circuits. *bioRxiv* (2025). https://www.biorxiv.org/content/10.64898/2025.12.01.691482v1
- Oren et al. Harnessing synthetic biology for energy-efficient bioinspired electronics. *Communications Engineering* (2026). https://www.nature.com/articles/s44172-026-00589-5
- HTGAA 2026: https://pages.htgaa.org/2026a/course-pages/index.print.html
