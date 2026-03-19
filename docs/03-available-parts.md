# Available Genetic Parts

The plasmid library from the Weiss Lab provides four categories of parts for building neuromorphic circuits.

## Part Categories

### 1. ERNs (Endoribonucleases)

Standalone enzymes that cut RNA at specific recognition sequences. These are the "neurons" that perform computation.

- `CasE`
- `Csy4`
- `PgU`

### 2. ERN_rec_ERN (ERN-regulated ERNs)

An ERN whose mRNA contains a recognition sequence for another ERN. This creates inhibitory connections between neurons.

- `PgU_rec_Csy4` -- PgU production is inhibited by Csy4
- `PgU_rec_CasE` -- PgU production is inhibited by CasE
- `Csy4_rec_CasE` -- Csy4 production is inhibited by CasE
- `CasE_rec_Csy4` -- CasE production is inhibited by Csy4

### 3. ERN_rec_Color (ERN-regulated Reporters)

A fluorescent reporter whose mRNA contains a recognition sequence for an ERN. These are the visible outputs.

- `Csy4_rec_mNeonGreen` -- mNeonGreen inhibited by Csy4
- `CasE_rec_mNeonGreen` -- mNeonGreen inhibited by CasE
- `PgU_rec_mNeonGreen` -- mNeonGreen inhibited by PgU
- `CasE_rec_Csy4_rec_mKO2` -- mKO2 inhibited by both CasE and Csy4

### 4. Colors (Unregulated Reporters)

Fluorescent proteins expressed constitutively (always on). Useful as controls or simple readouts.

- `mKO2` (orange)
- `eBFP2` (blue)
- `mMaroon1` (maroon/red)
- `mNeonGreen` (green)

## Combining Parts

Parts are grouped into **transfection groups**. Plasmids within the same transfection group are mixed together in one tube before being delivered to the cell. Different transfection groups are delivered separately but end up in the same cell.

The naming convention `ERN_rec_Target` always means: "Target's mRNA will be cut (inhibited) by ERN."
