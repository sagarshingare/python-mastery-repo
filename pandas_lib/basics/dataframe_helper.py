"""Pandas helper functions for data cleaning, string manipulation, and datetime feature engineering."""

from __future__ import annotations

import logging
from typing import Dict

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


def handle_missing_values(
    df: pd.DataFrame,
    numeric_strategy: str = "mean",
    categorical_fill: str = "Unknown",
) -> pd.DataFrame:
    """Impute or clean missing values across numeric and categorical columns."""
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            if numeric_strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif numeric_strategy == "median":
                df[col] = df[col].fillna(df[col].median())
            elif numeric_strategy == "zero":
                df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna(categorical_fill)
    return df


def transform_string_columns(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """Apply vectorized string transformations and extract metadata tokens."""
    df = df.copy()
    s = df[text_col].astype(str).str.strip()
    df[f"{text_col}_clean"] = s.str.lower()
    df[f"{text_col}_len"] = s.str.len()
    # Extract leading uppercase code prefix e.g. "SKU123" -> "SKU"
    df[f"{text_col}_code"] = s.str.extract(r"^([A-Za-z]+)", expand=False).fillna("N/A")
    return df


def extract_datetime_features(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Engineer calendar features from a datetime column."""
    df = df.copy()
    dt_series = pd.to_datetime(df[date_col], errors="coerce")
    df[f"{date_col}_year"] = dt_series.dt.year
    df[f"{date_col}_month"] = dt_series.dt.month
    df[f"{date_col}_quarter"] = dt_series.dt.quarter
    df[f"{date_col}_day_name"] = dt_series.dt.day_name()
    df[f"{date_col}_is_weekend"] = dt_series.dt.dayofweek.isin([5, 6])
    return df
