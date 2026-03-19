# The Big Picture: What This Lab Is Really About

## Starting from the Very Beginning

### What's a cell?

A human cell is a tiny bag of water surrounded by a membrane. Inside, it has DNA (the instruction manual) and molecular machinery that reads those instructions to make proteins. Proteins are the workers that do everything — they give cells structure, send signals, break down food, and so on.

### What's a plasmid?

A plasmid is a small, circular piece of DNA that you can design on a computer and have a company manufacture. When you put a plasmid into a cell, the cell reads it just like its own DNA and makes whatever protein the plasmid encodes.

### What's transfection?

Transfection is the process of getting plasmids into cells. The cells don't want foreign DNA, so you use a trick: Lipofectamine 3000 wraps the DNA in tiny fat bubbles (lipid nanoparticles) that fuse with the cell membrane and dump the DNA inside. It's like sneaking a package past security by disguising it.

### So what are we doing?

We're putting multiple plasmids into cells at the same time. Each plasmid makes a different protein. Some of those proteins interact with each other — specifically, some proteins destroy the instructions for making other proteins. By choosing which plasmids to put in, we can create a little network of interactions inside the cell. That network is the "circuit."

## What Makes This a "Neural Network"

A real neural network (like in your brain) has neurons that can activate or inhibit other neurons. This lab builds something similar inside a cell:

- Each **plasmid** is like a neuron
- **Endoribonucleases** (ERNs) are the connections between neurons
- An ERN **inhibits** its target by destroying the target's mRNA (the intermediate message between DNA and protein)

The key difference from traditional genetic circuits (which are digital — ON or OFF) is that these circuits are **analog**. The amount of protein produced depends on how much plasmid you put in and how much inhibition is happening. You get a spectrum of expression levels, not just binary switches.

## The Central Mechanism: How ERNs Work

This is the most important concept in the lab. Let's go through it very carefully.

### The Normal Path: DNA → mRNA → Protein

```
DNA (plasmid)
    │
    ▼  transcription (cell copies DNA into mRNA)
mRNA (messenger RNA)
    │
    ▼  translation (cell reads mRNA to build protein)
Protein (the final product that does something)
```

This happens automatically for every plasmid you put into the cell. The cell doesn't know or care what the plasmid encodes — it just reads it and makes the protein.

### What an ERN Does

An endoribonuclease (ERN) is a protein that **cuts RNA**. But it doesn't cut all RNA — it only cuts RNA that contains a specific **recognition sequence** (a particular string of RNA letters).

Think of it like a paper shredder that only shreds documents with a specific barcode on them.

```
ERN protein (e.g., Csy4)
    │
    ▼  scans all mRNA in the cell
    │
    ├── mRNA without recognition sequence → IGNORED (survives)
    │
    └── mRNA WITH Csy4 recognition sequence → CUT AND DESTROYED
         (protein never gets made)
```

### How the Parts Are Named

The naming convention tells you exactly what inhibits what:

**`Csy4_rec_CasE`** means:
- This plasmid encodes **CasE** protein
- But the mRNA has a **Csy4 recognition** sequence built into it
- So if Csy4 protein is present in the cell, it will find this mRNA and cut it
- Result: **Csy4 inhibits CasE production**

Read it as: "[inhibitor]\_rec\_[target]" → the inhibitor destroys the target.

More examples:
- `CasE_rec_mNeonGreen` → CasE destroys mNeonGreen mRNA → **CasE inhibits green fluorescence**
- `PgU_rec_Csy4` → Csy4 destroys PgU mRNA → **Csy4 inhibits PgU production**
- `CasE_rec_Csy4_rec_mKO2` → mKO2's mRNA has recognition sequences for **both** CasE and Csy4 → **either one can destroy it**

### The Three ERNs

There are three endoribonucleases available, each recognizing a different RNA sequence:

| ERN | What it does |
|-----|-------------|
| **Csy4** | Cuts any mRNA with a Csy4 recognition sequence |
| **CasE** | Cuts any mRNA with a CasE recognition sequence |
| **PgU** | Cuts any mRNA with a PgU recognition sequence |

They don't interact with each other directly. They only interact through the engineered recognition sequences on the plasmids you choose.

## Fluorescent Proteins: How You See the Result

You can't see proteins with your eyes. But **fluorescent proteins** glow specific colors when you shine the right wavelength of light on them. They're the readout — like indicator lights on a dashboard.

| Protein | Color | What you see |
|---------|-------|-------------|
| mKO2 | Orange | Orange glow under fluorescence microscope |
| eBFP2 | Blue | Blue glow |
| mMaroon1 | Maroon/Red | Red glow |
| mNeonGreen | Green | Green glow |

If a fluorescent protein's mRNA is being cut by an ERN, the protein doesn't get made, and that color is **absent** (dark). If no ERN is cutting it, the color is **present** (bright).

## Putting It Together: A Simple Example

Say you put these two plasmids into a cell:
1. **Csy4** (the enzyme)
2. **Csy4_rec_mNeonGreen** (green, but with a Csy4 recognition sequence)

What happens:
1. Cell makes Csy4 protein from plasmid 1
2. Cell transcribes plasmid 2 into mNeonGreen mRNA
3. Csy4 protein finds the mNeonGreen mRNA (it has the recognition sequence!)
4. Csy4 cuts and destroys the mNeonGreen mRNA
5. mNeonGreen protein never gets made
6. **Result: no green fluorescence** — the cell is dark in the green channel

Now compare: if you put in just **mNeonGreen** (no recognition sequence, from the Colors list) without any ERN, the cell happily makes mNeonGreen protein and **glows green**.

That's the fundamental building block. Everything else is just chaining these interactions together.

## Chains of Inhibition

The interesting circuits come from chaining ERNs together:

### Single Inhibition
```
Csy4 ──inhibits──► mNeonGreen
(via Csy4_rec_mNeonGreen)

Result: green is OFF
```

### Double Inhibition (the default circuit)
```
Csy4 ──inhibits──► CasE ──inhibits──► mNeonGreen
(via Csy4_rec_CasE)    (via CasE_rec_mNeonGreen)

Csy4 kills CasE → CasE can't kill mNeonGreen → green is ON
Two negatives make a positive.
```

### Triple Inhibition
```
CasE ──inhibits──► Csy4 ──inhibits──► PgU ──inhibits──► mNeonGreen

CasE kills Csy4 → Csy4 can't kill PgU → PgU kills mNeonGreen → green is OFF
Three negatives make a negative.
```

The pattern: **even** number of inhibitions = output ON, **odd** number = output OFF. Just like multiplying negative numbers.

## The Analog Part

This isn't purely ON/OFF though. The **amounts matter**. If you put in a lot of Csy4 (say 200 ng) and only a little Csy4_rec_CasE (say 50 ng), Csy4 overwhelmingly suppresses CasE. But if you reverse the amounts, there might be enough CasE mRNA being produced that Csy4 can't cut it all fast enough, and some CasE protein gets made.

This is why the circuit is "neuromorphic" — like real neurons, the output is a continuous value that depends on the relative strengths of the inputs, not a binary switch.

## What the OT-2 Robot Does

You can't easily pipette 2.4 microliters of liquid by hand (that's about 1/20th of a raindrop). The OT-2 robot does the precise liquid handling:

1. Mixes the right amount of each plasmid DNA into tubes
2. Adds the Lipofectamine transfection reagents
3. Gently pipettes the mixture onto the cells growing in a plate

See [Physical Protocol Walkthrough](../reference/physical-protocol-walkthrough.md) for the full step-by-step physical process.

## What You Get at the End

After 24-48 hours in the incubator, you look at the plate under a fluorescence microscope. Each well shows some combination of colored fluorescence depending on which plasmids were in that well and how the ERN logic played out. You compare the fluorescence intensities to what the biocompiler simulation predicted.

The circuit is successful if the observed fluorescence pattern matches the predicted one — meaning the ERNs are doing their job as designed and the analog computation is working inside living cells.
