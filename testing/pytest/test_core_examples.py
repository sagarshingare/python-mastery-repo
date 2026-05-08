"""Unit tests for core Python examples."""

from __future__ import annotations

import pandas as pd
import pytest

from core_python.basics.variables import compute_discounted_price
from core_python.oops.classes import Order, calculate_total_revenue
from pandas.basics.dataframe_helper import clean_sales_data


def test_compute_discounted_price_valid() -> None:
    assert compute_discounted_price(100.0, 0.2) == 80.0


def test_compute_discounted_price_invalid_rate() -> None:
    with pytest.raises(ValueError):
        compute_discounted_price(100.0, 1.5)


def test_calculate_total_revenue() -> None:
    orders = [Order("A", 1, 20.0), Order("B", 2, 15.5)]
    assert calculate_total_revenue(orders) == 51.0


def test_clean_sales_data() -> None:
    df = pd.DataFrame(
        {
            "sales_date": ["2026-05-01", None],
            "product_name": ["Widget A", "Widget B"],
            "quantity": ["10", "5"],
            "unit_price": ["12.5", "25.0"],
        }
    )
    cleaned = clean_sales_data(df)
    assert cleaned.shape[0] == 1
    assert cleaned["quantity"].dtype == int
    assert cleaned["unit_price"].dtype == float
