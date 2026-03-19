# HTGAA 2026 - Genetic Circuits II: Intracellular Artificial Neural Networks

## Course Context

This is Week 7 of **How to Grow (Almost) Anything 2026** (HTGAA), a course on designing and building genetic circuits using living cells.

Lab page: https://2026a.htgaa.org/2026a/course-pages/weeks/week-07/lab/index.html

## Overview

In this two-day lab, you design and build an **Intracellular Artificial Neural Network (IANN)** using:

- A library of plasmids from the **Ron Weiss Lab** at MIT
- **HEK293 cells** (human embryonic kidney cells) as the host
- An **OT-2 liquid handling robot** to automate the transfection protocol

IANNs differ from traditional synthetic genetic circuits because they perform **analog computations** rather than digital ones. Given enough intracellular artificial neurons, an IANN can approximate any input/output function (universal function approximation).

## Lab Schedule

**Day 1 (Dry Lab):** Design a neuromorphic circuit in groups of 3 using the NeuromorphicWizard tool. Fill out a Google Sheet template specifying which plasmids to use and how much DNA of each. Upload by 4pm ET on Friday.

**Day 2 (Wet Lab):** Observe the OT-2 robot building and transfecting your circuit into HEK293 cells at the Weiss Lab (NE-47, MIT campus).

## Key Constraints

- Concentration column is always **50 ng/uL**
- Total DNA per circuit must not exceed **650 ng**
- Use plasmid names from the official part names list
- MIT/Harvard groups: 1 circuit per group
- Global nodes: up to 2 submissions per node

## Tools

- **NeuromorphicWizard**: Python/NiceGUI application for designing circuits, simulating behavior, and generating OT-2 protocols
- **OT-2 Robot**: Opentrons liquid handling robot that executes the transfection protocol
- **Lipofectamine 3000**: Reagent used to transfect plasmid DNA into HEK293 cells
