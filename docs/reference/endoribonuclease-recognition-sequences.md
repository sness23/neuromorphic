# Endoribonuclease Recognition Sequences

This document describes the three endoribonucleases (ERNs) used in the neuromorphic computing circuit, their RNA recognition sequences, cleavage mechanisms, and origins.

## Overview

The circuit uses three orthogonal CRISPR-associated endoribonucleases. Each recognizes a distinct RNA hairpin (direct repeat) embedded in the mRNA of target genes. When present, the ERN binds its cognate hairpin and cleaves the mRNA, destroying it and preventing protein production.

| ERN | Family | Organism | DR Length | Cleavage Product |
|-----|--------|----------|-----------|-----------------|
| **CasE** (Cas6e) | Cas6, Type I-E | *Escherichia coli* K12 | 29 nt | 8-nt 5' handle + 21-nt 3' hairpin |
| **Csy4** (Cas6f) | Cas6, Type I-F | *Pseudomonas aeruginosa* PA14 | 28 nt | 8-nt 5' handle + 20-nt 3' hairpin |
| **PgU** (PguCas13b) | Cas13b, Type VI-B | *Porphyromonas gulae* | 36 nt | Cleaved at DR hairpin |

## CasE (Cas6e) — *E. coli* Type I-E

### Recognition Sequence

The *E. coli* K12 CRISPR repeat (CRISPR-1 and CRISPR-2 share the same repeat):

```
DNA:  5'-CGGTTTATCCCCGCTGGCGCGGGGAACAC-3'  (29 nt)
RNA:  5'-CGGUUUAUCCCCGCUGGCGCGGGGAACAC-3'
```

### Structure

The repeat folds into a stem-loop hairpin. CasE recognizes this hairpin through interactions with both the stem structure and specific bases on the 5' and 3' sides of the stem-loop.

```
        U   C
       C     G
      C       C     ← Loop
       G --- C
       C --- G
       G --- C      ← Stem (A-form helix)
       G --- C
       C --- G
       |
  5'-CGG         AACAC-3'
      ↑               ↑
   5' flank        3' flank
```

### Cleavage

CasE cleaves **8 nucleotides upstream of the spacer** (at the 3' base of the hairpin), producing:
- A **5' handle** of 8 nt (`AUAAACCG` in RNA) that remains bound to Cascade
- A **3' handle** of 21 nt forming the hairpin, with CasE remaining bound

### Key References

- Brouns et al. (2008) "Small CRISPR RNAs guide antiviral defense in prokaryotes." *Science* 321:960-964.
- Jackson et al. (2014) "Crystal structure of the CRISPR RNA-guided surveillance complex from *E. coli*." *Science* 345:1473-1479. [PMC4188430](https://pmc.ncbi.nlm.nih.gov/articles/PMC4188430/)
- Hochstrasser et al. (2014) "CasA mediates Cas3-catalyzed target degradation during CRISPR RNA-guided interference." *PNAS* 111:6618-6623.
- Hainsworth, DiAndreth et al. (2020) "An endoribonuclease-based feedforward controller." *Nat Commun* 11:6135. [PMC33173034](https://pubmed.ncbi.nlm.nih.gov/33173034/)
- Touchon et al. (2011) "CRISPR distribution within the *E. coli* species." *J Bacteriol* 193:2460-2467. [PMC3133152](https://pmc.ncbi.nlm.nih.gov/articles/PMC3133152/)

---

## Csy4 (Cas6f) — *P. aeruginosa* Type I-F

### Recognition Sequence

The *Pseudomonas aeruginosa* PA14 CRISPR repeat:

```
DNA:  5'-GTTCACTGCCGTATAGGCAGCTAAGAAA-3'  (28 nt)
RNA:  5'-GUUCACUGCCGUAUAGGCAGCUAAGAAA-3'
```

A minimal 16-nt fragment (the stem-loop plus one downstream nucleotide, nt 5-20) is sufficient for Csy4-catalyzed cleavage.

### Structure

The repeat forms a characteristic stem-loop with a 5-bp stem and a GUAUA pentaloop:

```
       G   A
      U     U     ← GUAUA pentaloop
       A---U        (with sheared G-A pair
       G===C         and extruded U14)
       C===G
       C===G      ← 5-bp A-form stem
       G===C
       U---A
       |
  5'-GU         GCUAAGAAA-3'
      ↑  C6---G20  ↑
   5' flank  (critical   3' flank
              base pair)
```

The terminal base pair **C6-G20** is critical for recognition. Csy4 residues Arg102 and Gln104 make sequence-specific hydrogen bonds in the major groove to G20 and A19.

### Cleavage

Csy4 cleaves at the **3' base of the stem-loop** (after G20), producing:
- A **5' handle** of 8 nt
- A **3' hairpin** of 20 nt, with Csy4 remaining tightly bound (Kd ~ 50 pM)

The catalytic dyad consists of **Ser148** and **His29** (unusual — most RNases use His-acid pairs). Cleavage generates a 2',3'-cyclic phosphate on the upstream product.

### Key References

- Haurwitz et al. (2010) "Sequence- and structure-specific RNA processing by a CRISPR endonuclease." *Science* 329:1355-1358. [PMC3133607](https://pmc.ncbi.nlm.nih.gov/articles/PMC3133607/)
- Sternberg et al. (2012) "Mechanism of substrate selection by a highly specific CRISPR endoribonuclease." *RNA* 18:661-672. [PMC3312554](https://pmc.ncbi.nlm.nih.gov/articles/PMC3312554/)
- Haurwitz et al. (2012) "Csy4 relies on an unusual catalytic dyad to position and cleave CRISPR RNA." *EMBO J* 31:2824-2832. [PMC3380207](https://pmc.ncbi.nlm.nih.gov/articles/PMC3380207/)
- Nissim et al. (2014) "Multiplexed and programmable regulation of gene networks with an integrated RNA and CRISPR/Cas toolkit in human cells." *Mol Cell* 54:698-710.
- Lee et al. (2015) "Controlling mRNA stability and translation with the CRISPR endoribonuclease Csy4." *RNA* 21:1921-1930. [PMC4604432](https://pmc.ncbi.nlm.nih.gov/articles/PMC4604432/)

---

## PgU (PguCas13b) — *P. gulae* Type VI-B

### Recognition Sequence

PguCas13b recognizes a **36-nt direct repeat (DR)** from the *Porphyromonas gulae* CRISPR array. Unlike CasE and Csy4 (which are Cas6-family enzymes), PgU belongs to the Cas13b family (Type VI-B). In the PERSIST/neuromorphic circuit context, PgU is used in a guide-RNA-independent mode: the DR hairpin is embedded directly in the target mRNA's UTR, and PgU recognizes and cleaves it.

The 36-nt DR has the following conserved features:
- 3-6 bp stem formed by complementary 5' and 3' ends
- 9-14 nt loop containing a poly-U stretch
- Located at the **3' end** of the crRNA (unlike Cas13a/c/d which use 5' DRs)

```
              U
           U     U
          U       U    ← poly-U loop
           A --- U
           ...       ← variable stem
           G --- C
           |
  5'- GUUG         CAAC -3'
       ↑               ↑
    conserved       conserved
    5' end          3' end
```

**Note:** The exact 36-nt sequence is deposited in Addgene plasmid [pC0042](https://www.addgene.org/103853/) (PguCas13b crRNA backbone, Zhang lab) but is not published inline in the literature. Consult the plasmid sequence file or the supplementary data of Cox et al. (2017) for the exact nucleotides.

### Cleavage

PguCas13b has two distinct nuclease activities:
1. **Pre-crRNA processing** — cleaves at the DR hairpin (used in the neuromorphic circuit). The processing site is in the Lid domain; mutation K393A specifically abolishes this activity.
2. **HEPN-domain RNase** — target RNA cleavage guided by the spacer (not used in this circuit context).

In the PERSIST architecture, only the pre-crRNA processing activity matters: PgU finds its DR hairpin in the mRNA, cleaves it, and destabilizes the transcript.

### Key References

- Smargon et al. (2017) "Cas13b is a Type VI-B CRISPR-associated RNA-guided RNase." *Mol Cell* 65:618-630. [PMC5432119](https://pmc.ncbi.nlm.nih.gov/articles/PMC5432119/)
- Cox et al. (2017) "RNA editing with CRISPR-Cas13." *Science* 358:1019-1027. [PMID 29070703](https://pubmed.ncbi.nlm.nih.gov/29070703/)
- Slaymaker et al. (2019) "High-resolution structure of Cas13b and biochemical characterization of RNA targeting and cleavage." *Cell Reports* 26:3741-3751. [PMC6659120](https://pmc.ncbi.nlm.nih.gov/articles/PMC6659120/)
- DiAndreth, Wauford et al. (2022) "PERSIST platform provides programmable RNA regulation using CRISPR endoRNases." *Nat Commun* 13:2582. [PMID 35562172](https://pubmed.ncbi.nlm.nih.gov/35562172/)

---

## Comparison Table

| Property | CasE | Csy4 | PgU |
|----------|------|------|-----|
| **Full name** | Cas6e | Cas6f | PguCas13b |
| **CRISPR type** | Type I-E | Type I-F | Type VI-B |
| **Protein family** | Cas6 (RAMP) | Cas6 (RAMP) | Cas13b (HEPN) |
| **Source organism** | *E. coli* K12 | *P. aeruginosa* PA14 | *P. gulae* |
| **DR length** | 29 nt | 28 nt | 36 nt |
| **DR structure** | Stem-loop hairpin | 5-bp stem + GUAUA pentaloop | Stem-loop with poly-U loop |
| **Cleavage position** | 3' base of hairpin (8 nt from spacer) | 3' base of stem (after G20) | At DR hairpin (Lid domain) |
| **Stays bound after cut?** | Yes (part of Cascade) | Yes (Kd ~ 50 pM) | Processing releases fragment |
| **Crystal structure?** | Yes (PDB 4TVX, others) | Yes (PDB 2XLK, 4AL5-7) | Yes (PDB 6DTD, PbuCas13b) |

## Crystal Structures (PDB)

Experimentally determined structures are available for all three ERNs (or close homologs):

### Csy4 Structures

| PDB | Resolution | Contents | Citation |
|-----|-----------|----------|----------|
| [**2XLK**](https://www.rcsb.org/structure/2XLK) | 1.80 A | Csy4 bound to 16-nt crRNA hairpin (orthorhombic) | Haurwitz et al. (2010) *Science* 329:1355-1358 |
| [2XLI](https://www.rcsb.org/structure/2XLI) | — | Csy4-crRNA complex (monoclinic form) | Haurwitz et al. (2010) *Science* 329:1355 |
| [2XLJ](https://www.rcsb.org/structure/2XLJ) | — | Csy4-crRNA complex (hexagonal form) | Haurwitz et al. (2010) *Science* 329:1355 |
| [**4AL5**](https://www.rcsb.org/structure/4AL5) | 2.00 A | Csy4 bound to 20-nt crRNA product | Haurwitz et al. (2012) *EMBO J* 31:2824-2832 |
| [4AL6](https://www.rcsb.org/structure/4AL6) | — | S148A mutant Csy4-crRNA complex | Haurwitz et al. (2012) *EMBO J* 31:2824 |
| [4AL7](https://www.rcsb.org/structure/4AL7) | — | Csy4 bound to minimal crRNA | Haurwitz et al. (2012) *EMBO J* 31:2824 |

**Best structure to cite:** [2XLK](https://www.rcsb.org/structure/2XLK) — the landmark 1.8 A Csy4-crRNA complex from the Doudna lab showing the sequence-specific major groove recognition mechanism.

### CasE Structures

| PDB | Resolution | Contents | Citation |
|-----|-----------|----------|----------|
| [**4TVX**](https://www.rcsb.org/structure/4TVX) | 3.24 A | Full *E. coli* Cascade complex (CasA-E + 61-nt crRNA) | Jackson et al. (2014) *Science* 345:1473-1479 |
| [4U7U](https://www.rcsb.org/structure/4U7U) | 3.05 A | *E. coli* Cascade complex (alternate crystal form) | Zhao et al. (2014) *Nature* 515:147-150 |
| [**4DZD**](https://www.rcsb.org/structure/4DZD) | 2.00 A | CasE protein alone (*E. coli* K12), no RNA | Wei et al. (unpublished) |
| [4QYZ](https://www.rcsb.org/structure/4QYZ) | — | Cascade bound to ssDNA target | Mulepati et al. (2014) *Science* 345:1479-1484 |

**Best structure to cite:** [4TVX](https://www.rcsb.org/structure/4TVX) — the full Cascade complex showing CasE bound to the crRNA 3' hairpin in biological context. For the isolated CasE protein, [4DZD](https://www.rcsb.org/structure/4DZD) at 2.0 A.

### PgU (Cas13b) Structures

No crystal structure of PguCas13b (*P. gulae*) itself has been deposited. The closest available structure is the homolog PbuCas13b (*Prevotella buccae*):

| PDB | Resolution | Contents | Citation |
|-----|-----------|----------|----------|
| [**6DTD**](https://www.rcsb.org/structure/6DTD) | 1.65 A | PbuCas13b bound to crRNA (36-nt DR + 5-nt spacer) | Slaymaker et al. (2019) *Cell Reports* 26:3741-3751 |

**Best structure to cite:** [6DTD](https://www.rcsb.org/structure/6DTD) — high-resolution PbuCas13b-crRNA complex from the Zhang lab. PguCas13b shares domain architecture with PbuCas13b (HEPN1, HEPN2, Helical-1, Helical-2, and Lid domains). The Lid domain caps the 3' DR hairpin and contains the pre-crRNA processing active site (K393).

### Quick-Reference Summary

| ERN | Recommended PDB | Resolution | Paper |
|-----|----------------|-----------|-------|
| **Csy4** | [2XLK](https://www.rcsb.org/structure/2XLK) | 1.80 A | Haurwitz et al. (2010) *Science* 329:1355 |
| **CasE** | [4TVX](https://www.rcsb.org/structure/4TVX) | 3.24 A | Jackson et al. (2014) *Science* 345:1473 |
| **PgU** (homolog) | [6DTD](https://www.rcsb.org/structure/6DTD) | 1.65 A | Slaymaker et al. (2019) *Cell Rep* 26:3741 |

---

## Orthogonality

The three ERNs are fully orthogonal — each only recognizes its own cognate DR hairpin:

- CasE does **not** cut Csy4 or PgU recognition sequences
- Csy4 does **not** cut CasE or PgU recognition sequences
- PgU does **not** cut CasE or Csy4 recognition sequences

This orthogonality is what enables the construction of multi-layer inhibitory circuits, where each ERN acts as an independent "neuron" that can be wired to suppress specific targets.

## How Recognition Sequences Are Used in the Circuit

In the neuromorphic circuit, DR hairpins are engineered into the **5' UTR or coding region** of target mRNAs on plasmids:

| Part Name | Encoded Protein | DR(s) in mRNA | Inhibited By |
|-----------|----------------|---------------|-------------|
| `CasE_rec_mNeonGreen` | mNeonGreen | CasE DR | CasE |
| `Csy4_rec_mNeonGreen` | mNeonGreen | Csy4 DR | Csy4 |
| `PgU_rec_mNeonGreen` | mNeonGreen | PgU DR | PgU |
| `PgU_rec_Csy4` | Csy4 | PgU DR | PgU |
| `PgU_rec_CasE` | CasE | PgU DR | PgU |
| `Csy4_rec_CasE` | CasE | Csy4 DR | Csy4 |
| `CasE_rec_Csy4` | Csy4 | CasE DR | CasE |
| `CasE_rec_Csy4_rec_mKO2` | mKO2 | CasE DR + Csy4 DR | CasE or Csy4 |

The naming convention `X_rec_Y` means: "X's recognition sequence (DR) is on Y's mRNA, so X inhibits Y."

## Further Reading

- [PERSIST Platform (DiAndreth et al. 2022)](https://www.nature.com/articles/s41467-022-30172-3) — Nine orthogonal ERNs for programmable RNA regulation
- [Synthetic Neuromorphic Computing (Rizik et al. 2022)](https://www.nature.com/articles/s41467-022-33288-8) — Neural network computation in living cells
- [Complete Parts Reference](complete-parts-reference.md) — All available parts in this circuit library
- [Biology Concepts](../background/biology-concepts.md) — How ERNs create inhibitory wiring
