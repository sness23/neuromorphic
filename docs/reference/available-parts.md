# Available Genetic Parts

The plasmid library from the Weiss Lab provides four categories of parts for building neuromorphic circuits.

## Part Categories

### 1. ERNs (Endoribonucleases)

Standalone enzymes that cut RNA at specific recognition sequences. These are the "neurons" that perform computation.

- `CasE`
- `Csy4`
- `PgU`

### 2. ERN_rec_ERN (ERN-regulated ERNs)

An ERN whose mRNA contains a recognition sequence for another ERN. This creates inhibitory connections between neurons. The naming convention is `X_rec_Y`: X is the inhibitor, Y is the target protein encoded by the plasmid. X's recognition sequence is on Y's mRNA.

- `PgU_rec_Csy4` -- PgU inhibits Csy4 (Csy4's mRNA has a PgU recognition sequence)
- `PgU_rec_CasE` -- PgU inhibits CasE (CasE's mRNA has a PgU recognition sequence)
- `Csy4_rec_CasE` -- Csy4 inhibits CasE (CasE's mRNA has a Csy4 recognition sequence)
- `CasE_rec_Csy4` -- CasE inhibits Csy4 (Csy4's mRNA has a CasE recognition sequence)

### 3. ERN_rec_Color (ERN-regulated Reporters)

A fluorescent reporter whose mRNA contains a recognition sequence for an ERN. These are the visible outputs.

- `Csy4_rec_mNeonGreen` -- Csy4 inhibits mNeonGreen
- `CasE_rec_mNeonGreen` -- CasE inhibits mNeonGreen
- `PgU_rec_mNeonGreen` -- PgU inhibits mNeonGreen
- `CasE_rec_Csy4_rec_mKO2` -- mKO2 inhibited by both CasE and Csy4

### 4. Colors (Unregulated Reporters)

Fluorescent proteins expressed constitutively (always on). Useful as controls or simple readouts.

- `mKO2` (orange)
- `eBFP2` (blue)
- `mMaroon1` (maroon/red)
- `mNeonGreen` (green)

## Combining Parts

Parts are grouped into **transfection groups**. Plasmids within the same transfection group are mixed together in one tube before being delivered to the cell. Different transfection groups are delivered separately but end up in the same cell.

The naming convention `X_rec_Y` always means: "X inhibits Y" — X's recognition sequence is on Y's mRNA, so if X is present, Y's mRNA is cut and Y is not produced.
