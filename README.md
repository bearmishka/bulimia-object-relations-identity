# Object Relations and Identity in Bulimia Nervosa (Reproducibility Materials)

This repository contains reproducibility materials for the preprint:

**Object Relations and Identity Features in Women with Bulimia Nervosa: An Exploratory Clinical Pilot Study** (March 2026).

## Contents

- `main.tex` — manuscript source (LaTeX)
- `main.pdf` — compiled manuscript
- `stats_audit.py` — statistical verification script used to audit reported inferential results

## What `stats_audit.py` checks

The script recalculates and prints:

- two-tailed p-values for selected Pearson correlations;
- two-tailed p-values for regression coefficients from reported t-statistics;
- model-level F and p-values from reported R² values.

## Requirements

- Python 3.9+
- `scipy`

## Run

```bash
python stats_audit.py
```

## Citation

If you use this code, please cite the software record (Zenodo DOI) and the related preprint.

Zenodo DOI (v1.0.0):

`https://doi.org/10.5281/zenodo.18986931`

## License

Code in this repository is released under the MIT License (see `LICENSE`).
