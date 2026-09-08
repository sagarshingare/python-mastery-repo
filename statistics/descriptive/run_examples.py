"""Demonstrations for Descriptive Statistics and Outlier Detection."""

from __future__ import annotations

import argparse
import numpy as np
import pandas as pd

from .summary_statistics import (
    describe_series,
    z_score,
    detect_iqr_outliers,
    compute_percentiles,
    compute_bivariate_metrics,
)


def get_sample_salaries() -> pd.Series:
    np.random.seed(42)
    # Typical log-normalish distribution with injected outliers
    base = np.random.normal(loc=75000, scale=12000, size=100)
    outliers = [250000, 320000, 15000]
    return pd.Series(np.concatenate([base, outliers]), name="salary")


def demo_summary() -> None:
    salaries = get_sample_salaries()
    print("--- 1. Comprehensive Univariate Metrics ---")
    summary = describe_series(salaries)
    for k, v in summary.items():
        print(f"  {k:<12}: {v:,.2f}")


def demo_outliers() -> None:
    salaries = get_sample_salaries()
    print("\n--- 2. Tukey IQR Outlier Detection ---")
    is_outlier, bounds = detect_iqr_outliers(salaries)
    print(f"  Q25: ${bounds['q25']:,.2f} | Q75: ${bounds['q75']:,.2f} | IQR: ${bounds['iqr']:,.2f}")
    print(f"  Valid Range: [${bounds['lower_bound']:,.2f}, ${bounds['upper_bound']:,.2f}]")
    print(f"  Detected {int(bounds['outlier_count'])} outliers:")
    for val in salaries[is_outlier]:
        print(f"    - ${val:,.2f}")


def demo_bivariate() -> None:
    print("\n--- 3. Bivariate Relationships (Pearson & Spearman) ---")
    np.random.seed(42)
    years_exp = pd.Series(np.random.uniform(1, 20, size=50), name="experience")
    salary = years_exp * 4500 + np.random.normal(30000, 5000, size=50)
    metrics = compute_bivariate_metrics(years_exp, salary)
    print(f"  Covariance:           {metrics['covariance']:,.2f}")
    print(f"  Pearson Correlation:  {metrics['pearson_correlation']:.4f}")
    print(f"  Spearman Correlation: {metrics['spearman_correlation']:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Descriptive Statistics Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "summary", "outliers", "bivariate"],
        default="all",
        help="Specific descriptive demo to run",
    )
    args = parser.parse_args()

    print("=== DESCRIPTIVE STATISTICS DEMONSTRATIONS ===")
    if args.demo in ("all", "summary"):
        demo_summary()
    if args.demo in ("all", "outliers"):
        demo_outliers()
    if args.demo in ("all", "bivariate"):
        demo_bivariate()


if __name__ == "__main__":
    main()
