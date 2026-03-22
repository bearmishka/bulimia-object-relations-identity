# Object Relations and Identity in Bulimia Nervosa (Reproducibility Materials)

This repository contains reproducibility materials for two preprints:

1. **Profatilova, E.S. (2026).** Object Relations and Identity Features in Women with Bulimia Nervosa: An Exploratory Clinical Pilot Study. PsyArXiv preprint.

2. **Profatilova, E.S. (2026).** Psychometric Profiles of Object Relations and Identity in Women with Bulimia Nervosa: A Clinical Pilot Study. PsyArXiv preprint.

## Contents

- `main.tex` — manuscript source (LaTeX)
- `main.pdf` — compiled manuscript
- `stats_audit.py` — statistical verification script: recalculates p-values for reported Pearson correlations, regression coefficients, and model-level F-statistics
- `reliability_analysis.py` — internal consistency script: computes Cronbach's alpha with bootstrapped 95% CI for all BORI and EIS-III domains (n=28)

## What `stats_audit.py` checks

- Two-tailed p-values for selected Pearson correlations
- Two-tailed p-values for regression coefficients from reported t-statistics
- Model-level F and p-values from reported R² values

## What `reliability_analysis.py` computes

- Cronbach's alpha for each BORI domain (Alienation, Insecure Attachment, Egocentricity, Social Incompetence)
- Cronbach's alpha for each EIS-III domain (Confidence, Sexual Identity, Body/Appearance)
- Bootstrapped 95% CI (2000 iterations) for each estimate

**Note:** Raw item-level response files are not included due to participant confidentiality. The script is provided for methodological transparency.

## Requirements

- Python 3.9+
- `scipy`, `pandas`, `numpy`, `openpyxl`

## Run
```bash
python stats_audit.py
python reliability_analysis.py
```

## Zenodo

Current version (1.1.0): `https://doi.org/10.5281/zenodo.19159728`

Previous version (v1.0.0): `https://doi.org/10.5281/zenodo.18986931`

## License

Code in this repository is released under the MIT License (see `LICENSE`).
