# Genetic Circuit Visualization Tools Survey

A survey of graphical tools for designing and visualizing genetic circuits, with recommendations for building a custom visual builder for the neuromorphic project.

## Existing Open-Source Tools

### SBOLCanvas

- **Type**: Web-based drag-and-drop editor
- **URL**: https://sbolcanvas.org
- **Source**: https://github.com/SynBioDex/SBOLCanvas
- **Paper**: [ACS Synthetic Biology, 2021](https://pubs.acs.org/doi/10.1021/acssynbio.1c00096)
- **Stack**: Angular frontend + Java/Spring backend, Dockerized
- **Features**: Add DNA and non-DNA components, link via interactions (production, inhibition), organize into modules, export to SynBioHub or as images
- **Relevance**: Closest existing tool to what we need — a visual editor with SBOL export. However, the Angular/Java stack is heavyweight for our purposes.

### Synergetica

- **Type**: Desktop application (2025)
- **Source**: https://github.com/khokao/synergetica
- **Docs**: https://khokao.github.io/synergetica/
- **Features**: Node-based visual interface AND code-based interface, integrated simulation, DNA sequence generation
- **Relevance**: Modern and open-source, but desktop-only. Good reference for UI/UX patterns.

### Cello 2.0

- **Type**: Design automation tool
- **Source**: https://github.com/CIDARLAB/Cello-v2
- **Paper**: [Nature Protocols, 2021](https://www.nature.com/articles/s41596-021-00675-2)
- **Stack**: Java
- **Features**: Compiles high-level logic specifications (Verilog-like) into DNA sequences using a characterized parts library
- **Relevance**: Powerful backend for logic-to-DNA compilation. Not a visual editor, but the logic compilation concept is relevant to our ERN circuit design.

### iBioSim 3

- **Type**: Full CAD suite
- **Source**: https://github.com/MyersResearchGroup/iBioSim
- **Paper**: [ACS Synthetic Biology, 2019](https://pubs.acs.org/doi/10.1021/acssynbio.8b00078)
- **Stack**: Desktop Java application
- **Features**: Model editors, simulation, SBOL and SBML support, SynBioHub integration
- **Relevance**: Comprehensive but heavy. Good reference for simulation capabilities.

### SBOLDesigner 2

- **Type**: Desktop GUI for structural genetic design
- **URL**: https://sboldesigner.github.io/
- **Stack**: Java, Apache 2.0 license
- **Features**: Native SBOL 2.1 and SBOL Visual 1.0 support
- **Relevance**: Focused on structural design, not circuit-level logic visualization.

### DNAplotlib

- **Type**: Python library
- **Source**: https://github.com/VoigtLab/dnaplotlib
- **Paper**: [ACS Synthetic Biology, 2017](https://pubs.acs.org/doi/abs/10.1021/acssynbio.6b00252)
- **Features**: Programmable visualization of genetic constructs, publication-quality SVG/PDF output
- **Relevance**: Excellent for static rendering and figure generation, but not interactive.

### paraSBOLv

- **Type**: Python library
- **Source**: https://github.com/BiocomputeLab/paraSBOLv
- **Paper**: [Synthetic Biology (Oxford), 2021](https://academic.oup.com/synbio/article/6/1/ysab022/6347203)
- **Features**: Lightweight parametric SVG glyph rendering based on SBOL Visual spec
- **Relevance**: Good foundation for building custom visualization tools. MIT license.

### Pigeon

- **Type**: Web tool
- **Features**: Translates textual descriptions of synthetic biology designs into images
- **Relevance**: Simple and easy to learn, but older and limited in interactivity.

## JavaScript/Web Libraries

### visbol-js

- **Source**: https://github.com/VisBOL/visbol-js
- **npm**: `visbol`
- **License**: BSD-2-Clause
- **Features**: Renders SBOL Visual diagrams in the browser, supports interactions (inhibition, genetic production, stimulation, degradation)
- **Relevance**: The key JS library for SBOL rendering. Handles rendering but not editing.

### VisBOL2

- **Source**: https://github.com/VisBOL/VisBOL2
- **Features**: Updated version of VisBOL for improved web-based visualization

### sboljs / sboljs3

- **sboljs**: https://github.com/SynBioDex/sboljs (SBOL 2.3.0, BSD-2-Clause)
- **sboljs3**: https://github.com/sboltools/sbolgraph (TypeScript rewrite, SBOL3 support)
- **Features**: JavaScript/TypeScript implementation of the SBOL data model, reads/writes SBOL XML/RDF
- **Relevance**: Handles the data layer for any custom tool we build.

### SBOL Visual CSS

- **Source**: https://github.com/Edinburgh-Genome-Foundry/SBOL-Visual-CSS
- **Demo**: https://edinburgh-genome-foundry.github.io/SBOL-Visual-CSS/
- **Features**: Pure CSS library (20kb) for displaying SBOL Visual glyphs using simple HTML markup
- **Relevance**: Extremely lightweight, great for quick prototyping. Drop-in CSS glyphs work in any web page.

### SeqViz

- **Source**: https://github.com/Lattice-Automation/seqviz
- **npm**: `seqviz`
- **License**: MIT
- **Features**: React component for viewing DNA/RNA/protein sequences with annotations, enzyme cut sites, searching
- **Relevance**: Useful for sequence-level views alongside a circuit builder.

## Commercial / In-Development Tools

### Asimov

- **URL**: https://www.asimov.com/
- **Type**: Commercial cloud-based software
- **Features**: Design, simulate, and optimize genetic systems
- **Relevance**: Represents state of the art in commercial tooling. Not open source.

### Cambridge SynBioFund Project

- **URL**: https://www.engbio.cam.ac.uk/synbiofund/Interactive_software_project_folder/sw_genetic_circuit_design_full
- **Type**: Interactive web-based tool (in development)
- **Features**: Combines control theory with user-friendly design, hides mathematical complexity

## Gap Analysis

No single existing tool perfectly fits the need for a **lightweight, modern, web-based drag-and-drop circuit builder** — especially one tailored to our ERN-based neuromorphic circuits (Csy4, CasE, PgU inhibition networks).

| Need | Best Existing Option | Gap |
|------|---------------------|-----|
| Visual drag-and-drop editing | SBOLCanvas | Heavy Angular/Java stack |
| SBOL glyph rendering in browser | visbol-js, SBOL Visual CSS | Rendering only, no editing |
| SBOL data model in JS | sboljs3 | Data only, no UI |
| Simulation | iBioSim, Synergetica | Desktop-only |
| ERN-specific parts library | None | All tools are generic |
| Integration with NeuromorphicWizard CSV format | None | Custom requirement |

## Recommended Approach: Custom Visual Builder

### Proposed Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | Svelte | Already in the project environment, excellent reactivity, small bundles |
| Canvas/Diagram | Svelvet or React Flow | Purpose-built for node-based editors with drag-and-drop and edge connections |
| Glyph rendering | Custom SVG components based on SBOL Visual spec | Full control, lightweight |
| Quick prototyping | SBOL Visual CSS | 20kb drop-in for initial mockups |
| Data model | sboljs3 (TypeScript) | SBOL3 read/write if standards compliance is needed |
| Export | SVG/PNG + CSV (NeuromorphicWizard format) | Direct integration with existing pipeline |

### Proposed Features

**Core (MVP):**
1. Parts palette with ERN enzymes (Csy4, CasE, PgU) and reporters (mNeonGreen, mKO2, eBFP2, mMaroon1)
2. Drag parts onto a canvas
3. Wire inhibition connections between parts (matching `X_rec_Y` naming convention)
4. Visualize circuit logic (cascades, AND gates) with proper SBOL-style glyphs
5. Export circuit to CSV format compatible with NeuromorphicWizard

**Extended:**
6. Auto-calculate DNA budget against the 650ng constraint
7. Show predicted ON/OFF state for each node based on inhibition chain parity
8. Import existing circuit CSVs from `experiments/inputs/`
9. Export to SBOL3 XML for interoperability with other tools
10. Export diagram as SVG/PNG for documentation and presentations

### Architecture

```
CircuitBuilder (Svelte app)
├── PartsPanel          -- Sidebar with draggable ERN parts and reporters
├── Canvas              -- Svelvet/React Flow node-edge editor
│   ├── ERNNode         -- Custom node component for enzymes
│   ├── ReporterNode    -- Custom node component for fluorescent reporters
│   └── InhibitionEdge  -- Custom edge with flat-head arrow (repression)
├── PropertiesPanel     -- Selected node/edge properties
├── BudgetBar           -- DNA budget tracker (current/650ng)
├── ExportPanel         -- CSV, SVG, PNG export controls
└── lib/
    ├── parts.ts        -- Parts library (from HTGAA-part-names.csv)
    ├── circuit.ts      -- Circuit data model and validation
    ├── csv-export.ts   -- NeuromorphicWizard CSV format export
    └── svg-glyphs.ts   -- SBOL Visual glyph SVG definitions
```

### Integration with Existing Pipeline

The visual builder would sit upstream of the NeuromorphicWizard:

```
[Visual Circuit Builder]  →  CSV  →  [NeuromorphicWizard]  →  OT-2 Protocol
     Design phase              ↓         Build/Predict/Generate phases
                          experiments/
                          inputs/*.csv
```

## References

- SBOL Visual standard: https://sbolstandard.org/visual-about/
- SBOL Standard applications list: https://sbolstandard.org/applications/
- Nature Communications 2025: "Engineering wetware and software for the predictive design of compressed genetic circuits" https://www.nature.com/articles/s41467-025-64457-0
