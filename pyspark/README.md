# PySpark Data Processing

A comprehensive collection of PySpark examples for Apache Spark development with Python. This module covers core data processing concepts from basics to advanced optimization techniques.

## Included topics

- **basics** - SparkSession, DataFrames, schema definition, basic operations
- **transformations** - Map, filter, groupBy, window functions, union operations
- **spark_sql** - SQL queries, temporary tables, DataFrame SQL operations
- **streaming** - Structured streaming, event processing
- **partitioning** - Partition strategies, optimization, bucketing
- **optimization** - Caching, broadcasting, query optimization
- **delta_lake** - Delta Lake tables, ACID transactions
- **actions** - Collect, count, save, write operations

## Python version

This module is written for Python 3.9+ and requires PySpark 3.5+.

## Prerequisites

```bash
pip install pyspark>=3.5.0
```

## Learning outcomes

- Understand Apache Spark architecture and RDDs
- Create and manipulate DataFrames efficiently
- Write optimized Spark SQL queries
- Process streaming data in real-time
- Implement data partitioning strategies
- Optimize Spark jobs for performance
- Use Delta Lake for reliable data processing
- Handle large-scale data processing tasks

## Quick start

```python
from pyspark.basics.spark_basics import create_spark_session, create_dataframe_from_list, sample_data

# Create SparkSession
spark = create_spark_session("MyApp")

# Create DataFrame
data = sample_data()
df = create_dataframe_from_list(spark, data, ["id", "name", "salary"])

# Display data
df.show()
```

## Run learning modules

Each module includes interactive examples:

```bash
export PYTHONPATH=$(pwd)

# Basics
python -m pyspark.basics.run_examples --module spark_session
python -m pyspark.basics.run_examples --module dataframe

# Transformations
python -m pyspark.transformations.run_examples --module filter
python -m pyspark.transformations.run_examples --module groupby

# More modules...
```

## Module structure

```
pyspark/
├── basics/                    # DataFrame creation and basic operations
├── transformations/           # Map, filter, aggregations
├── spark_sql/                 # SQL operations
├── streaming/                 # Real-time data processing
├── partitioning/              # Partition optimization
├── optimization/              # Performance tuning
├── delta_lake/                # Delta Lake tables
└── actions/                   # Collect, save operations
```

## Best practices

1. **Always use DataFrames** over RDDs for better performance
2. **Cache intermediate results** to avoid recomputation
3. **Use Spark SQL** for complex queries
4. **Partition data efficiently** for parallel processing
5. **Monitor and optimize** job execution
6. **Use Delta Lake** for reliable data storage

## Testing

Run tests using pytest:

```bash
export PYTHONPATH=$(pwd)
pytest testing/pytest/test_pyspark*.py -v
```

## Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Delta Lake Documentation](https://docs.delta.io/)
