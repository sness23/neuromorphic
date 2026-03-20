#!/usr/bin/env python3
"""
Command-line interface for the NeuromorphicWizard pipeline.

Takes a circuit design CSV and generates:
  - experiment_config.csv  (full config with slot assignments)
  - opentrons_protocol.py  (OT-2 robot script)
  - plate_layouts.xlsx     (color-coded rack/plate layouts)
  - biocompiler.json5      (biocompiler simulation format)
"""

import argparse
import sys
import os

# Add NeuromorphicWizard to the path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WIZARD_DIR = os.path.join(PROJECT_ROOT, 'NeuromorphicWizard')
sys.path.insert(0, WIZARD_DIR)

import pandas as pd
from core.config import ALL_COLUMNS, REQUIRED_COLUMNS
from core.utils import normalize_dataframe
from core.validation import validate_experiment_design
from core.layout import generate_layout, generate_plate_layouts
from core.exporters import generate_opentrons_script, generate_excel_file
from core.json_converter import convert_to_json


def load_csv(path):
    """Load and normalize an input CSV."""
    df = pd.read_csv(path)

    # Check required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        print(f"Error: missing required columns: {', '.join(sorted(missing))}", file=sys.stderr)
        sys.exit(1)

    return normalize_dataframe(df)


def main():
    parser = argparse.ArgumentParser(
        description='Generate experiment files from a circuit design CSV.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  %(prog)s experiments/inputs/three-layer-cascade.csv
  %(prog)s experiments/inputs/and-gate.csv -o output/ --layout 96well
  %(prog)s experiments/inputs/three-layer-cascade.csv --template v3.8
""")

    parser.add_argument('input', help='Input CSV file (minimal 5-column format)')
    parser.add_argument('-o', '--output-dir', default='.',
                        help='Output directory (default: current directory)')
    parser.add_argument('--layout', choices=['24tube', '96well'], default='24tube',
                        help='Labware layout type (default: 24tube)')
    parser.add_argument('--template', choices=['v3.8', 'v3.9', '96-well'], default='v3.9',
                        help='OT-2 script template version (default: v3.9)')
    parser.add_argument('--name', default=None,
                        help='Base filename for outputs (default: input filename stem)')
    parser.add_argument('--no-validate', action='store_true',
                        help='Skip validation (not recommended)')

    args = parser.parse_args()

    # Load input
    df = load_csv(args.input)
    print(f"Loaded {len(df)} rows from {args.input}")

    # Validate
    if not args.no_validate:
        is_valid, error = validate_experiment_design(df, layout_key=args.layout)
        if not is_valid:
            print(f"Validation failed:\n{error}", file=sys.stderr)
            sys.exit(1)
        print("Validation passed")

    # Generate layout (slot assignments)
    config_df = generate_layout(df, layout_key=args.layout)
    print(f"Layout generated ({args.layout})")

    # Generate plate layouts
    plate_layouts = generate_plate_layouts(config_df, layout_key=args.layout)

    # Generate opentrons script
    template_map = {
        'v3.8': os.path.join(WIZARD_DIR, 'data', 'OT2_automated_transfection_v3.8.py'),
        'v3.9': os.path.join(WIZARD_DIR, 'data', 'OT2_automated_transfection_v3.9.py'),
        '96-well': os.path.join(WIZARD_DIR, 'data', 'OT2_automated_transfection_test96well_format.py'),
    }
    template_path = template_map[args.template]
    opentrons_script = generate_opentrons_script(config_df, template_path=template_path)

    # Generate biocompiler JSON
    biocompiler_json = convert_to_json(config_df)

    # Generate Excel
    excel_bytes = generate_excel_file(config_df, plate_layouts, layout_key=args.layout)

    # Write outputs
    os.makedirs(args.output_dir, exist_ok=True)
    base = args.name or os.path.splitext(os.path.basename(args.input))[0]

    csv_path = os.path.join(args.output_dir, f'{base}_config.csv')
    config_df.to_csv(csv_path, index=False)
    print(f"  {csv_path}")

    script_path = os.path.join(args.output_dir, f'{base}_protocol.py')
    with open(script_path, 'w') as f:
        f.write(opentrons_script)
    print(f"  {script_path}")

    xlsx_path = os.path.join(args.output_dir, f'{base}_layouts.xlsx')
    with open(xlsx_path, 'wb') as f:
        f.write(excel_bytes.read())
    print(f"  {xlsx_path}")

    json_path = os.path.join(args.output_dir, f'{base}_biocompiler.json5')
    with open(json_path, 'w') as f:
        f.write(biocompiler_json)
    print(f"  {json_path}")

    print("Done.")


if __name__ == '__main__':
    main()
