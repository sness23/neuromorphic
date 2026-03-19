# NeuromorphicWizard Tool

## What It Is

NeuromorphicWizard is a Python web application (built with NiceGUI) for designing neuromorphic genetic circuits and generating OT-2 liquid handling robot protocols.

Repository: `NeuromorphicWizard/` (has its own git repo)

## Running It

```bash
conda create -n neuro_wiz python==3.10
conda activate neuro_wiz
pip install -r requirements.txt
python3 main.py
```

Opens a web interface at http://localhost:8080

## Application Tabs

### Build
Upload your circuit design CSV. The tool validates your input, checks part names, and ensures DNA totals are within limits.

### Predict
Simulates your circuit's behavior using the biocompiler format. Shows predicted expression levels of each component based on plasmid ratios and the inhibition network.

### Generate
Generates the OT-2 protocol script and plate layouts. Assigns physical positions:
- **DNA source slots** -- where each plasmid tube sits on the OT-2 rack
- **DNA destination slots** -- mixing tubes (one per transfection group)
- **L3K/OM MM destination** -- Lipofectamine/Opti-MEM master mix tubes
- **Plate destination** -- target well in the 96-well plate

### Analyze
Tools for analyzing experimental results after the wet lab.

## Output Files

When you export, the Wizard generates a zip containing:

| File | Description |
|------|-------------|
| `experiment_config.csv` | Full config with source/destination slot assignments |
| `opentrons_protocol.py` | OT-2 Python script for the robot |
| `plate_layouts.xlsx` | Visual plate layout diagram |
| `biocompiler_format.json5` | Circuit in biocompiler format with plasmid ratios |

## Architecture

```
NeuromorphicWizard/
  main.py                  # Entry point, creates NiceGUI app on port 8080
  core/
    config.py              # Configuration constants
    state.py               # AppState and TemplateState classes
    validation.py          # Input validation rules
    layout.py              # Plate/rack layout assignment logic
    utils.py               # Utility functions
    script_utils.py        # OT-2 script generation helpers
    json_converter.py      # CSV to biocompiler JSON5 conversion
    exporters.py           # Zip file export
  ui/
    tabs/                  # Build, Predict, Generate, Analyze tab UIs
    components/            # Reusable UI components (upload, table, grid, etc.)
  data/
    OT2_automated_transfection_v3.9.py   # OT-2 protocol template
  static/
    css/styles.css
    js/file_operations.js
  tests/                   # Unit, integration, regression tests
```
