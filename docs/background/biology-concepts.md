# Biology Concepts

## Endoribonucleases (ERNs)

Endoribonucleases are enzymes that cut RNA molecules at specific recognition sequences. In this system, they are the computational building blocks -- each ERN acts like a "neuron" that can suppress (inhibit) the production of a target protein by cutting its mRNA.

The available ERNs are:

| ERN | Description |
|-----|-------------|
| **Csy4** | CRISPR-associated endoribonuclease |
| **CasE** | CRISPR-associated endoribonuclease |
| **PgU** | Endoribonuclease |

## Recognition and Cutting

A plasmid named `ERN_rec_Target` means the Target gene's mRNA contains a recognition sequence for the named ERN. When that ERN is present in the cell, it finds and cleaves the Target mRNA, preventing translation of the Target protein.

For example:
- `Csy4_rec_CasE` -- CasE mRNA has a Csy4 recognition site. If Csy4 is present, it cuts CasE mRNA, suppressing CasE production.
- `CasE_rec_mNeonGreen` -- mNeonGreen mRNA has a CasE recognition site. If CasE is present, it cuts mNeonGreen mRNA.

This creates **inhibitory connections** between components, analogous to inhibitory synapses in biological neural networks.

## Fluorescent Reporters

Fluorescent proteins serve as visible outputs -- you can measure their expression levels using fluorescence microscopy or flow cytometry.

| Reporter | Color |
|----------|-------|
| **mKO2** | Orange |
| **eBFP2** | Blue |
| **mMaroon1** | Maroon/Red |
| **mNeonGreen** | Green |

## HEK293 Cells

HEK293 (Human Embryonic Kidney 293) cells are an immortalized cell line originally derived in 1973 by Frank Graham from kidney cells in Alex van der Eb's lab in the Netherlands. The "293" refers to the 293rd experiment.

They are one of the most widely used cell lines in biology because they:
- Grow fast and are easy to maintain in culture
- Are very easy to transfect (high uptake of foreign DNA)
- Are well-characterized and produce reproducible results

Labs obtain HEK293 cells from cell line repositories (e.g., ATCC) or commercial suppliers. They have been continuously cultured for over 50 years.

## Lipofectamine 3000

Lipofectamine 3000 is a lipid-based transfection reagent. It forms lipid nanoparticles around plasmid DNA, which then fuse with the cell membrane to deliver DNA into the cell. The protocol uses:

- **Opti-MEM**: Reduced serum medium for dilution
- **P3000**: Enhancer reagent mixed with DNA
- **L3000**: Lipofectamine reagent mixed separately, then combined with the DNA/P3000 mixture

The ratios used in the OT-2 protocol (per ng of DNA):
- Opti-MEM: 0.05 uL/ng
- P3000: 0.0022 uL/ng
- L3000: 0.0022 uL/ng
- Excess multiplier: 1.2x (to account for pipetting error)
