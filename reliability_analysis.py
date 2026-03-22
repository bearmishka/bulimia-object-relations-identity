"""
reliability_analysis.py
=======================
Sample-specific internal consistency estimates (Cronbach's alpha with
bootstrapped 95% CI) for the Bell Object Relations Inventory (BORI) and
Erwin Identity Scale (EIS-III) as used in:

    Profatilova, E.S. (2026). Object Relations and Identity Features in
    Women with Bulimia Nervosa: An Exploratory Clinical Pilot Study.
    PsyArXiv preprint.

    Profatilova, E.S. (2026). Psychometric Profiles of Object Relations
    and Identity in Women with Bulimia Nervosa: A Clinical Pilot Study.
    PsyArXiv preprint.

Requirements: pandas, numpy, openpyxl
Usage: python reliability_analysis.py

Input files expected in the same directory:
    Bell_Object_Relations_Testing_Inventory___Ответы_.xlsx
    EIS_-_III___Ответы_.xlsx

Note: Raw item-level response files are not publicly posted due to
participant confidentiality. This script is provided for methodological
transparency. Researchers with access to the source data can reproduce
the reported alpha estimates by running this script.
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Domain key definitions
# ---------------------------------------------------------------------------

# BORI (Bell, 1995): item numbers (1-indexed) per domain
BORI_DOMAINS = {
    "Alienation":           [3, 4, 13, 14, 19, 20, 22, 26, 27, 29, 35, 40, 41],
    "Insecure Attachment":  [5, 6, 9, 12, 16, 17, 23, 24, 28, 33, 34, 36, 39],
    "Egocentricity":        [10, 11, 31, 44, 45],
    "Social Incompetence":  [2, 32, 38, 43],
}

# EIS-III (Erwin): item numbers (1-indexed) per domain
EIS_DOMAINS = {
    "Confidence":       [1, 4, 8, 12, 13, 17, 21, 24, 25, 26, 27, 29, 33,
                         35, 37, 41, 42, 51, 52, 54, 55, 56, 57, 58, 59],
    "Sexual Identity":  [3, 6, 11, 15, 18, 19, 23, 28, 31, 43, 44, 45,
                         48, 50, 53],
    "Body/Appearance":  [2, 5, 7, 9, 10, 14, 16, 20, 22, 30, 32, 34, 36,
                         38, 39, 40, 46, 47, 49],
}

# Response encodings
BORI_MAP = {"Верно": 1, "Неверно": 0}
EIS_MAP = {
    "Полностью про меня":         5,
    "Скорее про меня":            4,
    "Не уверен(а) или нейтрально": 3,
    "Скорее не про меня":         2,
    "Совсем не про меня":         1,
}

N_PARTICIPANTS = 28
N_BOOTSTRAP    = 2000
RANDOM_SEED    = 42


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def cronbach_alpha(df: pd.DataFrame) -> float:
    """Compute Cronbach's alpha for a DataFrame of item scores."""
    df = df.dropna()
    k = df.shape[1]
    item_vars  = df.var(axis=0, ddof=1)
    total_var  = df.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars.sum() / total_var)


def bootstrap_ci(df: pd.DataFrame,
                 n_boot: int = N_BOOTSTRAP,
                 seed: int = RANDOM_SEED,
                 ci: float = 0.95) -> tuple[float, float]:
    """Bootstrapped percentile CI for Cronbach's alpha."""
    rng = np.random.default_rng(seed)
    n   = len(df)
    boot = []
    for _ in range(n_boot):
        sample = df.iloc[rng.integers(0, n, size=n)]
        k  = sample.shape[1]
        iv = sample.var(axis=0, ddof=1)
        tv = sample.sum(axis=1).var(ddof=1)
        if tv > 0:
            boot.append((k / (k - 1)) * (1 - iv.sum() / tv))
    lo = np.percentile(boot, (1 - ci) / 2 * 100)
    hi = np.percentile(boot, (1 + ci) / 2 * 100)
    return lo, hi


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_bori(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path)
    # First two rows have NaN in name column; items are columns 1-45
    data = raw.iloc[2: 2 + N_PARTICIPANTS, 1:46].copy()
    data.columns = [f"B{i}" for i in range(1, 46)]
    return data.map(lambda x: BORI_MAP.get(str(x).strip(), np.nan))


def load_eis(path: str) -> pd.DataFrame:
    raw = pd.read_excel(path)
    # Name column is col 1; items are columns 2-60
    data = raw.iloc[:N_PARTICIPANTS, 2:61].copy()
    data.columns = [f"E{i}" for i in range(1, 60)]
    return data.map(lambda x: EIS_MAP.get(str(x).strip(), np.nan))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def compute_reliability(bori_path: str, eis_path: str) -> pd.DataFrame:
    bori = load_bori(bori_path)
    eis  = load_eis(eis_path)

    rows = []
    for instrument, domains, enc in [
        ("BORI",    BORI_DOMAINS, bori),
        ("EIS-III", EIS_DOMAINS,  eis),
    ]:
        prefix = "B" if instrument == "BORI" else "E"
        for domain, item_nums in domains.items():
            cols = [f"{prefix}{i}" for i in item_nums if f"{prefix}{i}" in enc.columns]
            subset = enc[cols]
            alpha  = cronbach_alpha(subset)
            lo, hi = bootstrap_ci(subset)
            rows.append({
                "Instrument": instrument,
                "Domain":     domain,
                "alpha":      round(alpha, 3),
                "CI_lower":   round(lo, 3),
                "CI_upper":   round(hi, 3),
                "n_items":    len(cols),
                "n":          N_PARTICIPANTS,
            })

    return pd.DataFrame(rows)


def print_table(df: pd.DataFrame) -> None:
    print("\nSample-specific internal consistency estimates")
    print(f"(Cronbach's alpha, bootstrapped 95% CI, n={N_PARTICIPANTS})\n")
    print(f"{'Instrument':<10} {'Domain':<22} {'alpha':>6}  {'95% CI':^16}  {'Items':>5}")
    print("-" * 65)
    for _, row in df.iterrows():
        ci = f"[{row.CI_lower:.3f}, {row.CI_upper:.3f}]"
        print(f"{row.Instrument:<10} {row.Domain:<22} {row.alpha:>6.3f}  {ci:^16}  {row.n_items:>5}")
    print()
    print("Note: CI estimated via 2000 bootstrap iterations.")
    print("Conventional adequacy threshold: alpha >= 0.70")


if __name__ == "__main__":
    BORI_FILE = "Bell_Object_Relations_Testing_Inventory___Ответы_.xlsx"
    EIS_FILE  = "EIS_-_III___Ответы_.xlsx"

    results = compute_reliability(BORI_FILE, EIS_FILE)
    print_table(results)
    results.to_csv("reliability_results.csv", index=False)
    print("Results saved to reliability_results.csv")
