# Circuit Design Template

## Input Format

The design template is a CSV with 5 columns:

| Column | Description | Notes |
|--------|-------------|-------|
| **Circuit name** | A name for your circuit | Same name for all rows in one circuit |
| **Transfection group** | Group label (e.g., X1, X2, Bias) | Plasmids in the same group are co-transfected |
| **Contents** | Plasmid name | Must match a name from the parts list |
| **Concentration (ng/uL)** | Stock concentration | Always 50 |
| **DNA wanted (ng)** | Amount of this plasmid | All rows must sum to <= 650 |

## Default Example

```csv
Circuit name,Transfection group,Contents,Concentration (ng/uL),DNA wanted (ng)
MyCircuit,X1,Csy4,50,150
MyCircuit,X1,mKO2,50,100
MyCircuit,X2,Csy4_rec_CasE,50,100
MyCircuit,X2,eBFP2,50,100
MyCircuit,Bias,CasE_rec_mNeonGreen,50,200
```

## How to Read This

Each row is one plasmid. Rows with the same **Transfection group** are mixed together into one tube.

- **Group X1**: Csy4 (150 ng) + mKO2 (100 ng) are co-transfected
- **Group X2**: Csy4_rec_CasE (100 ng) + eBFP2 (100 ng) are co-transfected
- **Group Bias**: CasE_rec_mNeonGreen (200 ng) alone

Total DNA: 150 + 100 + 100 + 100 + 200 = 650 ng (at the maximum)

## Design Tips

- The total DNA across all rows must not exceed **650 ng**
- Higher ng amounts mean more of that plasmid is delivered, resulting in higher expression
- The **ratio** between plasmids matters more than absolute amounts for circuit behavior
- Use transfection groups to control which plasmids are physically mixed together
- The "Bias" group typically contains constitutive components that set a baseline
