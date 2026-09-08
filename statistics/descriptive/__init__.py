"""Descriptive statistics package."""

from .summary_statistics import (
    describe_series,
    z_score,
    detect_iqr_outliers,
    compute_percentiles,
    compute_bivariate_metrics,
)

__all__ = [
    "describe_series",
    "z_score",
    "detect_iqr_outliers",
    "compute_percentiles",
    "compute_bivariate_metrics",
]