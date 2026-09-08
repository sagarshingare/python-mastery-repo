"""Probability distributions: Continuous and discrete models with PDF/PMF, CDF, and goodness-of-fit."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def normal_distribution_metrics(
    mean: float = 0.0,
    std: float = 1.0,
    x_values: List[float] = [-2.0, -1.0, 0.0, 1.0, 2.0],
) -> Dict[str, Any]:
    """Calculate PDF, CDF, and empirical rule intervals for a Normal distribution."""
    dist = stats.norm(loc=mean, scale=std)
    pdf_vals = [float(dist.pdf(x)) for x in x_values]
    cdf_vals = [float(dist.cdf(x)) for x in x_values]

    # Empirical 68-95-99.7 rule interval coverage
    rule_1_std = float(dist.cdf(mean + std) - dist.cdf(mean - std))
    rule_2_std = float(dist.cdf(mean + 2 * std) - dist.cdf(mean - 2 * std))
    rule_3_std = float(dist.cdf(mean + 3 * std) - dist.cdf(mean - 3 * std))

    return {
        "mean": mean,
        "std": std,
        "x_values": x_values,
        "pdf": pdf_vals,
        "cdf": cdf_vals,
        "empirical_rule": {
            "within_1_std": round(rule_1_std * 100.0, 2),
            "within_2_std": round(rule_2_std * 100.0, 2),
            "within_3_std": round(rule_3_std * 100.0, 2),
        },
    }


def binomial_distribution_metrics(
    n: int = 10,
    p: float = 0.5,
    k_values: List[int] = [0, 2, 5, 8, 10],
) -> Dict[str, Any]:
    """Calculate PMF and CDF for a Binomial distribution B(n, p)."""
    dist = stats.binom(n=n, p=p)
    pmf_vals = [float(dist.pmf(k)) for k in k_values]
    cdf_vals = [float(dist.cdf(k)) for k in k_values]

    return {
        "n": n,
        "p": p,
        "expected_value": float(dist.mean()),
        "variance": float(dist.var()),
        "k_values": k_values,
        "pmf": pmf_vals,
        "cdf": cdf_vals,
    }


def poisson_distribution_metrics(
    mu: float = 5.0,
    k_values: List[int] = [0, 2, 5, 8, 12],
) -> Dict[str, Any]:
    """Calculate PMF and CDF for a Poisson distribution with arrival rate mu."""
    dist = stats.poisson(mu=mu)
    pmf_vals = [float(dist.pmf(k)) for k in k_values]
    cdf_vals = [float(dist.cdf(k)) for k in k_values]

    return {
        "lambda_rate": mu,
        "mean": float(dist.mean()),
        "variance": float(dist.var()),
        "k_values": k_values,
        "pmf": pmf_vals,
        "cdf": cdf_vals,
    }


def exponential_distribution_metrics(
    scale: float = 2.0,  # scale = 1 / lambda
    x_values: List[float] = [0.5, 1.0, 2.0, 4.0],
) -> Dict[str, Any]:
    """Calculate PDF and CDF for an Exponential distribution."""
    dist = stats.expon(scale=scale)
    pdf_vals = [float(dist.pdf(x)) for x in x_values]
    cdf_vals = [float(dist.cdf(x)) for x in x_values]

    return {
        "lambda_rate": 1.0 / scale,
        "mean": float(dist.mean()),
        "variance": float(dist.var()),
        "x_values": x_values,
        "pdf": pdf_vals,
        "cdf": cdf_vals,
    }


def evaluate_normality_ks(data: np.ndarray) -> Dict[str, float]:
    """Perform Kolmogorov-Smirnov test to evaluate adherence to a normal distribution."""
    clean = np.asarray(data)
    mean = np.mean(clean)
    std = np.std(clean, ddof=1)
    # Standardize data to N(0, 1)
    standardized = (clean - mean) / max(std, 1e-9)
    stat, p_value = stats.kstest(standardized, "norm")

    return {
        "statistic": float(stat),
        "p_value": float(p_value),
        "is_normal_05": float(p_value > 0.05),
    }


# Backwards compatibility alias
test_normality_kolmogorov_smirnov = evaluate_normality_ks

