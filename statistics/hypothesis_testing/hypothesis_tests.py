"""Statistical hypothesis testing: Parametric and non-parametric tests for inference and A/B testing."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Sequence

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


def one_sample_t_test(
    sample: Sequence[float],
    pop_mean: float,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Test if a sample mean significantly differs from a hypothesized population mean."""
    data = np.asarray(sample)
    t_stat, p_val = stats.ttest_1samp(data, pop_mean)
    reject = bool(p_val < alpha)

    return {
        "test": "One-Sample t-test",
        "sample_mean": float(np.mean(data)),
        "pop_mean": pop_mean,
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "Sample mean differs significantly from baseline" if reject else "Fail to reject null hypothesis",
    }


def two_sample_t_test(
    group_a: Sequence[float],
    group_b: Sequence[float],
    equal_var: bool = False,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Test if two independent groups differ significantly (Welch's t-test by default)."""
    a = np.asarray(group_a)
    b = np.asarray(group_b)
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=equal_var)
    reject = bool(p_val < alpha)

    return {
        "test": "Two-Sample Welch's t-test" if not equal_var else "Two-Sample Student's t-test",
        "mean_a": float(np.mean(a)),
        "mean_b": float(np.mean(b)),
        "diff_means": float(np.mean(b) - np.mean(a)),
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "Statistically significant difference between groups" if reject else "No significant difference detected",
    }


def paired_t_test(
    before: Sequence[float],
    after: Sequence[float],
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Test difference between paired observations before and after intervention."""
    b = np.asarray(before)
    a = np.asarray(after)
    t_stat, p_val = stats.ttest_rel(b, a)
    reject = bool(p_val < alpha)

    return {
        "test": "Paired Samples t-test",
        "mean_before": float(np.mean(b)),
        "mean_after": float(np.mean(a)),
        "mean_change": float(np.mean(a - b)),
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "Intervention produced a statistically significant change" if reject else "No significant change observed",
    }


def one_way_anova(
    *groups: Sequence[float],
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Test if any group mean differs significantly among 3 or more independent groups."""
    group_arrays = [np.asarray(g) for g in groups]
    f_stat, p_val = stats.f_oneway(*group_arrays)
    reject = bool(p_val < alpha)

    return {
        "test": "One-Way ANOVA",
        "num_groups": len(groups),
        "f_statistic": float(f_stat),
        "p_value": float(p_val),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "At least one group mean is statistically different" if reject else "All group means are statistically consistent",
    }


def chi_square_test_of_independence(
    contingency_table: Sequence[Sequence[int]],
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Test categorical independence between two variables given a 2D contingency table."""
    table = np.asarray(contingency_table)
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(table)
    reject = bool(p_val < alpha)

    return {
        "test": "Chi-Square Test of Independence",
        "chi2_statistic": float(chi2_stat),
        "p_value": float(p_val),
        "dof": int(dof),
        "expected_frequencies": expected.tolist(),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "Variables are significantly dependent" if reject else "Variables appear statistically independent",
    }


def mann_whitney_u_test(
    group_a: Sequence[float],
    group_b: Sequence[float],
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Non-parametric rank-sum test for two independent distributions."""
    a = np.asarray(group_a)
    b = np.asarray(group_b)
    stat, p_val = stats.mannwhitneyu(a, b, alternative="two-sided")
    reject = bool(p_val < alpha)

    return {
        "test": "Mann-Whitney U Test",
        "u_statistic": float(stat),
        "p_value": float(p_val),
        "alpha": alpha,
        "reject_null": reject,
        "interpretation": "Distributions of groups differ significantly" if reject else "No significant difference in rank distributions",
    }
