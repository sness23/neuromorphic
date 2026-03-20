# Transfection Groups: X1, X2, and Bias

## What Are Transfection Groups?

A **transfection group** is a set of plasmids that are physically mixed together in one tube before being delivered to the cell. Each group enters via its own lipid nanoparticle, but all groups end up in the same cell.

In the design template CSV, the transfection group is the second column:

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
MyCircuit,X1,Csy4,50,150
MyCircuit,X1,mKO2,50,100
MyCircuit,X2,Csy4_rec_CasE,50,100
MyCircuit,X2,eBFP2,50,100
MyCircuit,Bias,CasE_rec_mNeonGreen,50,200
```

Rows with the same group label are mixed into a single tube and co-transfected together.

## What X1, X2, and Bias Actually Mean

The names come from the HTGAA 2026 course design template and borrow neural network notation (x₁, x₂, bias). But **the labels are really just names for separate physical tubes** — they don't have a fixed computational meaning.

This becomes clear when you look at how different circuits use them:

### Default circuit (2-layer cascade)

| Group | Contents | Computational role |
|-------|----------|--------------------|
| X1 | Csy4 + mKO2 | Csy4 is the **top of the chain** (unregulated ERN) |
| X2 | Csy4_rec_CasE + eBFP2 | CasE is a **middle layer** (regulated by Csy4) |
| Bias | CasE_rec_mNeonGreen | mNeonGreen is the **output** (regulated by CasE) |

Here X2 is not an "input" at all — it contains a component that is actively inhibited by X1.

### Three-layer cascade

| Group | Contents | Computational role |
|-------|----------|--------------------|
| X1 | PgU + eBFP2 | PgU is the **top of the chain** (unregulated) |
| X2 | PgU_rec_Csy4 + mMaroon1 | Csy4 is **layer 2** (regulated by PgU) |
| X3 | Csy4_rec_CasE | CasE is **layer 3** (regulated by Csy4) |
| Bias | CasE_rec_mNeonGreen | mNeonGreen is the **output** |

Again, X2 is a middle layer, and there's even an X3.

### AND gate

| Group | Contents | Computational role |
|-------|----------|--------------------|
| X1 | CasE | True input #1 (unregulated) |
| X2 | Csy4 | True input #2 (unregulated) |
| Output | CasE_rec_Csy4_rec_mKO2 | The gate output |
| Control | eBFP2 + mNeonGreen | Transfection controls |

Here X1 and X2 really are both independent inputs converging on one target. And the group names "Output" and "Control" are used instead of "Bias".

### The pattern

X1/X2/Bias is a naming convention, not a fixed architecture. The groups define **which plasmids share a tube**, not their role in the circuit logic. The same label can hold an unregulated ERN, a regulated middle-layer component, or just a reporter — depending on the circuit design.

## Why Separate Groups?

Splitting plasmids into separate transfection groups means they enter the cell in **different lipid nanoparticles**. While all groups ultimately end up in the same cell, delivering them separately matters for:

- **Experimental control** — you can remove an entire group to test its contribution (e.g., remove the group containing Csy4 and see if the output changes)
- **Stoichiometry** — the ratio of plasmids within a group is more tightly controlled than between groups
- **Physical protocol** — each group gets its own mixing tube, its own lipofectamine tube, and its own pipetting steps on the OT-2

## The Labels Are Free-Text

X1, X2, Bias, Output, Control — these are all just arbitrary labels. The NeuromorphicWizard treats the transfection group column as free text. You could name them "TubeA" and "TubeB" and the protocol would work identically. The x₁/x₂/bias convention exists to gesture at the neural network analogy, but it maps loosely at best.
