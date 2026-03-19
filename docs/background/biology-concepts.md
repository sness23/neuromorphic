# Biology Concepts

This document explains every biological concept used in the lab, building up from the absolute basics.

---

## Part 1: How Cells Make Proteins

### DNA → mRNA → Protein

This is the most important concept. Every protein in a cell is made in two steps:

```
Step 1: TRANSCRIPTION              Step 2: TRANSLATION

  DNA ──────────────▶ mRNA ──────────────▶ Protein
  (permanent          (temporary           (the thing that
   blueprint)          photocopy)           actually does work)
```

**Step 1 — Transcription:** The cell makes a temporary copy of a gene. This copy is called **mRNA** (messenger RNA). Think of DNA as the master cookbook that stays in the vault, and mRNA as a photocopy of one recipe that gets taken to the kitchen.

**Step 2 — Translation:** The cell's machinery (ribosomes) reads the mRNA and builds the protein, one amino acid at a time. This is like following the photocopied recipe to cook the dish.

**The key insight for our lab:** If you destroy the mRNA (the photocopy) before the ribosome reads it, the protein never gets made. No photocopy → no dish. This is exactly how our circuits work.

### What is a plasmid?

A plasmid is a small, circular piece of DNA that we design on a computer and have manufactured. When we put a plasmid into a cell, the cell reads it just like its own DNA — it transcribes it into mRNA and translates it into protein.

Each plasmid in our lab encodes **one protein**. Put the plasmid in → the cell makes that protein. It's that simple.

### What is transfection?

Cells don't want foreign DNA. Transfection is the trick we use to get our plasmids inside. **Lipofectamine 3000** wraps the plasmid DNA in tiny fat bubbles (lipid nanoparticles) that fuse with the cell membrane and dump the DNA inside. Like disguising a package to get it past security.

---

## Part 2: The Two Types of Proteins in Our Lab

### Fluorescent proteins (the readout)

These proteins glow specific colors when you shine the right light on them. They're the indicator lights on our circuit — they tell us what's happening inside the cell.

| Protein | Color | What you see under the microscope |
|---------|-------|----------------------------------|
| **mKO2** | Orange | Orange glow |
| **eBFP2** | Blue | Blue glow |
| **mMaroon1** | Maroon/Red | Red glow |
| **mNeonGreen** | Green | Green glow |

If the cell is making a fluorescent protein → you see that color.
If the cell is NOT making it → that color is dark/absent.

### Endoribonucleases — ERNs (the scissors)

An ERN is an enzyme (a type of protein) that **cuts RNA**. Let's break the word down:
- **endo** = cuts in the middle
- **ribo** = RNA
- **nuclease** = enzyme that cuts nucleic acids

Our lab uses three ERNs:

| ERN | What it does |
|-----|-------------|
| **CasE** | Cuts mRNA that has a CasE recognition sequence |
| **Csy4** | Cuts mRNA that has a Csy4 recognition sequence |
| **PgU** | Cuts mRNA that has a PgU recognition sequence |

**The critical detail:** An ERN doesn't cut ALL mRNA. It only cuts mRNA that contains a specific **recognition sequence** — a particular short string of RNA letters (~20-30 letters) that the ERN recognizes.

Think of it like a paper shredder that only shreds documents with a specific barcode:

```
ERN scans all mRNA in the cell...

  mRNA without the barcode  →  SAFE, protein gets made  ✓
  mRNA WITH the barcode     →  CUT AND DESTROYED, protein never made  ✗
```

Each ERN has a **different** barcode. CasE cannot cut Csy4's targets. Csy4 cannot cut CasE's targets. They are independent scissors.

---

## Part 3: The Naming Convention

This is where everything clicks. The part names tell you exactly what inhibits what.

### The rule: `X_rec_Y` means "X inhibits Y"

In the name `X_rec_Y`:
- **X** = the ERN whose recognition sequence is on the mRNA (the inhibitor)
- **rec** = "recognition sequence"
- **Y** = the protein encoded by this plasmid (the target that gets inhibited)

The plasmid **produces Y**, but Y's mRNA has X's recognition sequence embedded in it. So if X enzyme is present in the cell, X finds the mRNA and cuts it, and Y protein is never made.

### Walking through every example

**`Csy4_rec_CasE`**

| Question | Answer |
|----------|--------|
| What protein does this plasmid produce? | **CasE** (the second name) |
| What recognition sequence is on the mRNA? | **Csy4's** recognition sequence (the first name) |
| What happens if Csy4 enzyme is in the cell? | Csy4 finds CasE's mRNA, cuts it → **CasE is NOT made** |
| What happens if Csy4 is NOT in the cell? | Nobody cuts CasE's mRNA → **CasE IS made normally** |
| **Summary:** | **Csy4 inhibits CasE** |

**`CasE_rec_mNeonGreen`**

| Question | Answer |
|----------|--------|
| What protein does this plasmid produce? | **mNeonGreen** (green fluorescent protein) |
| What recognition sequence is on the mRNA? | **CasE's** recognition sequence |
| What happens if CasE enzyme is in the cell? | CasE finds mNeonGreen's mRNA, cuts it → **no green glow** |
| What happens if CasE is NOT in the cell? | mNeonGreen is made → **cell glows green** |
| **Summary:** | **CasE inhibits mNeonGreen** |

**`PgU_rec_Csy4`**

| Question | Answer |
|----------|--------|
| What protein does this plasmid produce? | **Csy4** enzyme |
| What recognition sequence is on the mRNA? | **PgU's** recognition sequence |
| What happens if PgU enzyme is in the cell? | PgU finds Csy4's mRNA, cuts it → **Csy4 is NOT made** |
| What happens if PgU is NOT in the cell? | Csy4 is made normally → **Csy4 is active** |
| **Summary:** | **PgU inhibits Csy4** |

**`CasE_rec_Csy4_rec_mKO2`** (special dual-recognition part)

| Question | Answer |
|----------|--------|
| What protein does this plasmid produce? | **mKO2** (orange fluorescent protein) |
| What recognition sequences are on the mRNA? | **Both** CasE's AND Csy4's recognition sequences |
| What happens if CasE is in the cell? | CasE cuts mKO2's mRNA → **no orange** |
| What happens if Csy4 is in the cell? | Csy4 cuts mKO2's mRNA → **no orange** |
| What happens if BOTH are in the cell? | Both cut it → **definitely no orange** |
| What happens if NEITHER is in the cell? | Nobody cuts it → **orange ON** |
| **Summary:** | **Either CasE or Csy4 (or both) inhibits mKO2** |

### How to think about it: ERNs scan for their own tag

Each ERN is constantly scanning all mRNA in the cell, looking for **its own** recognition site — a specific RNA hairpin (~28-36 nucleotides) that acts like a barcode. Any mRNA carrying that barcode gets cut and destroyed.

The `_rec_` in a part name **is** that barcode, physically engineered into the mRNA:

```
PgU (the enzyme) scans all mRNA...

  mRNA from PgU_rec_Csy4        →  Has PgU's barcode!  →  CUT. No Csy4 made.
  mRNA from PgU_rec_CasE        →  Has PgU's barcode!  →  CUT. No CasE made.
  mRNA from PgU_rec_mNeonGreen  →  Has PgU's barcode!  →  CUT. No green.
  mRNA from Csy4_rec_CasE       →  No PgU barcode.     →  SAFE. Ignored.
  mRNA from mKO2                →  No PgU barcode.     →  SAFE. Ignored.
```

The same logic applies to each ERN — it only sees its own barcode:

```
CasE scans for CasE_rec    →  cuts any mRNA tagged with CasE_rec
Csy4 scans for Csy4_rec    →  cuts any mRNA tagged with Csy4_rec
PgU  scans for PgU_rec     →  cuts any mRNA tagged with PgU_rec
```

They are completely independent. CasE cannot see `Csy4_rec`. Csy4 cannot see `PgU_rec`. This **orthogonality** is what makes it possible to wire complex circuits — each connection is a specific barcode on a specific mRNA, and only the matching enzyme can cut it.

**Reading the name:** `X_rec_Y` → "X's **rec**ognition site is on Y's mRNA" → X recognizes and cleaves Y.

### What about plain ERN names and color names?

Parts like `CasE`, `Csy4`, `PgU` (no `_rec_` in the name) have **no recognition sequence** on their mRNA. No ERN can inhibit them. They are always active when expressed.

Parts like `mKO2`, `eBFP2`, `mMaroon1`, `mNeonGreen` (no `_rec_`) similarly have no recognition sequences. They always glow when expressed. They serve as **controls** — if you see their color, the transfection worked.

---

## Part 4: Building Circuits by Chaining Inhibitions

### Single inhibition: one step

Put Csy4 (free enzyme) and `Csy4_rec_mNeonGreen` into the same cell:

```
Csy4 ──inhibits──▶ mNeonGreen

Csy4 is active → cuts mNeonGreen mRNA → green is OFF
```

### Double inhibition: two steps (the default circuit)

Put Csy4, `Csy4_rec_CasE`, and `CasE_rec_mNeonGreen` into the same cell:

```
Csy4 ──inhibits──▶ CasE ──inhibits──▶ mNeonGreen

Step 1: Csy4 is active → cuts CasE mRNA → CasE is OFF
Step 2: CasE is OFF → can't cut mNeonGreen → green is ON

Two negatives make a positive!
```

### Triple inhibition: three steps (our ThreeLayer circuit)

Put PgU, `PgU_rec_Csy4`, `Csy4_rec_CasE`, and `CasE_rec_mNeonGreen` into the same cell:

```
PgU ──inhibits──▶ Csy4 ──inhibits──▶ CasE ──inhibits──▶ mNeonGreen

Step 1: PgU is active     → cuts Csy4 mRNA  → Csy4 is OFF
Step 2: Csy4 is OFF       → can't cut CasE  → CasE is ON
Step 3: CasE is ON        → cuts mNeonGreen → green is OFF

Three negatives make a negative!
```

### The pattern

| Number of inhibitions | Output | Like multiplying... |
|----------------------|--------|-------------------|
| 1 (odd) | OFF | (-1) = -1 |
| 2 (even) | ON | (-1) × (-1) = +1 |
| 3 (odd) | OFF | (-1) × (-1) × (-1) = -1 |

---

## Part 5: Why It's "Analog" Not Digital

The amounts matter. If you put in 200 ng of Csy4 and only 50 ng of `Csy4_rec_CasE`, Csy4 overwhelmingly destroys CasE's mRNA. But if you reverse the amounts — 50 ng of Csy4 and 200 ng of `Csy4_rec_CasE` — there might be so much CasE mRNA being produced that Csy4 can't cut it all fast enough. Some CasE protein leaks through.

This is why the circuits are "neuromorphic" — like real neurons, the output is a **continuous value** that depends on the relative strengths of inputs, not a binary ON/OFF switch.

---

## Part 6: The Complete Inhibition Map

Here is every possible inhibition with the available parts:

```
PgU ──can inhibit──▶ Csy4  (via PgU_rec_Csy4)
PgU ──can inhibit──▶ CasE  (via PgU_rec_CasE)
Csy4 ──can inhibit──▶ CasE  (via Csy4_rec_CasE)
CasE ──can inhibit──▶ Csy4  (via CasE_rec_Csy4)

PgU ──can inhibit──▶ mNeonGreen   (via PgU_rec_mNeonGreen)
CasE ──can inhibit──▶ mNeonGreen   (via CasE_rec_mNeonGreen)
Csy4 ──can inhibit──▶ mNeonGreen   (via Csy4_rec_mNeonGreen)

CasE + Csy4 ──can inhibit──▶ mKO2  (via CasE_rec_Csy4_rec_mKO2)
```

Notice:
- **PgU** can inhibit both other ERNs (Csy4 and CasE) — it's the most powerful inhibitor
- **CasE and Csy4** can inhibit each other, but **neither can inhibit PgU**
- **PgU** is the only ERN that can start a 3-layer cascade (because it's the only one nobody can inhibit through wiring parts)
- **mKO2** can only be regulated by the dual-recognition part (both CasE and Csy4)
- **mMaroon1** has no regulated version — it's always a constitutive control

---

## Part 7: HEK293 Cells

HEK293 (Human Embryonic Kidney 293) cells are the host cells we use. Key facts:

- **Origin:** Derived once in 1973 from kidney cells of a legally aborted fetus in the Netherlands. The "293" refers to the 293rd experiment by Frank Graham.
- **Immortalized:** These cells divide indefinitely in the lab. They've been continuously cultured for 50+ years.
- **Where labs get them:** Cell line repositories (ATCC) or commercial suppliers (Thermo Fisher). No new embryonic tissue is needed.
- **Why we use them:** They grow fast, are extremely easy to transfect (high DNA uptake), and produce reproducible results.

---

## Part 8: Lipofectamine 3000 Transfection

Lipofectamine 3000 is how we get plasmid DNA into cells. The process has three components:

| Component | What it is | Role |
|-----------|-----------|------|
| **Opti-MEM** | Reduced serum cell culture medium | Dilution buffer — provides the right environment |
| **P3000** | Enhancer reagent | Binds to DNA, helps it get packaged into nanoparticles |
| **L3000** | Lipofectamine reagent | The lipid molecules that form nanoparticles around the DNA |

### How it works, step by step:

1. **DNA + P3000** are mixed in Opti-MEM. P3000 coats the DNA.
2. **L3000** is mixed separately in Opti-MEM.
3. The two mixtures are **combined**. The lipid molecules self-assemble into nanoparticles (tiny fat bubbles) around the DNA.
4. You wait **10 minutes** for the nanoparticles to form.
5. The mixture is gently pipetted onto cells. The nanoparticles settle onto the cell surface.
6. The nanoparticles **fuse with the cell membrane** and release the DNA inside.
7. The cell starts reading the plasmid DNA and making proteins.

### Protocol ratios (per ng of DNA)

| Reagent | Amount per ng DNA | With 1.2x excess |
|---------|------------------|-------------------|
| Opti-MEM | 0.05 uL | 0.06 uL |
| P3000 | 0.0022 uL | 0.00264 uL |
| L3000 | 0.0022 uL | 0.00264 uL |

The 1.2x excess accounts for liquid lost to pipette tips and tube walls.
