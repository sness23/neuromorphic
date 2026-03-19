# Glossary

## Biology Terms

**Amino acid**: The building blocks of proteins. There are 20 standard amino acids. A protein is a chain of amino acids folded into a specific shape.

**Cell**: The basic unit of life. A membrane-bound compartment containing DNA and molecular machinery. Human cells are eukaryotic (they have a nucleus containing DNA).

**Cell line**: Cells that have been adapted to grow indefinitely in the lab. They are "immortalized" — they don't stop dividing like normal cells do. HEK293 is an example.

**Cell monolayer**: A single layer of cells attached to the bottom of a well or dish. Cells grow flat and spread out, covering the surface. The OT-2 protocol is careful not to disturb this layer when adding transfection mix.

**Constitutive expression**: A gene that is always ON — it produces its protein continuously without any regulation. In this lab, the unregulated fluorescent reporters (mKO2, eBFP2, mMaroon1, mNeonGreen from the Colors category) are constitutively expressed.

**DNA (Deoxyribonucleic Acid)**: The molecule that stores genetic information. A long chain of nucleotides (A, T, G, C) that encodes instructions for making proteins.

**Endoribonuclease (ERN)**: An enzyme that cuts RNA molecules internally (not from the ends). In this lab, CasE, Csy4, and PgU are endoribonucleases that cut RNA at specific recognition sequences.

**Expression**: The process of a gene being read and its protein being produced. "High expression" means a lot of protein is made. "Low expression" means little protein is made. Expression level depends on how much plasmid DNA is in the cell and whether the mRNA is being cut.

**Fluorescence**: The emission of light by a substance that has absorbed light of a different wavelength. Fluorescent proteins absorb one color of light (excitation) and emit another (emission). This is how we see the circuit output.

**Fluorescence microscope**: A microscope that shines specific wavelengths of light on a sample and captures the emitted fluorescence through filters. Different filters reveal different fluorescent proteins (blue, green, orange, maroon).

**Gene**: A segment of DNA that encodes a protein. Each plasmid in this lab carries one gene.

**HEK293 cells**: Human Embryonic Kidney 293 cells. An immortalized cell line derived in 1973. Widely used in biology because they are easy to grow and transfect.

**Incubator**: A device that maintains cells at 37°C with 5% CO2 and controlled humidity, mimicking conditions inside the human body.

**Inhibition**: The suppression of a biological process. In this lab, ERNs inhibit protein production by cutting the mRNA before it can be translated into protein.

**Lipid nanoparticle**: A tiny sphere made of lipid (fat) molecules, typically 50-200 nanometers in diameter. Used to deliver DNA into cells by fusing with the cell membrane.

**Lipofectamine 3000**: A commercial transfection reagent (from Thermo Fisher). It consists of lipid molecules that spontaneously form nanoparticles around DNA. The "3000" indicates the product generation. Components: L3000 (lipofectamine), P3000 (enhancer), Opti-MEM (dilution medium).

**mRNA (Messenger RNA)**: A temporary copy of a gene's DNA sequence, made by transcription. mRNA carries the instructions from DNA to the ribosome, where the protein is built. ERNs destroy mRNA to prevent protein production.

**Opti-MEM**: A reduced serum cell culture medium (from Gibco/Thermo Fisher). Used as a dilution medium for the Lipofectamine transfection reagent. "Reduced serum" means it has less protein than standard medium, which improves transfection efficiency.

**Plasmid**: A small, circular piece of DNA that exists separately from the cell's own chromosomes. Plasmids can be designed on a computer, manufactured by a DNA synthesis company, and introduced into cells. Each plasmid in this lab encodes one protein.

**Protein**: A molecular machine made of amino acids. Proteins do all the work in a cell — they provide structure, catalyze reactions, send signals, and more. In this lab, the ERN enzymes and fluorescent reporters are all proteins.

**Recognition sequence**: A specific short sequence of RNA nucleotides that an ERN identifies and binds to before cutting. Each ERN recognizes a different sequence. The recognition sequence is engineered into the mRNA of target genes.

**Transcription**: The process of copying a DNA gene into an mRNA molecule. Performed by RNA polymerase enzyme. This is the first step in gene expression (DNA → mRNA).

**Transfection**: The process of introducing foreign DNA (plasmids) into cells. In this lab, Lipofectamine 3000 is used to wrap DNA in lipid nanoparticles that fuse with cell membranes.

**Translation**: The process of reading an mRNA molecule and building the corresponding protein. Performed by ribosomes. This is the second step in gene expression (mRNA → protein).

## Lab Equipment Terms

**24-tube rack**: A holder for 24 Eppendorf tubes, arranged in a 4×6 grid (rows A-D, columns 1-6). The OT-2 uses this to hold DNA tubes, mixing tubes, and reagent tubes.

**24-well plate**: A plastic plate with 24 wells (4×6 grid), each well holding up to 3.4 mL. Cells grow in these wells. The Corning 24-well plate is used in this lab.

**96-well plate**: A plastic plate with 96 wells (8×12 grid), each well holding less volume than a 24-well plate. Some protocols use these for higher throughput.

**Eppendorf tube**: A small (1.5 mL) plastic tube with a snap cap. Standard container for small volumes of liquid in molecular biology.

**OT-2**: An Opentrons liquid handling robot. It has two pipette mounts (left and right) and a 12-slot deck for labware. It automates precise pipetting that would be difficult to do by hand.

**P20 pipette**: A pipette that can accurately measure 1-20 microliters. Mounted on the left side of the OT-2. Used for small volume transfers (most DNA transfers in this lab).

**P300 pipette**: A pipette that can accurately measure 20-300 microliters. Mounted on the right side of the OT-2. Used for larger volume transfers (Opti-MEM, final transfection mixes).

**Tip rack**: A tray of disposable pipette tips. The OT-2 picks up a fresh tip for each transfer to prevent cross-contamination. 20 uL tips for the P20, 300 uL tips for the P300.

## Circuit Design Terms

**Analog computation**: Computation where values can be any number in a continuous range, not just 0 or 1. In neuromorphic circuits, protein expression levels are continuous values determined by plasmid ratios and inhibition strengths.

**AND gate**: A logic gate whose output is ON only when ALL inputs meet a specific condition. In this lab, `CasE_rec_Csy4_rec_mKO2` is an AND gate — orange is ON only when both CasE AND Csy4 are absent.

**Cascade**: A chain of sequential inhibitions where each component inhibits the next. A→B→C→D. The output depends on the number of steps (even = ON, odd = OFF).

**Co-transfection**: Delivering multiple plasmids into the same cell simultaneously. Plasmids in the same transfection group are co-transfected (mixed in the same tube before delivery).

**IANN (Intracellular Artificial Neural Network)**: A network of interacting proteins inside a living cell that performs computation. Each "neuron" is a plasmid-encoded component, and the connections are ERN-mediated inhibitions.

**Neuromorphic**: "Brain-shaped" — mimicking the structure or function of neural networks. Neuromorphic circuits use analog, inhibitory interactions rather than digital logic gates.

**Sequestron**: The building block of neuromorphic genetic circuits. A component that can sequester (capture and neutralize) another component's mRNA. Named by analogy to the neuron.

**Transfection group**: A set of plasmids that are mixed together in one tube before being delivered to cells. All plasmids in the same group enter the cell in the same lipid nanoparticle. Different groups enter in separate nanoparticles but end up in the same cell.

**Universal function approximator**: A system that can approximate any mathematical function to arbitrary precision, given enough components. IANNs are universal function approximators — with enough intracellular neurons, they can implement any input/output mapping.

## Units

**ng (nanogram)**: One billionth of a gram (10⁻⁹ g). DNA amounts in this lab are measured in nanograms. The total DNA budget per circuit is 650 ng.

**ng/uL (nanograms per microliter)**: Concentration unit. All DNA stocks in this lab are at 50 ng/uL. To calculate the volume needed: volume = amount / concentration.

**uL (microliter)**: One millionth of a liter (10⁻⁶ L). About 1/50th of a drop of water. The OT-2 robot pipettes volumes as small as 1 uL.

**mL (milliliter)**: One thousandth of a liter (10⁻³ L). Well volumes in the 24-well plate are measured in mL.

## Software Terms

**Biocompiler**: A simulation tool that predicts circuit behavior based on plasmid ratios and the known inhibition relationships. Takes a JSON5 file as input.

**JSON5**: A more human-readable variant of JSON that allows comments, trailing commas, and unquoted keys. The biocompiler format uses JSON5.

**NeuromorphicWizard**: The Python web application used to design circuits, validate inputs, simulate OT-2 protocols, and export experiment files. Built with the NiceGUI framework.

**NiceGUI**: A Python framework for building web-based user interfaces. The NeuromorphicWizard uses it to create the Build/Predict/Generate/Analyze tabs.

**Opentrons API**: The Python library used to program the OT-2 robot. The generated protocol script uses the Opentrons API (version 2.19) to control pipettes, labware, and liquid transfers.

**Opentrons Simulate**: A command-line tool that simulates an OT-2 protocol without needing a physical robot. Used to verify that the protocol runs without errors before uploading to the actual robot.
