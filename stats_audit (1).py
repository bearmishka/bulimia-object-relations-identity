from math import sqrt
from scipy import stats


N = 28
K = 4


def p_from_r(r: float, n: int = N):
    df = n - 2
    t_value = r * sqrt(df / (1 - r * r))
    p_value = 2 * stats.t.sf(abs(t_value), df)
    return t_value, p_value


def p_from_t(t_value: float, df: int):
    return 2 * stats.t.sf(abs(t_value), df)


def model_p_from_r2(r2: float, n: int = N, k: int = K):
    df1 = k
    df2 = n - k - 1
    f_value = (r2 / df1) / ((1 - r2) / df2)
    p_value = stats.f.sf(f_value, df1, df2)
    return f_value, p_value


if __name__ == "__main__":
    print("=== Correlation checks (n=28) ===")
    correlations = [
        ("BORI ALN-IA", 0.517279269604765, 0.004818815709460248),
        ("BORI ALN-EGC", 0.1531166135354035, 0.4366391159140733),
        ("BORI ALN-SI", 0.7355964256563562, 8.19613592845609e-06),
        ("BORI IA-EGC", 0.3835085289131295, 0.04394746381648987),
        ("BORI IA-SI", 0.6757036922702089, 7.950828330745678e-05),
        ("BORI EGC-SI", 0.234361263192518, 0.22998806248983558),
        ("EIS Conf-Sex", 0.87, 2.65e-09),
        ("EIS Conf-Body", 0.91, 3.61e-11),
        ("EIS Sex-Body", 0.88, 7.1e-10),
    ]
    for name, r, p_report in correlations:
        _, p_calc = p_from_r(r)
        print(f"{name:14s}  p_report={p_report:.12g}  p_calc={p_calc:.12g}")

    print("\n=== Regression model-level checks ===")
    for name, r2 in [
        ("Confidence", 0.58),
        ("Sexual identity", 0.62),
        ("Body/appearance", 0.391),
    ]:
        f_value, p_value = model_p_from_r2(r2)
        print(f"{name:14s}  R2={r2:.3f}  F={f_value:.4f}  p={p_value:.6g}")

    print("\n=== Regression coefficient checks (df=23) ===")
    df = N - K - 1
    t_values = [
        ("T6 ALN", -3.46, 0.002),
        ("T6 IA", -3.45, 0.002),
        ("T6 EGC", -0.92, 0.366),
        ("T6 SI", -2.70, 0.012),
        ("T7 ALN", 3.17, 0.004),
        ("T7 IA", 4.50, 0.001),
        ("T7 EGC", -2.00, 0.058),
        ("T7 SI", 3.44, 0.002),
        ("T8 ALN", 3.96, 0.001),
        ("T8 IA", 2.37, 0.024),
        ("T8 EGC", 1.35, 0.187),
        ("T8 SI", 3.26, 0.003),
    ]
    for name, t_value, p_report in t_values:
        p_calc = p_from_t(t_value, df)
        print(f"{name:8s}  p_report={p_report:.6g}  p_calc={p_calc:.6g}")
