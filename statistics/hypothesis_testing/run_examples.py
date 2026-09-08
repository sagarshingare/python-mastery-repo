"""Demonstrations for Statistical Hypothesis Testing."""

from __future__ import annotations

import argparse
import numpy as np

from .hypothesis_tests import (
    one_sample_t_test,
    two_sample_t_test,
    paired_t_test,
    one_way_anova,
    chi_square_test_of_independence,
    mann_whitney_u_test,
)


def demo_one_sample() -> None:
    print("--- 1. One-Sample t-test (Baseline SLA: 200ms) ---")
    np.random.seed(42)
    response_times = np.random.normal(loc=208.5, scale=15.0, size=40)
    res = one_sample_t_test(response_times, pop_mean=200.0)
    print(f"  Sample Mean: {res['sample_mean']:.2f}ms vs Target: {res['pop_mean']}ms")
    print(f"  t-statistic: {res['t_statistic']:.4f}, p-value: {res['p_value']:.4f}")
    print(f"  Result: {res['interpretation']} (Reject H0: {res['reject_null']})")


def demo_two_sample_ab() -> None:
    print("\n--- 2. Two-Sample Welch's t-test (A/B Test Conversion Spend) ---")
    np.random.seed(42)
    control = np.random.normal(loc=45.0, scale=12.0, size=100)
    variant = np.random.normal(loc=51.5, scale=14.0, size=100)
    res = two_sample_t_test(control, variant)
    print(f"  Control Mean: ${res['mean_a']:.2f} | Variant Mean: ${res['mean_b']:.2f} (Δ=${res['diff_means']:.2f})")
    print(f"  t-statistic:  {res['t_statistic']:.4f}, p-value: {res['p_value']:.4e}")
    print(f"  Result: {res['interpretation']} (Reject H0: {res['reject_null']})")


def demo_paired() -> None:
    print("\n--- 3. Paired Samples t-test (Before vs After Training) ---")
    np.random.seed(42)
    before = np.random.normal(loc=65.0, scale=8.0, size=30)
    after = before + np.random.normal(loc=7.0, scale=3.0, size=30)  # genuine improvement
    res = paired_t_test(before, after)
    print(f"  Before: {res['mean_before']:.2f} | After: {res['mean_after']:.2f} (Avg Gain: +{res['mean_change']:.2f})")
    print(f"  t-statistic: {res['t_statistic']:.4f}, p-value: {res['p_value']:.4e}")
    print(f"  Result: {res['interpretation']} (Reject H0: {res['reject_null']})")


def demo_anova() -> None:
    print("\n--- 4. One-Way ANOVA (Comparing 3 Landing Page Variants) ---")
    np.random.seed(42)
    page_a = np.random.normal(10.0, 2.0, size=40)
    page_b = np.random.normal(10.5, 2.0, size=40)
    page_c = np.random.normal(12.5, 2.2, size=40)
    res = one_way_anova(page_a, page_b, page_c)
    print(f"  F-statistic: {res['f_statistic']:.4f}, p-value: {res['p_value']:.4e}")
    print(f"  Result: {res['interpretation']} (Reject H0: {res['reject_null']})")


def demo_chi_square() -> None:
    print("\n--- 5. Chi-Square Test of Independence (Device vs Purchase Decision) ---")
    # Rows: Mobile, Desktop. Columns: Purchased, Abandoned
    table = [[120, 280], [190, 210]]
    res = chi_square_test_of_independence(table)
    print(f"  Contingency Table: {table}")
    print(f"  Chi2-statistic: {res['chi2_statistic']:.4f}, p-value: {res['p_value']:.4e}, dof: {res['dof']}")
    print(f"  Result: {res['interpretation']} (Reject H0: {res['reject_null']})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hypothesis Testing Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "one_sample", "two_sample", "paired", "anova", "chi_square"],
        default="all",
        help="Specific hypothesis test to run",
    )
    args = parser.parse_args()

    print("=== STATISTICAL HYPOTHESIS TESTING DEMONSTRATIONS ===")
    if args.demo in ("all", "one_sample"):
        demo_one_sample()
    if args.demo in ("all", "two_sample"):
        demo_two_sample_ab()
    if args.demo in ("all", "paired"):
        demo_paired()
    if args.demo in ("all", "anova"):
        demo_anova()
    if args.demo in ("all", "chi_square"):
        demo_chi_square()


if __name__ == "__main__":
    main()
