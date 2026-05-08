"""Pandas helper functions for data cleaning and transformation."""

from __future__ import annotations

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare a sales dataset for analytics.

    - Normalize string fields
    - Fill missing values
    - Convert types for downstream aggregation
    """
    logger.debug("Starting sales data cleaning with %d rows", len(df))

    df = df.copy()
    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0).astype(float)
    df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")
    df = df.dropna(subset=["product_name", "sales_date"])

    logger.info("Completed cleaning sales data; final row count=%d", len(df))
    return df
