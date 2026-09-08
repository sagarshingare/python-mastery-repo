"""Descriptive statistics helpers for analytics and reporting."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def describe_series(series: pd.Series) -> Dict[str, float]:
    """Return a comprehensive summary of a numeric pandas Series."""
    clean = series.dropna()
    q25 = float(clean.quantile(0.25))
    q75 = float(clean.quantile(0.75))
    iqr = q75 - q25

    return {
        "count": float(clean.count()),
        "mean": float(clean.mean()),
        "std": float(clean.std(ddof=1)),
        "min": float(clean.min()),
        "q25": q25,
        "median": float(clean.median()),
        "q75": q75,
        "max": float(clean.max()),
        "iqr": float(iqr),
        "range": float(clean.max() - clean.min()),
        "variance": float(clean.var(ddof=1)),
        "skewness": float(clean.skew()),
        "kurtosis": float(clean.kurtosis()),
    }


def z_score(series: pd.Series) -> pd.Series:
    """Compute z-scores for a numeric series."""
    mean = series.mean()
    std = series.std(ddof=1)
    if std == 0.0 or pd.isna(std):
        return pd.Series(0.0, index=series.index)
    return (series - mean) / std


def detect_iqr_outliers(series: pd.Series, whisker: float = 1.5) -> Tuple[pd.Series, Dict[str, float]]:
    """Identify outliers using John Tukey's IQR fence method."""
    clean = series.dropna()
    q25 = float(clean.quantile(0.25))
    q75 = float(clean.quantile(0.75))
    iqr = q75 - q25
    lower_bound = q25 - whisker * iqr
    upper_bound = q75 + whisker * iqr

    is_outlier = (series < lower_bound) | (series > upper_bound)
    bounds = {
        "q25": q25,
        "q75": q75,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": float(is_outlier.sum()),
    }
    return is_outlier, bounds


def compute_percentiles(
    series: pd.Series, percentiles: List[float] = [10.0, 25.0, 50.0, 75.0, 90.0, 95.0, 99.0]
) -> Dict[str, float]:
    """Calculate explicit percentile thresholds."""
    clean = series.dropna()
    results = {}
    for p in percentiles:
        results[f"p{int(p)}"] = float(np.percentile(clean, p))
    return results


def compute_bivariate_metrics(series_a: pd.Series, series_b: pd.Series) -> Dict[str, float]:
    """Compute covariance, Pearson linear correlation, and Spearman monotonic rank correlation."""
    df = pd.DataFrame({"a": series_a, "b": series_b}).dropna()
    cov = float(df["a"].cov(df["b"]))
    pearson_corr = float(df["a"].corr(df["b"], method="pearson"))
    spearman_corr = float(df["a"].corr(df["b"], method="spearman"))

    return {
        "sample_size": float(len(df)),
        "covariance": cov,
        "pearson_correlation": pearson_corr,
        "spearman_correlation": spearman_corr,
    }
