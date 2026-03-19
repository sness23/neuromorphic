# OT-2 Protocol

## What the Robot Does

The OT-2 liquid handling robot automates the three-step transfection protocol:

1. **Mix DNA** -- pipette the right amount of each plasmid into mixing tubes (one tube per transfection group)
2. **Prepare Lipofectamine master mix** -- combine Opti-MEM, P3000, and L3000 in separate tubes
3. **Transfect cells** -- combine DNA mixtures with Lipofectamine mixtures, then deliver to HEK293 cells in the 96-well plate

## Protocol Parameters

```python
OM = 0.05      # uL of Opti-MEM per ng of DNA
P3K = 0.0022   # uL of P3000 per ng of DNA
L3K = 0.0022   # uL of L3000 per ng of DNA
Excess = 1.2   # 20% excess to account for pipetting error
```

## Slot Assignments

The Wizard assigns physical positions on the OT-2 deck. The notation `A1.1` means well A1 on rack in slot 1.

For the default circuit:

| Plasmid | DNA Source | DNA Dest | L3K/OM Dest | Plate Dest |
|---------|-----------|----------|-------------|------------|
| Csy4 | A1.1 | A6.1 | B3.1 | A1.1 |
| mKO2 | A2.1 | A6.1 | B3.1 | A1.1 |
| Csy4_rec_CasE | A3.1 | B1.1 | B4.1 | A1.1 |
| eBFP2 | A4.1 | B1.1 | B4.1 | A1.1 |
| CasE_rec_mNeonGreen | A5.1 | B2.1 | B5.1 | A1.1 |

Notice:
- Plasmids in the same transfection group share the same **DNA destination** (mixing tube)
- Each group has its own **L3K/OM destination** for the Lipofectamine mix
- All groups go to the same **plate destination** well (the same cell population receives all groups)

## Volume Calculations

For a plasmid with X ng of DNA wanted at 50 ng/uL concentration:

- **DNA volume**: X / 50 uL
- **Opti-MEM volume**: X * 0.05 * 1.2 uL
- **P3000 volume**: X * 0.0022 * 1.2 uL
- **L3000 volume**: X * 0.0022 * 1.2 uL

Example for Csy4 (150 ng):
- DNA: 150 / 50 = 3.0 uL
- Opti-MEM: 150 * 0.05 * 1.2 = 9.0 uL
- P3000: 150 * 0.0022 * 1.2 = 0.396 uL
- L3000: 150 * 0.0022 * 1.2 = 0.396 uL

## Running the Protocol

The generated `opentrons_protocol.py` is uploaded directly to the OT-2 robot. The CSV data is embedded in the script as a string, so the robot doesn't need separate input files.
