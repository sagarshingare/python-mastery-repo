"""Comprehensive test suite for Stage 06: Distributed Big Data (PySpark)."""

from __future__ import annotations

import os
import tempfile
from typing import Generator

import pytest

from pyspark.basics.spark_basics import (
    HAS_PYSPARK,
    create_dataframe_from_dict,
    create_dataframe_from_list,
    create_spark_session,
    define_custom_schema,
    filter_dataframe,
    inspect_dataframe,
    sample_data,
    select_columns,
    stop_spark_session,
)
from pyspark.transformations.transformations import (
    apply_map_transformation,
    apply_window_analytics,
    apply_window_function,
    broadcast_join,
    derive_columns,
    filter_greater_than,
    group_and_aggregate,
    join_dataframes,
    union_dataframes,
)
from pyspark.actions.actions import (
    collect_data,
    count_rows,
    get_first_row,
    get_statistics,
    read_storage,
    summarize_dataframe,
    take_rows,
    write_csv,
    write_json,
    write_parquet,
    write_partitioned,
)
from pyspark.interview_questions.pyspark_interview import (
    Architecture_Tradeoffs,
    Coding_Problems,
    Memory_Management,
    Most_Asked_Questions,
    Partitioning_Strategy,
    Performance_Tuning,
    PySpark_Fundamentals,
)


@pytest.fixture(scope="module")
def spark() -> Generator[object, None, None]:
    """Module-scoped SparkSession fixture ensuring single startup and clean teardown."""
    if not HAS_PYSPARK:
        pytest.skip("PySpark is not installed in the active environment.")

    session = create_spark_session("PySpark-Pytest-Suite")
    yield session
    stop_spark_session(session)


# ==============================================================================
# Step 6.1: Spark Basics Tests
# ==============================================================================

class TestSparkBasics:
    """Test suite for SparkSession, Schema, and DataFrame ingestion basics."""

    def test_spark_session_lifecycle(self, spark: object) -> None:
        assert spark is not None
        assert spark.sparkContext.appName == "PySpark-Pytest-Suite"
        assert spark.sparkContext.master.startswith("local")

    def test_define_custom_schema(self) -> None:
        schema = define_custom_schema()
        field_names = [f.name for f in schema.fields]
        assert field_names == ["id", "name", "department", "salary"]
        assert schema["id"].dataType.simpleString() == "int"
        assert schema["name"].dataType.simpleString() == "string"
        assert schema["salary"].dataType.simpleString() == "double"

    def test_create_dataframe_from_list(self, spark: object) -> None:
        schema = define_custom_schema()
        data = sample_data()
        df = create_dataframe_from_list(spark, data, schema=schema)
        assert df is not None
        assert df.count() == 5
        assert len(df.columns) == 4

    def test_create_dataframe_from_dict(self, spark: object) -> None:
        records = [
            {"id": 1, "product": "Laptop", "price": 1200.0},
            {"id": 2, "product": "Mouse", "price": 25.0},
        ]
        df = create_dataframe_from_dict(spark, records)
        assert df is not None
        assert df.count() == 2
        assert "price" in df.columns

    def test_inspect_dataframe(self, spark: object) -> None:
        df = create_dataframe_from_list(spark, sample_data(), define_custom_schema())
        stats = inspect_dataframe(df)
        assert stats["row_count"] == 5
        assert stats["column_count"] == 4
        assert "department" in stats["columns"]
        assert any(col_name == "salary" and dtype == "double" for col_name, dtype in stats["dtypes"])

    def test_filter_and_select(self, spark: object) -> None:
        df = create_dataframe_from_list(spark, sample_data(), define_custom_schema())
        filtered = filter_dataframe(df, "salary >= 100000")
        assert filtered is not None
        assert filtered.count() == 2

        selected = select_columns(filtered, ["name", "salary"])
        assert selected is not None
        assert selected.columns == ["name", "salary"]


# ==============================================================================
# Step 6.2: Spark Transformations Tests
# ==============================================================================

class TestSparkTransformations:
    """Test suite for narrow vs wide transformations, broadcast joins, and windowing."""

    @pytest.fixture
    def employee_df(self, spark: object) -> object:
        data = [
            (1, "Alice", "Engineering", 95000.0),
            (2, "Bob", "Marketing", 62000.0),
            (3, "Charlie", "Engineering", 110000.0),
            (4, "Diana", "Product", 88000.0),
            (5, "Evan", "Engineering", 105000.0),
            (6, "Fiona", "Marketing", 75000.0),
        ]
        return spark.createDataFrame(data, ["id", "name", "dept", "salary"])

    @pytest.fixture
    def department_df(self, spark: object) -> object:
        data = [
            ("Engineering", "Building A", "Tech"),
            ("Marketing", "Building B", "Business"),
            ("Product", "Building A", "Product"),
        ]
        return spark.createDataFrame(data, ["dept", "location", "division"])

    def test_derive_columns(self, employee_df: object) -> None:
        derived = derive_columns(employee_df)
        assert derived is not None
        assert "bonus" in derived.columns
        assert "total_comp" in derived.columns
        assert "tier" in derived.columns

        first_row = derived.filter("id = 1").first()
        assert first_row["bonus"] == 9500.0
        assert first_row["total_comp"] == 104500.0
        assert first_row["tier"] == "Senior"

    def test_filter_greater_than(self, employee_df: object) -> None:
        filtered = filter_greater_than(employee_df, "salary", 100000.0)
        assert filtered is not None
        assert filtered.count() == 2

    def test_group_and_aggregate(self, employee_df: object) -> None:
        agg_sum = group_and_aggregate(employee_df, "dept", "salary", "sum")
        assert agg_sum is not None
        eng_sum = agg_sum.filter("dept = 'Engineering'").first()["sum_salary"]
        assert eng_sum == 310000.0

        agg_avg = group_and_aggregate(employee_df, "dept", "salary", "avg")
        assert agg_avg is not None
        assert "avg_salary" in agg_avg.columns

    def test_standard_and_broadcast_joins(self, employee_df: object, department_df: object) -> None:
        joined = join_dataframes(employee_df, department_df, join_key="dept", how="inner")
        assert joined is not None
        assert joined.count() == 6
        assert "location" in joined.columns

        broadcasted = broadcast_join(employee_df, department_df, join_key="dept", how="left")
        assert broadcasted is not None
        assert broadcasted.count() == 6

    def test_window_ranking_and_analytics(self, employee_df: object) -> None:
        ranked = apply_window_function(employee_df, partition_col="dept", order_col="salary")
        assert ranked is not None
        assert "rank" in ranked.columns

        # Charlie (110000.0) should be rank 1 in Engineering
        charlie_rank = ranked.filter("name = 'Charlie'").first()["rank"]
        assert charlie_rank == 1

        analytics = apply_window_analytics(employee_df, partition_col="dept", order_col="salary", value_col="salary")
        assert analytics is not None
        assert "dense_rank" in analytics.columns
        assert "running_total" in analytics.columns

    def test_union_dataframes(self, spark: object) -> None:
        df1 = spark.createDataFrame([(1, "A")], ["id", "val"])
        df2 = spark.createDataFrame([(2, "B")], ["id", "val"])
        unioned = union_dataframes(df1, df2)
        assert unioned is not None
        assert unioned.count() == 2


# ==============================================================================
# Step 6.3: Spark Actions & Sinks Tests
# ==============================================================================

class TestSparkActions:
    """Test suite for eager actions, statistical summary, and storage sinks."""

    @pytest.fixture
    def sample_action_df(self, spark: object) -> object:
        data = [
            (1, "Alice", 95000.0, "Engineering"),
            (2, "Bob", 62000.0, "Marketing"),
            (3, "Charlie", 110000.0, "Engineering"),
            (4, "Diana", 88000.0, "Product"),
        ]
        return spark.createDataFrame(data, ["id", "name", "salary", "dept"])

    def test_action_retrievals(self, sample_action_df: object) -> None:
        assert count_rows(sample_action_df) == 4
        first = get_first_row(sample_action_df)
        assert first is not None
        assert first[0] == 1

        top2 = take_rows(sample_action_df, 2)
        assert len(top2) == 2

        collected = collect_data(sample_action_df)
        assert len(collected) == 4
        assert isinstance(collected[0], tuple)

    def test_summarize_dataframe(self, sample_action_df: object) -> None:
        summary = summarize_dataframe(sample_action_df)
        assert summary is not None
        assert summary.count() > 0
        summary_metrics = [r["summary"] for r in summary.select("summary").collect()]
        assert "count" in summary_metrics
        assert "mean" in summary_metrics

    def test_storage_writes_and_partitioning(self, spark: object, sample_action_df: object) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Parquet write
            p_path = os.path.join(tmpdir, "test.parquet")
            assert write_parquet(sample_action_df, p_path) is True
            assert os.path.exists(p_path)

            # 2. CSV write
            c_path = os.path.join(tmpdir, "test.csv")
            assert write_csv(sample_action_df, c_path) is True
            assert os.path.exists(c_path)

            # 3. JSON write
            j_path = os.path.join(tmpdir, "test.json")
            assert write_json(sample_action_df, j_path) is True
            assert os.path.exists(j_path)

            # 4. Partitioned write & read-back
            part_path = os.path.join(tmpdir, "partitioned")
            assert write_partitioned(sample_action_df, part_path, partition_cols=["dept"], file_format="parquet") is True
            assert os.path.exists(os.path.join(part_path, "dept=Engineering"))

            reloaded = read_storage(spark, part_path, file_format="parquet")
            assert reloaded is not None
            assert reloaded.count() == 4
            assert "dept" in reloaded.columns


# ==============================================================================
# Step 6.4: Spark Interview Questions & Optimization Tests
# ==============================================================================

class TestSparkInterviewQuestions:
    """Test suite for Spark architecture knowledge models and problem explanations."""

    def test_catalyst_optimizer_stages(self) -> None:
        catalyst = PySpark_Fundamentals.catalyst_optimizer()
        assert "stages" in catalyst
        assert any("Logical Plan" in stage or "Parsing" in stage for stage in catalyst["stages"])
        assert "predicate_pushdown" in catalyst["key_optimizations"]

    def test_shuffle_and_partitioning_strategies(self) -> None:
        shuffle = PySpark_Fundamentals.shuffle_explain()
        assert "groupBy()" in shuffle["shuffle_operations"]
        assert "join()" in shuffle["shuffle_operations"]

        part = Partitioning_Strategy.optimal_partition_count()
        assert "formula" in part
        assert "guidelines" in part
        assert "data_size_rule" in part["guidelines"]

    def test_memory_management_caching(self) -> None:
        mem = Memory_Management.caching_strategy()
        assert "storage_levels" in mem
        assert "MEMORY_AND_DISK" in mem["storage_levels"]

    def test_most_asked_and_coding_problems(self) -> None:
        q_lazy = Most_Asked_Questions.q1_what_is_lazy_evaluation()
        assert "question" in q_lazy
        assert "answer" in q_lazy
        assert "Transformations" in q_lazy["answer"]

        prob1 = Coding_Problems.problem_1_top_n_salary()
        assert "solution" in prob1
        assert "Window.partitionBy" in prob1["solution"]

        prob4 = Coding_Problems.problem_4_cumulative_sum()
        assert "solution" in prob4
        assert "cumulative_sum" in prob4["solution"]

    def test_performance_tuning_explain(self) -> None:
        tuning = Performance_Tuning.explain_plan()
        assert "output_sections" in tuning
        assert "what_to_look_for" in tuning

    def test_table_formats_iceberg_vs_delta_vs_hudi(self) -> None:
        tradeoffs = Architecture_Tradeoffs.table_formats_iceberg_vs_delta_vs_hudi()
        assert "formats" in tradeoffs
        assert "Apache_Iceberg" in tradeoffs["formats"]
        assert "Delta_Lake" in tradeoffs["formats"]
        assert "Apache_Hudi" in tradeoffs["formats"]

        # Iceberg hidden partitioning and metadata
        iceberg = tradeoffs["formats"]["Apache_Iceberg"]
        assert "Hidden Partitioning" in iceberg["partitioning"]
        assert "Snapshot Tree" in iceberg["metadata_architecture"]

        # Delta transaction log
        delta = tradeoffs["formats"]["Delta_Lake"]
        assert "Transaction Log" in delta["metadata_architecture"]

        # Decision matrix
        matrix = tradeoffs["decision_matrix"]
        assert "choose_iceberg_when" in matrix
        assert "choose_delta_when" in matrix
        assert "choose_hudi_when" in matrix

    def test_file_formats_parquet_vs_orc_vs_avro(self) -> None:
        ff = Architecture_Tradeoffs.file_formats_parquet_vs_orc_vs_avro()
        assert "Parquet" in ff["formats"]
        assert "ORC" in ff["formats"]
        assert "Avro" in ff["formats"]
        assert "Dremel" in str(ff["formats"]["Parquet"]["strengths"])
        assert "Row-oriented" in ff["formats"]["Avro"]["layout"]

    def test_repartition_vs_coalesce_tradeoffs(self) -> None:
        rc = Architecture_Tradeoffs.repartition_vs_coalesce()
        assert "repartition" in rc["comparison"]
        assert "coalesce" in rc["comparison"]
        assert "shuffle" in rc["comparison"]["repartition"]
        assert "interview_trap" in rc

    def test_join_strategies_tradeoffs(self) -> None:
        joins = Architecture_Tradeoffs.join_strategies_tradeoffs()
        assert "Broadcast_Hash_Join_BHJ" in joins["strategies"]
        assert "Sort_Merge_Join_SMJ" in joins["strategies"]
        assert "salting" in joins["skew_mitigation"]

    def test_lakehouse_medallion_tradeoffs(self) -> None:
        medallion = Architecture_Tradeoffs.lakehouse_medallion_tradeoffs()
        assert "Bronze_Raw" in medallion["layers"]
        assert "Silver_Cleansed" in medallion["layers"]
        assert "Gold_Aggregated" in medallion["layers"]
        assert "storage_cost_vs_reprocessing" in medallion["architectural_tradeoffs"]
