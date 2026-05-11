# PySpark Basics

This folder contains foundational PySpark examples and concepts for working with Apache Spark using Python.

## Included topics

- `spark_basics.py` - SparkSession, DataFrames, schema definition, and basic operations

## Python version

This module is written for Python 3.9+ and requires PySpark 3.5+.

## Learning outcomes

- Create and configure SparkSession
- Create DataFrames from various sources
- Define and apply custom schemas
- Perform basic DataFrame operations (filter, select)
- Inspect DataFrame metadata
- Work with PySpark efficiently

## Usage

Import the PySpark basics functions from `pyspark.basics` and use them in your applications.

Example:

```python
from pyspark.basics.spark_basics import create_spark_session, create_dataframe_from_list, sample_data

spark = create_spark_session("MyApp")
data = sample_data()
df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])
df.show()
```

## Run examples interactively

This package includes a CLI example runner that demonstrates PySpark basics concepts.

Run the examples as a Python package:

```bash
export PYTHONPATH=$(pwd)
python -m pyspark.basics.run_examples --module spark_session
python -m pyspark.basics.run_examples --module dataframe
python -m pyspark.basics.run_examples --module inspect
python -m pyspark.basics.run_examples --module filter
python -m pyspark.basics.run_examples --module select
```