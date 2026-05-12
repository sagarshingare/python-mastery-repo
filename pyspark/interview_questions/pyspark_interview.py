"""PySpark interview questions and coding problems.

This module covers common PySpark interview questions, most asked questions,
and LeetCode-style problems with detailed solutions and explanations.

Topics covered:
- RDDs vs DataFrames
- Partitioning and optimization
- Memory management and caching
- Spark SQL and DataFrame operations
- Streaming and real-time processing
- Performance tuning
- Distributed computing concepts

Python version: 3.9+
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


# ============================================================================
# FUNDAMENTAL CONCEPTS
# ============================================================================

class PySpark_Fundamentals:
    """Fundamental PySpark concepts and architecture."""
    
    @staticmethod
    def rdd_vs_dataframe() -> Dict[str, str]:
        """RDD vs DataFrame - Key differences and when to use each.
        
        Returns:
            Dictionary with comparison details.
        """
        return {
            "concept": "RDD vs DataFrame",
            "explanation": """
                RDD (Resilient Distributed Dataset):
                - Low-level abstraction
                - Untyped, not optimized
                - Good for unstructured data
                - Slower performance
                - Use when: Unstructured data, complex transformations
                
                DataFrame:
                - High-level abstraction
                - Typed schema, optimized by Catalyst
                - Best for structured data
                - Better performance
                - Use when: Structured data, SQL queries, production systems
            """,
            "performance_difference": "DataFrames 10-100x faster due to Catalyst optimizer",
            "code_example": """
                # RDD approach (slower)
                rdd = sc.textFile("data.txt")
                result = rdd.map(lambda x: x.split(",")).filter(lambda x: x[1] > "50000")
                
                # DataFrame approach (faster)
                df = spark.read.csv("data.txt", header=True)
                result = df.filter(col("salary") > 50000)
            """
        }
    
    @staticmethod
    def catalyst_optimizer() -> Dict[str, str]:
        """Catalyst Optimizer - How Spark optimizes queries.
        
        Returns:
            Dictionary with optimization strategies.
        """
        return {
            "concept": "Catalyst Optimizer",
            "stages": [
                "1. Parsing: Convert SQL to logical plan",
                "2. Validation: Check schema and expressions",
                "3. Optimization: Apply optimization rules (predicate pushdown, etc.)",
                "4. Physical Planning: Choose optimal execution strategy",
                "5. Code Generation: Generate optimized code"
            ],
            "key_optimizations": {
                "predicate_pushdown": "Push filters down to data source",
                "projection_pushdown": "Select only needed columns early",
                "constant_folding": "Pre-compute constant expressions",
                "boolean_simplification": "Simplify boolean logic",
                "null_propagation": "Handle NULL values efficiently"
            },
            "best_practice": "Use DataFrames and Spark SQL for automatic optimization"
        }
    
    @staticmethod
    def shuffle_explain() -> Dict[str, Any]:
        """Understanding Spark Shuffle - Performance impact.
        
        Returns:
            Dictionary with shuffle explanation.
        """
        return {
            "concept": "Spark Shuffle",
            "definition": "Redistribution of data across partitions during wide transformations",
            "shuffle_operations": [
                "groupBy()", "reduceByKey()", "join()", "repartition()",
                "coalesce()", "sortByKey()", "distinct()"
            ],
            "performance_impact": {
                "issue": "Very expensive operation - network I/O",
                "solution": "Minimize shuffles through careful query design",
                "techniques": [
                    "Use map/filter before reduce",
                    "Partition input data strategically",
                    "Use broadcast join for small DataFrames",
                    "Combine operations to reduce shuffles"
                ]
            },
            "example": """
                # EXPENSIVE - causes shuffle
                df.groupBy("category").count()
                
                # Use broadcast for join if possible
                small_df.broadcast()
                large_df.join(small_df, "id")
            """
        }


# ============================================================================
# PARTITIONING AND OPTIMIZATION
# ============================================================================

class Partitioning_Strategy:
    """Partitioning strategies and optimization techniques."""
    
    @staticmethod
    def optimal_partition_count() -> Dict[str, Any]:
        """How to calculate optimal partition count.
        
        Returns:
            Dictionary with partitioning guidelines.
        """
        return {
            "concept": "Optimal Partition Count",
            "formula": "number_of_cores * 2 to 4",
            "guidelines": {
                "typical_cluster": "For 8 cores cluster: 16-32 partitions",
                "data_size_rule": "Aim for 128MB per partition",
                "too_few": "Underutilizes cores, slow processing",
                "too_many": "Too much overhead, GC pressure",
                "sweet_spot": "1 task per core is ideal"
            },
            "calculation_example": """
                # Data size: 10GB, Target partition size: 128MB
                optimal_partitions = 10000 / 128 = ~78 partitions
                
                # Implementation
                df.repartition(78)
            """
        }
    
    @staticmethod
    def bucketing_advantage() -> Dict[str, str]:
        """Bucketing - When and why to use it.
        
        Returns:
            Dictionary with bucketing details.
        """
        return {
            "concept": "Bucketing in Spark",
            "definition": "Pre-partition data into fixed number of buckets based on hash",
            "advantages": [
                "Faster joins on bucketted columns",
                "Faster aggregations",
                "Reduced shuffles",
                "Better memory utilization"
            ],
            "when_to_use": [
                "Frequently joined on same column",
                "Data doesn't change frequently",
                "DataFrame size > 100GB",
                "Multiple joins with same keys"
            ],
            "implementation": """
                # Create bucketed table
                df.write \\
                    .bucketBy(10, "id") \\
                    .mode("overwrite") \\
                    .option("path", "/path/to/data") \\
                    .saveAsTable("bucketed_table")
                
                # Benefits: Joins now use bucket matching, no shuffle
                df1.join(df2, "id")  # Uses bucketed join
            """
        }


# ============================================================================
# MEMORY AND CACHING
# ============================================================================

class Memory_Management:
    """Memory management, caching, and performance tuning."""
    
    @staticmethod
    def caching_strategy() -> Dict[str, Any]:
        """Caching strategy and storage levels.
        
        Returns:
            Dictionary with caching guidance.
        """
        return {
            "concept": "DataFrame Caching",
            "when_to_cache": [
                "DataFrame used multiple times",
                "Expensive transformation result",
                "Before groupBy or join operations",
                "Intermediate results in ETL"
            ],
            "storage_levels": {
                "MEMORY_ONLY": "Fastest, but may spill",
                "MEMORY_AND_DISK": "Fallback to disk if memory full",
                "DISK_ONLY": "For very large DataFrames",
                "MEMORY_ONLY_2": "Replicate across 2 nodes"
            },
            "implementation": """
                from pyspark.storagelevel import StorageLevel
                
                # Cache in memory
                df.cache()
                df.persist()
                
                # Specific storage level
                df.persist(StorageLevel.MEMORY_AND_DISK)
                
                # Remove from cache
                df.unpersist()
            """,
            "gotchas": [
                "Cache uses memory - monitor usage",
                "Not all operations benefit from caching",
                "Check if cached before first action",
                "Clear cache when no longer needed"
            ]
        }
    
    @staticmethod
    def broadcast_vs_shuffle() -> Dict[str, Any]:
        """Broadcast join vs Shuffle join.
        
        Returns:
            Dictionary with join strategy comparison.
        """
        return {
            "concept": "Join Strategies",
            "broadcast_join": {
                "usage": "Small DataFrame < 2GB",
                "advantage": "No shuffle needed, very fast",
                "cost": "Memory on all executors",
                "implementation": """
                    from pyspark.sql.functions import broadcast
                    
                    large_df.join(broadcast(small_df), "id")
                """
            },
            "shuffle_join": {
                "usage": "Both DataFrames large",
                "advantage": "Works with large datasets",
                "cost": "Network I/O, slower",
                "implementation": """
                    large_df1.join(large_df2, "id")
                    # Automatically uses shuffle join
                """
            },
            "performance_comparison": {
                "broadcast": "10-100MB small table: << 1 second",
                "shuffle": "Same data: 10-100 seconds"
            }
        }


# ============================================================================
# MOST ASKED INTERVIEW QUESTIONS
# ============================================================================

class Most_Asked_Questions:
    """Most commonly asked PySpark interview questions with solutions."""
    
    @staticmethod
    def q1_what_is_lazy_evaluation() -> Dict[str, str]:
        """Q1: Explain lazy evaluation in Spark.
        
        Returns:
            Dictionary with question and answer.
        """
        return {
            "question": "What is lazy evaluation and why does Spark use it?",
            "answer": """
                Lazy evaluation means Spark doesn't compute transformations until an action is called.
                
                Transformations: map(), filter(), groupBy(), join() - not executed
                Actions: collect(), count(), save(), show() - trigger execution
                
                Benefits:
                1. Optimization opportunity - Catalyst can optimize entire pipeline
                2. Resource efficiency - only compute what's needed
                3. Fault tolerance - can recompute if needed
                4. Reduced memory - doesn't materialize intermediate results
            """,
            "code_example": """
                # These don't execute
                df_filtered = df.filter(col("age") > 30)  # Transformation
                df_mapped = df_filtered.map(lambda x: x.name)  # Transformation
                
                # This triggers execution
                result = df_mapped.collect()  # Action - NOW it computes
                
                # Check query plan
                df.explain()  # Shows logical and physical plans
            """
        }
    
    @staticmethod
    def q2_dataframe_vs_rdd() -> Dict[str, str]:
        """Q2: When would you use RDD vs DataFrame?
        
        Returns:
            Dictionary with comparison.
        """
        return {
            "question": "When would you use RDD instead of DataFrame?",
            "answer": """
                Use RDD when:
                1. Working with unstructured data
                2. Need low-level transformations
                3. Data doesn't fit schema
                4. Complex custom operations
                
                Use DataFrame when:
                1. Structured/semi-structured data
                2. Need SQL queries
                3. Want Catalyst optimization
                4. Production systems (better performance)
            """,
            "code_example": """
                # RDD - for unstructured
                rdd = sc.textFile("raw_logs.txt")
                result = rdd.map(parse_custom_format).filter(condition)
                
                # DataFrame - for structured
                df = spark.read.json("events.json")
                result = df.filter(col("status") == "error").groupBy("type").count()
            """
        }
    
    @staticmethod
    def q3_memory_issues() -> Dict[str, str]:
        """Q3: How to handle out of memory issues in Spark?
        
        Returns:
            Dictionary with solutions.
        """
        return {
            "question": "Your Spark job throws OutOfMemoryError. How do you fix it?",
            "answer": """
                Solutions in order of effectiveness:
                1. Increase executor memory
                2. Increase number of partitions (smaller per-partition)
                3. Use broadcast join instead of shuffle join
                4. Cache strategically (only what's needed multiple times)
                5. Use columnar compression (Parquet, ORC)
                6. Use Delta Lake for better memory usage
                7. Repartition/coalesce to control memory
            """,
            "code_example": """
                # Configuration
                spark = SparkSession.builder \\
                    .config("spark.executor.memory", "8g") \\
                    .config("spark.driver.memory", "4g") \\
                    .config("spark.sql.shuffle.partitions", "200") \\
                    .getOrCreate()
                
                # Repartition
                df = df.repartition(500)  # More partitions = smaller chunks
                
                # Use broadcast for small table
                from pyspark.sql.functions import broadcast
                result = large_df.join(broadcast(small_df), "id")
            """
        }
    
    @staticmethod
    def q4_skewed_data() -> Dict[str, str]:
        """Q4: How to handle skewed data?
        
        Returns:
            Dictionary with skew handling techniques.
        """
        return {
            "question": "What is data skew and how do you handle it?",
            "answer": """
                Data skew = some partitions have much more data than others.
                
                Impact: Stragglers - few tasks much slower than others, bottleneck.
                
                Solutions:
                1. Add salt to unbalanced keys
                2. Use adaptive query execution
                3. Increase partitions
                4. Use Salting + repartitioning
                5. Use explode() to spread data
            """,
            "code_example": """
                from pyspark.sql.functions import concat, lit, rand
                
                # Problem: join on skewed key 'category'
                # Category 'Other' has 80% of data
                
                # Solution: Salting
                salt = (rand() * 10).cast("int")
                df_salted = df.withColumn("salt_key", concat(col("category"), lit("_"), salt))
                
                # Now join uses salted keys - better distribution
                result = df1.join(df2, "salt_key")
            """
        }
    
    @staticmethod
    def q5_join_performance() -> Dict[str, str]:
        """Q5: How to optimize join operations?
        
        Returns:
            Dictionary with join optimization tips.
        """
        return {
            "question": "How do you optimize Spark join operations?",
            "answer": """
                Join optimization strategies:
                1. Use broadcast join for small tables (< 2GB)
                2. Pre-filter before join (predicate pushdown)
                3. Use correct join type (inner vs outer)
                4. Sort and bucket keys before join
                5. Avoid multiple joins in same query
                6. Use columnar format (Parquet)
                7. Repartition on join key
            """,
            "code_example": """
                from pyspark.sql.functions import broadcast, col
                
                # Optimized join
                df_filtered = df_large.filter(col("active") == True)
                
                if df_small.count() < 100_000_000:  # < ~2GB
                    result = df_filtered.join(broadcast(df_small), "id", "inner")
                else:
                    # Pre-repartition for shuffle join
                    df1_part = df_filtered.repartition(200, "id")
                    df2_part = df_small.repartition(200, "id")
                    result = df1_part.join(df2_part, "id", "inner")
            """
        }


# ============================================================================
# LEETCODE-STYLE PROBLEMS
# ============================================================================

class Coding_Problems:
    """LeetCode-style coding problems with PySpark solutions."""
    
    @staticmethod
    def problem_1_top_n_salary() -> Dict[str, Any]:
        """Problem 1: Find top N salaries by department.
        
        Returns:
            Dictionary with problem and solution.
        """
        return {
            "problem": "Find top N earners in each department",
            "description": """
                Given a dataset with columns: employee_id, name, salary, department.
                Find the top 3 earners in each department.
                
                Expected output: department, name, salary, rank_in_dept
            """,
            "solution": """
                from pyspark.sql import Window
                from pyspark.sql.functions import col, row_number, rank, dense_rank
                
                # Window function approach
                window_spec = Window.partitionBy("department").orderBy(col("salary").desc())
                
                result = df.withColumn(
                    "rank",
                    row_number().over(window_spec)
                ).filter(col("rank") <= 3)
                
                # Alternative using rank (handles ties)
                result = df.withColumn(
                    "rank",
                    rank().over(window_spec)
                ).filter(col("rank") <= 3)
            """,
            "time_complexity": "O(n log n) - due to sorting",
            "space_complexity": "O(n) - for window state"
        }
    
    @staticmethod
    def problem_2_duplicate_emails() -> Dict[str, Any]:
        """Problem 2: Find duplicate emails.
        
        Returns:
            Dictionary with problem and solution.
        """
        return {
            "problem": "Find duplicate emails in a dataset",
            "description": """
                Given a dataset with columns: id, email.
                Find all emails that appear more than once.
                
                Expected output: email
            """,
            "solution": """
                # Approach 1: GroupBy
                result = df.groupBy("email") \\
                    .count() \\
                    .filter(col("count") > 1) \\
                    .select("email")
                
                # Approach 2: Window function
                from pyspark.sql.functions import count
                window_spec = Window.partitionBy("email")
                
                result = df.withColumn("cnt", count("*").over(window_spec)) \\
                    .filter(col("cnt") > 1) \\
                    .select("email").distinct()
            """,
            "time_complexity": "O(n) - single pass with groupBy",
            "space_complexity": "O(k) - where k is unique emails"
        }
    
    @staticmethod
    def problem_3_second_highest_salary() -> Dict[str, Any]:
        """Problem 3: Find second highest salary.
        
        Returns:
            Dictionary with problem and solution.
        """
        return {
            "problem": "Find the second highest salary",
            "description": """
                Given a salary table with columns: id, salary.
                Find the second highest unique salary.
                If no second highest exists, return null.
            """,
            "solution": """
                # Approach 1: Using window function
                from pyspark.sql.functions import row_number, col
                from pyspark.sql import Window
                
                window = Window.orderBy(col("salary").desc())
                result = df.select("salary").distinct() \\
                    .withColumn("rank", row_number().over(window)) \\
                    .filter(col("rank") == 2) \\
                    .select("salary")
                
                # Approach 2: Using offset and limit
                result = df.select("salary").distinct() \\
                    .orderBy(col("salary").desc()) \\
                    .limit(2) \\
                    .tail(1)[0][0]  # Get second element
            """,
            "edge_cases": [
                "No salary data",
                "Only one unique salary",
                "Multiple employees with same salary"
            ]
        }
    
    @staticmethod
    def problem_4_cumulative_sum() -> Dict[str, Any]:
        """Problem 4: Calculate cumulative sum.
        
        Returns:
            Dictionary with problem and solution.
        """
        return {
            "problem": "Calculate cumulative sum over time",
            "description": """
                Given transactions with columns: id, date, amount.
                Calculate running total (cumulative sum) ordered by date.
            """,
            "solution": """
                from pyspark.sql.functions import sum as spark_sum, col
                from pyspark.sql import Window
                
                # Cumulative sum window
                window = Window.orderBy("date") \\
                    .rangeBetween(Window.unboundedPreceding, Window.currentRow)
                
                result = df.withColumn(
                    "cumulative_sum",
                    spark_sum("amount").over(window)
                )
            """,
            "time_complexity": "O(n log n) - window operation",
            "use_cases": ["Running total", "Cumulative metrics", "Time series analysis"]
        }
    
    @staticmethod
    def problem_5_top_k_frequent() -> Dict[str, Any]:
        """Problem 5: Find top K frequent elements.
        
        Returns:
            Dictionary with problem and solution.
        """
        return {
            "problem": "Find top K most frequent elements",
            "description": """
                Given a list of elements, find the top K most frequent ones.
                Example: [1,1,1,2,2,3] with K=2 -> [1,2]
            """,
            "solution": """
                from pyspark.sql.functions import col, count
                
                # Approach 1: GroupBy and sort
                result = df.groupBy("element") \\
                    .count() \\
                    .orderBy(col("count").desc()) \\
                    .limit(K) \\
                    .select("element")
                
                # Approach 2: Using RDD (if needed)
                rdd = sc.parallelize([1,1,1,2,2,3])
                result = rdd.map(lambda x: (x, 1)) \\
                    .reduceByKey(lambda a, b: a + b) \\
                    .sortBy(lambda x: x[1], ascending=False) \\
                    .take(K)
            """,
            "time_complexity": "O(n log k) - heap-based approach optimal",
            "space_complexity": "O(k)"
        }


# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

class Performance_Tuning:
    """Performance tuning and optimization techniques."""
    
    @staticmethod
    def sql_vs_dataframe() -> Dict[str, str]:
        """SQL vs DataFrame API - Which is faster?
        
        Returns:
            Dictionary with comparison.
        """
        return {
            "concept": "SQL vs DataFrame API",
            "answer": """
                They compile to same Catalyst plan, so SAME PERFORMANCE.
                
                Use SQL when:
                - Complex queries
                - Team knows SQL well
                - SQL is readable for your case
                
                Use DataFrame when:
                - Complex programmatic logic
                - Multiple conditional branches
                - Working with Python developers
                
                Both go through Catalyst optimizer, so pick for readability.
            """,
            "example": """
                # Same query - same performance
                # SQL
                df.createOrReplaceTempView("sales")
                result = spark.sql('''
                    SELECT department, SUM(amount) as total
                    FROM sales
                    WHERE year = 2024
                    GROUP BY department
                ''')
                
                # DataFrame API
                result = df.filter(col("year") == 2024) \\
                    .groupBy("department") \\
                    .agg(sum("amount").alias("total"))
            """
        }
    
    @staticmethod
    def explain_plan() -> Dict[str, str]:
        """Understanding Spark explain() output.
        
        Returns:
            Dictionary with explain guidance.
        """
        return {
            "concept": "Reading Spark Explain Plans",
            "output_sections": {
                "Parsed Logical Plan": "How Spark parsed the SQL",
                "Analyzed Logical Plan": "After analyzing for correctness",
                "Optimized Logical Plan": "After Catalyst optimizations",
                "Physical Plan": "Actual execution plan"
            },
            "what_to_look_for": [
                "Unnecessary shuffles",
                "Filter operations (should be early)",
                "Join types (broadcast vs shuffle)",
                "Predicates (should be pushed down)",
                "Aggregations (single vs multiple stages)"
            ],
            "usage": """
                # See logical and physical plans
                df.explain()  # Shows all 4 stages
                df.explain(True)  # Same as above
                df.explain(False)  # Physical plan only
                
                # Check explain plan to identify bottlenecks
            """
        }