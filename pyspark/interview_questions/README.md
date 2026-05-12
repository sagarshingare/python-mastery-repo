# PySpark Interview Questions & Coding Problems

Comprehensive collection of PySpark interview questions, most asked topics, and LeetCode-style coding problems with detailed solutions.

## Coverage

### Fundamental Concepts
- RDD vs DataFrame (when to use each, performance differences)
- Catalyst Optimizer (stages, optimization strategies, query optimization)
- Spark Shuffle (performance impact, cost, mitigation)
- Lazy Evaluation (why Spark uses it, transformations vs actions)
- Partitioning concepts and best practices

### Partitioning & Optimization
- Optimal partition count calculation
- Bucketing strategy and advantages
- Skewed data handling
- Partition pruning
- Co-partitioning for joins

### Memory & Caching
- Caching strategies and storage levels
- Broadcast vs Shuffle joins
- Memory management tuning
- GC optimization
- Out of memory issues

### Most Asked Interview Questions
1. **Lazy Evaluation** - What it is and why Spark uses it
2. **DataFrame vs RDD** - When to use which
3. **Memory Issues** - How to fix OutOfMemoryError
4. **Skewed Data** - Data skew handling techniques
5. **Join Performance** - Optimizing join operations

### Coding Problems (LeetCode Style)
1. **Top N Salary** - Find top earners per department (Window functions)
2. **Duplicate Emails** - Find duplicate emails (GroupBy)
3. **Second Highest Salary** - Find 2nd highest unique salary (Window ranking)
4. **Cumulative Sum** - Running total over time (Window aggregation)
5. **Top K Frequent** - Find K most frequent elements (GroupBy + Sort)

### Performance Tuning
- SQL vs DataFrame API
- Reading and interpreting explain() plans
- Query optimization patterns
- Common performance bottlenecks
- Monitoring and debugging

## Python version

Python 3.9+ with PySpark 3.5+

## Key Learning Outcomes

- Understand PySpark architecture and execution model
- Master optimization techniques for production systems
- Know when and how to use different join strategies
- Handle real-world performance challenges
- Ace technical interviews

## Run Examples

Interactive CLI with all questions and problems:

```bash
export PYTHONPATH=$(pwd)

# Run specific topics
python -m pyspark.interview_questions.run_examples --module fundamentals
python -m pyspark.interview_questions.run_examples --module partitioning
python -m pyspark.interview_questions.run_examples --module memory
python -m pyspark.interview_questions.run_examples --module most_asked
python -m pyspark.interview_questions.run_examples --module coding_problems
python -m pyspark.interview_questions.run_examples --module performance

# Run all
python -m pyspark.interview_questions.run_examples
python -m pyspark.interview_questions.run_examples --module all
```

## Topics by Difficulty

### Beginner
- RDD vs DataFrame
- Basic partitioning
- Cache operations
- Lazy evaluation

### Intermediate
- Catalyst optimizer
- Join strategies
- Window functions
- Partitioning optimization

### Advanced
- Data skew handling
- Memory tuning
- Shuffle optimization
- Query plan analysis
- Distributed computing concepts

## Real Interview Tips

1. **Prepare code examples** - Have concrete examples ready
2. **Understand the "why"** - Not just how, but why you choose solutions
3. **Think about trade-offs** - Every optimization has costs
4. **Ask clarifying questions** - Data size, frequency, SLA
5. **Discuss monitoring** - How would you know if it works
6. **Consider alternatives** - What if requirements change

## Common Pitfalls to Avoid

- ❌ Using RDD for structured data (use DataFrame)
- ❌ Forgetting to handle NULL values
- ❌ Not considering data skew in joins
- ❌ Caching too aggressively (memory issues)
- ❌ Using collect() on large DataFrames
- ❌ Not using broadcast join for small tables
- ❌ Ignoring partition count tuning

## Resource Links

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark Performance Tuning](https://spark.apache.org/docs/latest/tuning.html)
- [Catalyst Optimizer](https://spark.apache.org/docs/latest/sql-catalyst-optimizer.html)