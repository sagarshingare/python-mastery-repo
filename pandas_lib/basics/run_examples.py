"""CLI runner for Pandas Basics demonstrations."""

from __future__ import annotations

import argparse
import logging
import pandas as pd

from pandas_lib.basics.dataframe_helper import (
    clean_sales_data,
    extract_datetime_features,
    handle_missing_values,
    transform_string_columns,
)

logger = logging.getLogger(__name__)


def run_cleaning_demo() -> None:
    logger.info("Running Pandas Basics: Sales Data Cleaning Pipeline")
    raw_data = pd.DataFrame(
        {
            "Product Name": ["Widget A", "Gadget B", "Widget A", None],
            "Quantity": ["10", "invalid", "5", "2"],
            "Unit Price": ["19.99", "45.50", None, "10.00"],
            "Sales Date": ["2026-01-15", "2026-02-20", "2026-03-10", "invalid_date"],
        }
    )
    print("Raw Input DataFrame:")
    print(raw_data)

    cleaned = clean_sales_data(raw_data)
    print("\nCleaned & Coerced DataFrame:")
    print(cleaned)


def run_missing_data_demo() -> None:
    logger.info("Running Pandas Basics: Missing Value Imputation")
    df = pd.DataFrame(
        {
            "score": [90.0, None, 70.0, None, 85.0],
            "department": ["Engineering", "Product", None, "Engineering", None],
        }
    )
    imputed = handle_missing_values(df, numeric_strategy="mean")
    print("Original with NaNs:")
    print(df)
    print("\nImputed (Mean for score, 'Unknown' for department):")
    print(imputed)


def run_datetime_demo() -> None:
    logger.info("Running Pandas Basics: Datetime & String Feature Engineering")
    df = pd.DataFrame(
        {
            "product_tag": ["SKU1001-A", "item-99", "PROD5050-Z"],
            "order_date": ["2026-01-17", "2026-06-03", "2026-10-25"],
        }
    )
    str_df = transform_string_columns(df, "product_tag")
    feat_df = extract_datetime_features(str_df, "order_date")
    print("Engineered Datetime & String Features:")
    print(feat_df[["product_tag", "product_tag_code", "order_date_day_name", "order_date_is_weekend"]])


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas Basics Demonstrations")
    parser.add_argument(
        "--demo",
        choices=["cleaning", "missing_data", "datetime", "all"],
        default="all",
        help="Demonstration to run (default: all)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    dispatch = {
        "cleaning": run_cleaning_demo,
        "missing_data": run_missing_data_demo,
        "datetime": run_datetime_demo,
    }

    if args.demo == "all":
        for fn in dispatch.values():
            fn()
            print()
    else:
        dispatch[args.demo]()


if __name__ == "__main__":
    main()
