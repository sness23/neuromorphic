# Applications of ERN-Based Neuromorphic Circuits in Human Cells

## Why This Matters

The HTGAA 2026 approach — endoribonuclease (ERN) neural networks in HEK293 human cells — unlocks applications that were impossible with the earlier *E. coli* perceptgene work. The key enablers:

- **Human cells**: directly relevant to therapy, not just proof-of-concept
- **Post-transcriptional regulation**: faster, orthogonal to host gene expression, resistant to epigenetic silencing
- **Analog computation**: graded responses, not just ON/OFF — matching the continuous nature of biological signals
- **Modular wiring**: `X_rec_Y` parts can be recombined without re-engineering promoters

---

## Near-Term Applications

### 1. Smarter Cancer Immunotherapy

**The problem:** Current CAR-T cells and engineered immune cells use simple ON/OFF logic — they recognize one antigen and activate fully. This causes toxicity (cytokine storms) when the target antigen also appears on healthy tissue.

**What ERN circuits enable:** Analog, multi-input decision-making inside therapeutic cells. Instead of a binary kill switch, an ERN neural network could:
- Detect **multiple biomarkers simultaneously** (e.g., 2-3 cancer surface markers)
- Produce a **graded therapeutic response** proportional to the biomarker levels detected — high expression in tumor, low expression near healthy tissue
- Implement a **minimum function** (as demonstrated in the 2022 perceptgene paper) so that therapy activates only when *all* required markers are present above threshold

This directly addresses the 2022 paper's own suggestion: "The minimum operation may improve safety and efficacy of genetic circuits for cancer immunotherapy because it enables recognition of cancer biomarkers in a manner reminiscent of an AND logic gate... but in contrast to AND logic, the minimum operation will activate the immunotherapy at levels proportional to the biomarkers detected, which may reduce undesirable effects such as cytokine storms."

The ERN approach makes this feasible in human immune cells, not just *E. coli*.

**Related work:** Synthetic gene circuits for CAR-T safety switches ([Science Advances, 2024](https://www.science.org/doi/10.1126/sciadv.adj6251)); c-MYC sensing circuits that activate immunostimulatory agents only in tumor microenvironments ([Nature Communications, 2025](https://www.nature.com/articles/s41467-025-63377-3)).

### 2. Precision Cell-Based Therapies

**The problem:** Engineered cell therapies (for diabetes, autoimmune disease, hormone disorders) need to sense internal or external signals and respond with precisely dosed outputs — not just "gene ON" or "gene OFF."

**What ERN circuits enable:**
- **Analog-to-digital conversion** inside cells: a continuous biomarker concentration converted to discrete therapeutic responses (the 2-bit ADC from the perceptgene paper, now achievable in human cells)
- **Ternary switches**: three-level output from a single input — e.g., low/medium/high insulin secretion based on blood glucose sensing
- **Noise-tolerant averaging**: the average function filters out biological noise, producing stable outputs even when individual signals fluctuate

**Example:** An implanted cell therapy for diabetes that senses glucose at the mRNA level and produces insulin at three discrete doses (low, medium, high) rather than a simple on/off, reducing the risk of hypoglycemia.

### 3. Multi-Input Biosensors and Diagnostics

**The problem:** Current whole-cell biosensors typically detect one analyte with one output. Clinically useful diagnostics need to integrate multiple signals.

**What ERN circuits enable:**
- **Multi-analyte classification**: ERN neural networks process 2-3 inputs simultaneously and produce a classified output (e.g., "healthy" vs. "diseased" based on a panel of biomarkers)
- **Analog readout**: fluorescent output intensity encodes not just presence/absence but *severity* — useful for grading disease states
- **Programmable logic**: the same cell line can be reprogrammed for different diagnostic panels by changing plasmid ratios (weights), without genetic re-engineering

**Example:** A HEK293-based diagnostic cell line that detects combinations of inflammatory cytokines in a blood sample and produces a color-coded fluorescent output indicating disease severity. The four available fluorescent reporters (green, orange, blue, maroon) could encode a 4-channel readout.

**Related work:** HEK293-based biosensors with synthetic histamine-responsive modules for allergy detection from blood samples; whole-cell copper biosensors ([Nature Communications, 2024](https://www.nature.com/articles/s41467-024-47592-y)).

### 4. Controllable Gene Expression for Biomanufacturing

**The problem:** Producing therapeutic proteins (antibodies, enzymes, growth factors) in mammalian cell factories requires precise control over expression timing and levels. Current approaches use simple inducible promoters with limited dynamic range.

**What ERN circuits enable:**
- **Multi-gene coordination**: ERN cascades can sequence the activation of multiple genes — e.g., first produce a chaperone, then produce the therapeutic protein, then produce a quality-control reporter
- **Analog dosing**: protein production levels tuned by DNA ratios rather than inducer concentrations, enabling fine-grained control in bioreactors
- **Pathway balancing**: inhibition chains naturally create feedback-like regulation where overproduction of one enzyme suppresses upstream components

**Related work:** Review of mammalian synthetic gene circuits for biopharmaceutical development ([npj Systems Biology and Applications, 2025](https://www.nature.com/articles/s41540-025-00621-y)).

### 5. Tissue Engineering and Morphogenesis

**The problem:** Building complex tissues from stem cells requires cells to make context-dependent decisions — differentiate into type A here, type B there — based on multiple signals from neighboring cells and the extracellular environment.

**What ERN circuits enable:**
- **Graded differentiation signals**: analog ERN circuits produce transcription factor levels proportional to input signals, enabling smooth gradients rather than sharp boundaries
- **Multi-input integration**: cells sense position, neighbor signals, and time simultaneously and compute an appropriate differentiation program
- **Programmable cell fate**: by changing DNA ratios at transfection time, the same circuit can be tuned to produce different tissue architectures

This is directly aligned with Ron Weiss's stated research direction — he has described neuromorphic computing in cells as a tool for "coaxing stem cells into various specialized tissues and controlling their development with meticulous precision."

**Related work:** Weiss lab work on programmed morphogenesis with engineered HEK293 and CHO cells.

---

## Longer-Term Possibilities

### 6. In Vivo Programmable Therapeutics

As lipid nanoparticle (LNP) delivery of mRNA matures ([Nature, 2026](https://www.nature.com/articles/s41586-026-10235-x) — in vivo CAR-T generation via targeted LNPs), it becomes conceivable to deliver ERN circuit components as mRNA directly to cells in the body. This could enable:
- Transient neuromorphic computation inside a patient's own cells
- No permanent genetic modification — mRNA degrades naturally
- Programmable therapeutic responses that last days to weeks

### 7. Biological Machine Learning

The 2022 paper demonstrated backpropagation in *E. coli* — iteratively tuning weights to minimize a cost function. With ERN circuits in human cells, this could evolve toward:
- Cells that **adapt their behavior** based on environmental feedback
- Patient-derived cells trained on a patient's specific biomarker profile
- Hybrid systems where computational optimization (NeuromorphicWizard) designs circuits that are then fine-tuned via wet-lab gradient descent

### 8. Bio-Electronic Interfaces

The 2026 paper ["Harnessing synthetic biology for energy-efficient bioinspired electronics"](https://www.nature.com/articles/s44172-026-00589-5) already maps perceptgene principles into electronic hardware. ERN circuits in human cells could serve as the biological half of hybrid bio-electronic systems — cells performing analog computation, electronics handling digital readout and feedback.

---

## The PERSIST Advantage

A critical enabler for all these applications is the **PERSIST platform** ([Nature Communications, 2022](https://www.nature.com/articles/s41467-022-30172-3)), which uses CRISPR endoRNases (the same family as CasE, Csy4, PgU) as RNA-level regulators that **resist epigenetic silencing** for 2+ months in mammalian cells. Traditional transcription-factor-based circuits in mammalian cells tend to get silenced within weeks as the cell's epigenetic machinery shuts down the foreign promoters. ERN-based circuits operating at the RNA level sidestep this problem, making long-term therapeutic applications viable.

---

## Summary

| Application | Key ERN Capability | Timeline |
|---|---|---|
| Cancer immunotherapy | Multi-input analog classification | Near-term |
| Precision cell therapy | ADC, ternary switch, averaging | Near-term |
| Multi-analyte diagnostics | Programmable logic, 4-channel readout | Near-term |
| Biomanufacturing control | Cascaded gene coordination | Near-term |
| Tissue engineering | Graded differentiation signals | Medium-term |
| In vivo mRNA therapeutics | Transient computation via LNP delivery | Longer-term |
| Biological machine learning | Wet-lab backpropagation in human cells | Longer-term |
| Bio-electronic hybrids | Analog bio + digital electronic readout | Longer-term |

The HTGAA 2026 ERN approach is not just a teaching exercise — it's a platform technology. By combining the theoretical framework from the 2022 perceptgene paper with the modularity and human-cell compatibility of ERN circuits, it opens a path from proof-of-concept bacterial computing to real therapeutic and industrial applications.

---

## References

- Rizik et al. Synthetic neuromorphic computing in living cells. *Nat Commun* 13, 5602 (2022). https://www.nature.com/articles/s41467-022-33288-8
- Jones et al. An endoribonuclease-based feedforward controller. *Nat Commun* 11, 5690 (2020). https://www.nature.com/articles/s41467-020-19126-9
- Gao et al. PERSIST platform. *Nat Commun* 13, 2835 (2022). https://www.nature.com/articles/s41467-022-30172-3
- Oren et al. Bio-inspired logarithmic data converters. *Commun Eng* (2026). https://www.nature.com/articles/s44172-026-00589-5
- Bisso et al. Design principles of neuromorphic computing. *bioRxiv* (2025). https://www.biorxiv.org/content/10.64898/2025.12.01.691482v1
- Synthetic gene circuits for cell-based therapeutics. *Adv Sci* (2024). https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202309088
- In vivo site-specific T cell engineering. *Nature* (2026). https://www.nature.com/articles/s41586-026-10235-x
- Next-gen programmable cell therapies. *Nat Rev Genet* (2026). https://www.nature.com/articles/s41576-026-00945-3
- HTGAA 2026 Week 7. https://pages.htgaa.org/2026a/course-pages/index.print.html
