"""Tests for the sample batch ETL pipeline."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from projects.batch_etl_pipeline.etl import ETLConfig, load_config, transform_sales_data


def test_load_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "source_path: projects/batch_etl_pipeline/sample_data/sales.csv\ntarget_path: projects/batch_etl_pipeline/sample_data/transformed_sales.csv\nchunk_size: 50\n"
    )
    config = load_config(config_file)
    assert config.chunk_size == 50
    assert config.source_path.name == "sales.csv"


def test_transform_sales_data() -> None:
    df = pd.DataFrame(
        {
            "sales_date": ["2026-05-01", "2026-05-02"],
            "product_name": ["Widget A", "Widget B"],
            "quantity": ["10", "5"],
            "unit_price": ["12.5", "25.0"],
        }
    )
    transformed = transform_sales_data(df)
    assert "total_amount" in transformed.columns
    assert transformed.loc[0, "total_amount"] == 125.0
