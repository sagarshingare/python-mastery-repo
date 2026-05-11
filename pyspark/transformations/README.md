# PySpark Transformations

This folder contains PySpark transformation examples for processing and manipulating data.

## Included topics

- `transformations.py` - map, filter, groupBy, window functions, and union operations

## Python version

This module is written for Python 3.9+ and requires PySpark 3.5+.

## Learning outcomes

- Apply map and filter transformations
- Use groupBy and aggregation functions
- Implement window functions for advanced analytics
- Union and join DataFrames
- Flatten nested data structures

## Usage

Import the transformation functions from `pyspark.transformations` and use them in your applications.

Example:

```python
from pyspark.basics.spark_basics import create_spark_session, create_dataframe_from_list, sample_data
from pyspark.transformations.transformations import filter_greater_than, group_and_aggregate

spark = create_spark_session("Transform-App")
df = create_dataframe_from_list(spark, sample_data(), ["id", "name", "salary"])
filtered = filter_greater_than(df, "salary", 55000)
filtered.show()
```

## Run examples interactively

This package includes a CLI example runner that demonstrates PySpark transformations.

Run the examples as a Python package:

```bash
export PYTHONPATH=$(pwd)
python -m pyspark.transformations.run_examples --module map
python -m pyspark.transformations.run_examples --module filter
python -m pyspark.transformations.run_examples --module groupby
python -m pyspark.transformations.run_examples --module window
python -m pyspark.transformations.run_examples --module union
```