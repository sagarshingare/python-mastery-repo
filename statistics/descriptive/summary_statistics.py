"""Descriptive statistics helpers for analytics and reporting."""

from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd


def describe_series(series: pd.Series) -> Dict[str, float]:
    """Return a concise summary of a numeric pandas Series."""
    return {
        "count": float(series.count()),
        "mean": float(series.mean()),
        "std": float(series.std(ddof=1)),
        "min": float(series.min()),
        "max": float(series.max()),
        "median": float(series.median()),
        "variance": float(series.var(ddof=1)),
        "skewness": float(series.skew()),
        "kurtosis": float(series.kurtosis()),
    }


def z_score(series: pd.Series) -> pd.Series:
    """Compute z-scores for a numeric series."""
    mean = series.mean()
    std = series.std(ddof=1)
    return (series - mean) / std
