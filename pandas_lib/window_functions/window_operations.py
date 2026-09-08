"""Pandas window functions: rolling aggregates, expanding metrics, exponential moving averages, and partitioned ranking."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def calculate_rolling_metrics(
    df: pd.DataFrame,
    value_col: str,
    window: int = 3,
    min_periods: int = 1,
) -> pd.DataFrame:
    """Compute rolling window mean, standard deviation, and min/max boundaries."""
    df = df.copy()
    rolling = df[value_col].rolling(window=window, min_periods=min_periods)
    df[f"{value_col}_rolling_mean_{window}"] = rolling.mean()
    df[f"{value_col}_rolling_std_{window}"] = rolling.std().fillna(0.0)
    df[f"{value_col}_rolling_min_{window}"] = rolling.min()
    df[f"{value_col}_rolling_max_{window}"] = rolling.max()
    return df


def calculate_expanding_metrics(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Compute cumulative metrics (cumulative sum, running maximum, expanding mean)."""
    df = df.copy()
    expanding = df[value_col].expanding(min_periods=1)
    df[f"{value_col}_cumsum"] = df[value_col].cumsum()
    df[f"{value_col}_cummax"] = df[value_col].cummax()
    df[f"{value_col}_expanding_mean"] = expanding.mean()
    return df


def calculate_exponential_moving_average(
    df: pd.DataFrame,
    value_col: str,
    span: int = 12,
) -> pd.DataFrame:
    """Compute exponentially weighted moving average (EWMA)."""
    df = df.copy()
    df[f"{value_col}_ema_{span}"] = df[value_col].ewm(span=span, adjust=False).mean()
    return df


def calculate_partitioned_ranks(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    ascending: bool = False,
    method: str = "dense",
) -> pd.DataFrame:
    """Compute ranking within partitions (equivalent to SQL RANK() OVER (PARTITION BY ... ORDER BY ...))."""
    df = df.copy()
    df["rank"] = df.groupby(group_col)[value_col].rank(ascending=ascending, method=method).astype(int)
    return df


def calculate_lag_and_returns(
    df: pd.DataFrame,
    group_col: Optional[str] = None,
    value_col: str = "close",
    periods: int = 1,
) -> pd.DataFrame:
    """Compute previous value (lag), forward value (lead), and percentage return."""
    df = df.copy()
    if group_col:
        grouped = df.groupby(group_col)[value_col]
        df[f"{value_col}_lag_{periods}"] = grouped.shift(periods)
        df[f"{value_col}_lead_{periods}"] = grouped.shift(-periods)
        df[f"{value_col}_pct_change"] = grouped.pct_change(periods=periods)
    else:
        df[f"{value_col}_lag_{periods}"] = df[value_col].shift(periods)
        df[f"{value_col}_lead_{periods}"] = df[value_col].shift(-periods)
        df[f"{value_col}_pct_change"] = df[value_col].pct_change(periods=periods)
    return df
