# PySpark Actions

This folder contains PySpark action examples for retrieving and persisting data.

## Included topics

- `actions.py` - collect, count, first, take, show, foreach, write operations

## Python version

This module is written for Python 3.9+ and requires PySpark 3.5+.

## Learning outcomes

- Retrieve data from DataFrames with collect, first, and take
- Count rows and get statistics
- Display formatted DataFrame output
- Apply functions to each row with foreach
- Write DataFrames to multiple formats (Parquet, CSV, JSON, SQL tables)
- Handle write modes and error cases

## Usage

Import the action functions from `pyspark.actions` and use them in your applications.

Example:

```python
from pyspark.basics.spark_basics import create_spark_session, create_dataframe_from_list, sample_data
from pyspark.actions.actions import collect_data, count_rows, write_parquet

spark = create_spark_session("Actions-App")
df = create_dataframe_from_list(spark, sample_data(), ["id", "name", "salary"])

# Actions
row_count = count_rows(df)
data = collect_data(df)
write_parquet(df, "/path/to/output")
```

## Run examples interactively

This package includes a CLI example runner that demonstrates PySpark actions.

Run the examples as a Python package:

```bash
export PYTHONPATH=$(pwd)
python -m pyspark.actions.run_examples --module collect
python -m pyspark.actions.run_examples --module count
python -m pyspark.actions.run_examples --module first
python -m pyspark.actions.run_examples --module show
python -m pyspark.actions.run_examples --module foreach
python -m pyspark.actions.run_examples --module statistics
python -m pyspark.actions.run_examples --module write
```

## Action Types

### Display Actions
- **show()** - Display formatted DataFrame in console
- **collect()** - Retrieve all data to driver memory
- **first()** - Get first row
- **take(n)** - Get first n rows

### Aggregation Actions
- **count()** - Count total rows
- **foreach()** - Apply function to each row

### Write Actions
- **write.parquet()** - Write to Parquet format (columnar, compressed)
- **write.csv()** - Write to CSV format
- **write.json()** - Write to JSON format
- **write.saveAsTable()** - Create SQL table

## Best Practices

1. **Avoid collect() on large DataFrames** - it brings all data to driver memory
2. **Use take(n) for sampling** instead of collect for large data
3. **Prefer Parquet format** for data persistence (better compression, schema preservation)
4. **Use write modes carefully**:
   - `overwrite` - replace existing data
   - `append` - add to existing data
   - `ignore` - do nothing if data exists
   - `error` - raise error if data exists
5. **Use foreach for side effects** (logging, external updates)
6. **Monitor driver memory** when collecting data