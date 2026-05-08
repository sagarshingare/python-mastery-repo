"""A small production-grade batch ETL pipeline example."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@dataclass(frozen=True)
class ETLConfig:
    source_path: Path
    target_path: Path
    chunk_size: int


def load_config(config_path: Path) -> ETLConfig:
    """Load ETL configuration from YAML."""
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    return ETLConfig(
        source_path=Path(raw["source_path"]),
        target_path=Path(raw["target_path"]),
        chunk_size=int(raw.get("chunk_size", 1000)),
    )


def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform sales data for analytics and quality enforcement."""
    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0.0).astype(float)
    df["total_amount"] = df["quantity"] * df["unit_price"]
    df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")
    return df.dropna(subset=["product_name", "sales_date"])


def load_source_data(source_path: Path, chunk_size: int) -> pd.DataFrame:
    """Read source CSV in chunks for scalable batch processing."""
    return pd.concat(
        pd.read_csv(source_path, chunksize=chunk_size),
        ignore_index=True,
    )


def write_target_data(df: pd.DataFrame, target_path: Path) -> None:
    """Write transformed DataFrame to CSV in a production-friendly location."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=False)
    logger.info("Wrote transformed data to %s", target_path)


def run_pipeline(config_path: Path) -> None:
    """Run the batch ETL pipeline end to end."""
    config = load_config(config_path)
    logger.info("Running ETL pipeline with config: %s", config)

    source_df = load_source_data(config.source_path, config.chunk_size)
    transformed_df = transform_sales_data(source_df)
    write_target_data(transformed_df, config.target_path)
    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the batch ETL pipeline.")
    parser.add_argument("--config", default="projects/batch_etl_pipeline/config.yaml", help="Path to pipeline config YAML")
    args = parser.parse_args()
    run_pipeline(Path(args.config))
