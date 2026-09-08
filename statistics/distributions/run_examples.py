"""Demonstrations for Probability Distributions."""

from __future__ import annotations

import argparse
import numpy as np

from .probability_distributions import (
    normal_distribution_metrics,
    binomial_distribution_metrics,
    poisson_distribution_metrics,
    exponential_distribution_metrics,
    test_normality_kolmogorov_smirnov,
)


def demo_normal() -> None:
    print("--- 1. Normal Distribution N(0, 1) & Empirical Rule ---")
    res = normal_distribution_metrics(mean=0.0, std=1.0)
    print("  x-values: ", res["x_values"])
    print("  PDF:      ", [round(v, 4) for v in res["pdf"]])
    print("  CDF:      ", [round(v, 4) for v in res["cdf"]])
    print("  Coverage:")
    print(f"    - Within 1 SD (±1σ): {res['empirical_rule']['within_1_std']}% (expected ~68.27%)")
    print(f"    - Within 2 SD (±2σ): {res['empirical_rule']['within_2_std']}% (expected ~95.45%)")
    print(f"    - Within 3 SD (±3σ): {res['empirical_rule']['within_3_std']}% (expected ~99.73%)")


def demo_binomial() -> None:
    print("\n--- 2. Binomial Distribution B(n=10, p=0.5) ---")
    res = binomial_distribution_metrics(n=10, p=0.5)
    print(f"  Expected Value E[X]: {res['expected_value']}, Variance: {res['variance']}")
    for k, pmf, cdf in zip(res["k_values"], res["pmf"], res["cdf"]):
        print(f"  k={k:2d} -> P(X = k): {pmf:.4f} | P(X <= k): {cdf:.4f}")


def demo_poisson() -> None:
    print("\n--- 3. Poisson Distribution (λ = 5 arrivals/min) ---")
    res = poisson_distribution_metrics(mu=5.0)
    print(f"  Rate λ: {res['lambda_rate']}, Variance: {res['variance']}")
    for k, pmf, cdf in zip(res["k_values"], res["pmf"], res["cdf"]):
        print(f"  k={k:2d} arrivals -> P(X = k): {pmf:.4f} | P(X <= k): {cdf:.4f}")


def demo_exponential() -> None:
    print("\n--- 4. Exponential Distribution (scale = 2.0, λ = 0.5) ---")
    res = exponential_distribution_metrics(scale=2.0)
    print(f"  Mean (1/λ): {res['mean']}, λ rate: {res['lambda_rate']}")
    for x, pdf, cdf in zip(res["x_values"], res["pdf"], res["cdf"]):
        print(f"  x={x:.1f} -> PDF: {pdf:.4f} | CDF: {cdf:.4f}")


def demo_goodness_of_fit() -> None:
    print("\n--- 5. Goodness-of-Fit Normality Test (Kolmogorov-Smirnov) ---")
    np.random.seed(42)
    norm_sample = np.random.normal(50, 5, size=200)
    unif_sample = np.random.uniform(0, 100, size=200)

    res_norm = test_normality_kolmogorov_smirnov(norm_sample)
    print(f"  Sample from Normal dist:  KS-Stat={res_norm['statistic']:.4f}, p-val={res_norm['p_value']:.4f} -> Normal: {bool(res_norm['is_normal_05'])}")

    res_unif = test_normality_kolmogorov_smirnov(unif_sample)
    print(f"  Sample from Uniform dist: KS-Stat={res_unif['statistic']:.4f}, p-val={res_unif['p_value']:.4e} -> Normal: {bool(res_unif['is_normal_05'])}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Probability Distributions Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["all", "normal", "binomial", "poisson", "exponential", "fit"],
        default="all",
        help="Specific distribution demonstration to run",
    )
    args = parser.parse_args()

    print("=== PROBABILITY DISTRIBUTIONS DEMONSTRATIONS ===")
    if args.demo in ("all", "normal"):
        demo_normal()
    if args.demo in ("all", "binomial"):
        demo_binomial()
    if args.demo in ("all", "poisson"):
        demo_poisson()
    if args.demo in ("all", "exponential"):
        demo_exponential()
    if args.demo in ("all", "fit"):
        demo_goodness_of_fit()


if __name__ == "__main__":
    main()
