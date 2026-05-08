# Batch ETL Pipeline

This example demonstrates a configuration-driven batch ETL pipeline using pandas and YAML configuration.

## Features

- Config-driven ingestion with YAML
- Chunked CSV loading for scalability
- Type conversion, cleaning, and derived field generation
- Logging and path validation

## Run locally

```bash
python projects/batch_etl_pipeline/etl.py --config projects/batch_etl_pipeline/config.yaml
```
