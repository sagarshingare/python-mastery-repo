"""Pandas join and merge operations: relational joins, indicator diagnostics, concatenation, and asof time series alignment."""

from __future__ import annotations

import logging
from typing import List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def perform_relational_merge(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    on: str,
    how: str = "inner",
    indicator: bool = False,
) -> pd.DataFrame:
    """Execute standard relational merge (inner, left, right, outer) with optional merge indicator."""
    logger.debug("Merging dataframes on '%s' with method '%s'", on, how)
    return pd.merge(left_df, right_df, on=on, how=how, indicator=indicator)


def join_on_index(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    how: str = "left",
    lsuffix: str = "_left",
    rsuffix: str = "_right",
) -> pd.DataFrame:
    """Execute index-based join with column collision renaming."""
    return left_df.join(right_df, how=how, lsuffix=lsuffix, rsuffix=rsuffix)


def concatenate_dataframes(
    dfs: List[pd.DataFrame],
    axis: int = 0,
    ignore_index: bool = True,
) -> pd.DataFrame:
    """Concatenate multiple DataFrames vertically (axis=0) or horizontally (axis=1)."""
    return pd.concat(dfs, axis=axis, ignore_index=ignore_index)


def merge_asof_timestamps(
    trades_df: pd.DataFrame,
    quotes_df: pd.DataFrame,
    on: str = "timestamp",
    by: Optional[str] = "symbol",
    direction: str = "backward",
) -> pd.DataFrame:
    """Align time-series records by exact or nearest preceding/following timestamp (as-of join).
    
    DataFrames must be sorted by the key column 'on'.
    """
    trades_sorted = trades_df.sort_values(on).reset_index(drop=True)
    quotes_sorted = quotes_df.sort_values(on).reset_index(drop=True)
    return pd.merge_asof(
        trades_sorted,
        quotes_sorted,
        on=on,
        by=by,
        direction=direction,
    )


def validate_cardinality_merge(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    on: str,
    validate: str = "1:1",
) -> pd.DataFrame:
    """Merge while validating key uniqueness (e.g. 'one_to_one', 'one_to_many', 'many_to_one')."""
    return pd.merge(left_df, right_df, on=on, validate=validate)
