"""Comprehensive test suite for Data Analytics & Scientific Libraries (Stage 05).

Covers:
- Step 5.1: NumPy Fundamentals (Arrays, Broadcasting, Vectorization, Optimization)
- Step 5.2: Pandas Tabular Data (Basics, GroupBy, Joins, Window Functions, Optimization)
- Step 5.3: Statistical Analysis (Descriptive, Distributions, Hypothesis Testing, Regression)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

# NumPy Submodules
from numpy_lib.arrays import (
    batch_dot,
    create_grid,
    filter_by_mask,
    flatten_array,
    matrix_properties,
    normalize_vector,
    replace_outliers,
    reshape_array,
    slice_submatrix,
    split_array,
    stack_arrays,
)
from numpy_lib.broadcasting import (
    center_and_scale,
    check_broadcast_compatibility,
    expand_dimension,
    outer_product_grid,
    pairwise_euclidean_distance,
)
from numpy_lib.optimization import (
    compute_in_place,
    inspect_memory_layout,
    optimize_numeric_dtypes,
    verify_view_vs_copy,
)
from numpy_lib.vectorization import (
    benchmark_loop_vs_vectorized,
    categorize_values,
    compute_moving_window_diff,
    cumulative_drawdown,
    relu,
    sigmoid,
)

# Pandas Submodules
from pandas_lib.basics import (
    clean_sales_data,
    extract_datetime_features,
    handle_missing_values,
    transform_string_columns,
)
from pandas_lib.groupby import (
    aggregate_sales_by_department,
    calculate_group_zscore,
    calculate_percentage_of_group_total,
    create_pivot_sales_summary,
    filter_high_volume_groups,
)
from pandas_lib.joins import (
    concatenate_dataframes,
    join_on_index,
    merge_asof_timestamps,
    perform_relational_merge,
    validate_cardinality_merge,
)
from pandas_lib.optimization import (
    benchmark_vectorized_vs_apply,
    chunk_dataframe,
    get_memory_usage_report,
    optimize_dtypes,
)
from pandas_lib.window_functions import (
    calculate_expanding_metrics,
    calculate_exponential_moving_average,
    calculate_lag_and_returns,
    calculate_partitioned_ranks,
    calculate_rolling_metrics,
)

# Statistics Submodules
from statistics.descriptive import (
    compute_bivariate_metrics,
    compute_percentiles,
    describe_series,
    detect_iqr_outliers,
    z_score,
)
from statistics.distributions import (
    binomial_distribution_metrics,
    evaluate_normality_ks,
    exponential_distribution_metrics,
    normal_distribution_metrics,
    poisson_distribution_metrics,
)
from statistics.hypothesis_testing import (
    chi_square_test_of_independence,
    mann_whitney_u_test,
    one_sample_t_test,
    one_way_anova,
    paired_t_test,
    two_sample_t_test,
)
from statistics.regression import (
    multiple_linear_regression,
    predict_linear,
    simple_linear_regression,
)


# ============================================================================
# STEP 5.1: NUMPY FUNDAMENTALS TESTS
# ============================================================================

def test_numpy_arrays_operations() -> None:
    # Coordinate grid
    grid = create_grid(rows=5, cols=5, step=1.0)
    assert grid.shape == (5, 5, 2)

    # Reshaping and flattening
    arr = np.arange(12)
    reshaped = reshape_array(arr, (3, 4))
    assert reshaped.shape == (3, 4)
    flat_c = flatten_array(reshaped, copy=False)
    assert flat_c.shape == (12,)

    # Slicing
    submat = slice_submatrix(reshaped, row_start=0, row_end=2, col_start=1, col_end=3)
    assert submat.shape == (2, 2)

    # Stacking and splitting
    a = np.ones((2, 3))
    b = np.full((2, 3), 2.0)
    vstacked = stack_arrays(a, b, direction="vertical")
    assert vstacked.shape == (4, 3)
    splits = split_array(vstacked, num_sections=2, axis=0)
    assert len(splits) == 2

    # Masking and outliers
    vals = np.array([10, 25, 40, 55, 70])
    filtered = filter_by_mask(vals, (vals >= 30) & (vals <= 60))
    assert filtered.tolist() == [40, 55]
    replaced = replace_outliers(vals, lower_bound=20, upper_bound=60, fill_value=0)
    assert replaced.tolist() == [0, 25, 40, 55, 0]

    # Vector and matrix metrics
    vec = np.array([3.0, 4.0])
    norm = normalize_vector(vec)
    assert np.linalg.norm(norm) == pytest.approx(1.0)

    mat = np.array([[3.0, 1.0], [1.0, 2.0]])
    props = matrix_properties(mat)
    assert props["determinant"] == pytest.approx(5.0)
    assert props["trace"] == pytest.approx(5.0)
    assert props["norm"] > 0


def test_numpy_broadcasting_and_distance() -> None:
    # Rules
    compat, shape = check_broadcast_compatibility((3, 1), (3, 4))
    assert compat is True
    assert shape == (3, 4)

    compat_f, _ = check_broadcast_compatibility((3, 2), (3, 4))
    assert compat_f is False

    # Expanding
    arr_1d = np.array([1, 2, 3])
    expanded = expand_dimension(arr_1d, axis=1)
    assert expanded.shape == (3, 1)

    # Feature scaling
    raw_feats = np.array([[10.0, 200.0], [20.0, 400.0], [30.0, 600.0]])
    scaled, mean, std = center_and_scale(raw_feats)
    assert np.allclose(scaled.mean(axis=0), 0.0)
    assert np.allclose(scaled.std(axis=0), 1.0)

    # Outer product
    x = np.array([1, 2])
    y = np.array([10, 20, 30])
    outer = outer_product_grid(x, y)
    assert outer.shape == (2, 3)
    assert outer[0, 0] == 10
    assert outer[1, 2] == 60

    # Pairwise distance
    pts_a = np.array([[0.0, 0.0], [3.0, 4.0]])
    pts_b = np.array([[0.0, 0.0], [1.0, 1.0], [3.0, 4.0]])
    dist_mat = pairwise_euclidean_distance(pts_a, pts_b)
    assert dist_mat.shape == (2, 3)
    assert dist_mat[0, 0] == pytest.approx(0.0)
    assert dist_mat[0, 2] == pytest.approx(5.0)
    assert dist_mat[1, 2] == pytest.approx(0.0)


def test_numpy_vectorization_patterns() -> None:
    # Activation functions
    x = np.array([-2.0, 0.0, 3.0])
    relu_out = relu(x)
    assert np.array_equal(relu_out, [0.0, 0.0, 3.0])

    sig = sigmoid(np.array([0.0]))
    assert sig[0] == pytest.approx(0.5)

    # Branching np.select
    scores = np.array([95, 82, 74, 61, 45])
    grades = categorize_values(scores)
    assert grades.tolist() == ["A", "B", "C", "D", "F"]

    # Drawdown
    prices = np.array([100.0, 120.0, 90.0, 110.0, 80.0])
    dd_series = cumulative_drawdown(prices)
    max_dd = float(np.max(np.abs(dd_series))) * 100.0
    assert max_dd == pytest.approx(33.333, abs=1e-2)

    # Moving window difference
    diffs = compute_moving_window_diff(prices, lag=1)
    assert diffs[0] == pytest.approx(20.0)

    # Benchmark
    bench = benchmark_loop_vs_vectorized(n=5_000)
    assert bench["speedup_factor"] > 1.0


def test_numpy_memory_optimization() -> None:
    arr = np.zeros((50, 50), dtype=float)
    layout = inspect_memory_layout(arr)
    assert layout["c_contiguous"] is True
    assert layout["shape"] == (50, 50)

    # In place
    a = np.ones(5, dtype=float)
    id_before, id_after = compute_in_place(a, 3.0)
    assert id_before == id_after
    assert np.array_equal(a, [3.0, 3.0, 3.0, 3.0, 3.0])

    # View vs copy
    orig = np.arange(10)
    view_test = verify_view_vs_copy(orig)
    assert view_test["view_shares_memory"] is True
    assert view_test["copy_shares_memory"] is False

    # Downcast
    large_ints = np.array([10, 20, 50], dtype=np.int64)
    downcast_ints, stats = optimize_numeric_dtypes(large_ints)
    assert downcast_ints.dtype == np.int8
    assert stats["savings_percentage"] > 0
    assert stats["original_bytes"] > stats["optimized_bytes"]


# ============================================================================
# STEP 5.2: PANDAS TABULAR DATA TESTS
# ============================================================================

def test_pandas_basics_pipeline() -> None:
    # Cleaning
    raw = pd.DataFrame(
        {
            "Product Name": ["Item A", "Item B", None],
            "Quantity": ["5", "invalid", "10"],
            "Unit Price": ["20.5", "15.0", "30.0"],
            "Sales Date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        }
    )
    cleaned = clean_sales_data(raw)
    assert len(cleaned) == 2
    assert "product_name" in cleaned.columns
    assert cleaned["quantity"].iloc[1] == 0

    # Missing value imputation
    df_na = pd.DataFrame({"num": [10.0, None, 30.0], "cat": ["X", None, "Z"]})
    imputed = handle_missing_values(df_na, numeric_strategy="mean", categorical_fill="Missing")
    assert imputed["num"].iloc[1] == pytest.approx(20.0)
    assert imputed["cat"].iloc[1] == "Missing"

    # String parsing
    df_str = pd.DataFrame({"sku": ["SKU123-A", "PROD99"]})
    transformed = transform_string_columns(df_str, "sku")
    assert transformed["sku_code"].tolist() == ["SKU", "PROD"]

    # Datetime features
    df_dt = pd.DataFrame({"dt": ["2026-01-03", "2026-01-05"]})  # Jan 3 is Saturday
    dt_feats = extract_datetime_features(df_dt, "dt")
    assert dt_feats["dt_is_weekend"].iloc[0] is True or dt_feats["dt_is_weekend"].iloc[0] == 1
    assert dt_feats["dt_is_weekend"].iloc[1] is False or dt_feats["dt_is_weekend"].iloc[1] == 0


def test_pandas_groupby_aggregations() -> None:
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "department": ["Tech", "Tech", "Tech", "Books"],
            "revenue": [100.0, 200.0, 300.0, 50.0],
        }
    )
    # Named aggregation
    agg_res = aggregate_sales_by_department(df)
    tech = agg_res[agg_res["department"] == "Tech"].iloc[0]
    assert tech["total_revenue"] == 600.0
    assert tech["average_ticket"] == 200.0
    assert tech["order_count"] == 3

    # Group Z-score
    z = calculate_group_zscore(df, "department", "revenue")
    assert z.iloc[1] == pytest.approx(0.0)  # 200 is mean of [100, 200, 300]

    # Percentage of group total
    pct = calculate_percentage_of_group_total(df, "department", "revenue")
    assert pct.iloc[0] == pytest.approx(100.0 / 600.0 * 100.0)

    # Filter
    filtered = filter_high_volume_groups(df, "department", min_count=2, min_total_revenue=200.0)
    assert (filtered["department"] == "Tech").all()
    assert len(filtered) == 3


def test_pandas_joins_and_merges() -> None:
    df_a = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    df_b = pd.DataFrame({"id": [2, 3], "role": ["Dev", "Designer"]})

    # Relational merge
    inner = perform_relational_merge(df_a, df_b, on="id", how="inner")
    assert len(inner) == 1
    assert inner["name"].iloc[0] == "Bob"

    # Outer with indicator
    outer = perform_relational_merge(df_a, df_b, on="id", how="outer", indicator=True)
    assert len(outer) == 3
    assert "_merge" in outer.columns

    # Time series asof merge
    trades = pd.DataFrame({"time": pd.to_datetime(["2026-01-01 10:00:05"]), "price": [100.5]})
    quotes = pd.DataFrame(
        {
            "time": pd.to_datetime(["2026-01-01 10:00:00", "2026-01-01 10:00:10"]),
            "bid": [100.0, 101.0],
        }
    )
    asof = merge_asof_timestamps(trades, quotes, on="time", by=None, direction="backward")
    assert asof["bid"].iloc[0] == 100.0


def test_pandas_window_operations() -> None:
    df = pd.DataFrame({"val": [10.0, 20.0, 30.0, 40.0, 50.0]})
    # Rolling
    rolling = calculate_rolling_metrics(df, "val", window=2)
    assert rolling["val_rolling_mean_2"].iloc[1] == 15.0
    assert rolling["val_rolling_mean_2"].iloc[4] == 45.0

    # Expanding
    expanding = calculate_expanding_metrics(df, "val")
    assert expanding["val_cumsum"].iloc[4] == 150.0

    # Shift & Return
    shifted = calculate_lag_and_returns(df, value_col="val", periods=1)
    assert shifted["val_lag_1"].iloc[1] == 10.0
    assert shifted["val_pct_change"].iloc[1] == pytest.approx(1.0)  # (20-10)/10 = 100%


def test_pandas_memory_and_optimization() -> None:
    df = pd.DataFrame(
        {
            "id": np.arange(100, dtype=np.int64),
            "tag": ["alpha"] * 50 + ["beta"] * 50,  # low cardinality
            "price": np.full(100, 19.99, dtype=np.float64),
        }
    )
    optimized, stats = optimize_dtypes(df)
    assert str(optimized["tag"].dtype) == "category"
    assert optimized["price"].dtype == np.float32
    assert stats["saved_bytes"] > 0

    # Chunks
    chunks = list(chunk_dataframe(df, chunk_size=25))
    assert len(chunks) == 4
    assert len(chunks[0]) == 25


# ============================================================================
# STEP 5.3: STATISTICAL ANALYSIS TESTS
# ============================================================================

def test_statistics_descriptive() -> None:
    series = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0, 1000.0])  # 1000 is an outlier
    summary = describe_series(series)
    assert summary["count"] == 6.0
    assert summary["median"] == 35.0
    assert summary["min"] == 10.0
    assert summary["max"] == 1000.0

    # Outliers
    is_outlier, bounds = detect_iqr_outliers(series)
    assert is_outlier.iloc[-1] is True or is_outlier.iloc[-1] == 1
    assert bounds["outlier_count"] == 1.0

    # Percentiles
    pcts = compute_percentiles(series, percentiles=[50.0])
    assert pcts["p50"] == 35.0

    # Bivariate
    x = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
    bivar = compute_bivariate_metrics(x, y)
    assert bivar["pearson_correlation"] == pytest.approx(1.0)
    assert bivar["spearman_correlation"] == pytest.approx(1.0)


def test_statistics_distributions() -> None:
    # Normal
    norm = normal_distribution_metrics(mean=0.0, std=1.0)
    assert norm["empirical_rule"]["within_1_std"] == pytest.approx(68.27, abs=0.1)
    assert norm["empirical_rule"]["within_2_std"] == pytest.approx(95.45, abs=0.1)

    # Binomial
    binom = binomial_distribution_metrics(n=4, p=0.5, k_values=[2])
    assert binom["expected_value"] == 2.0
    assert binom["pmf"][0] == pytest.approx(0.375)  # 6/16

    # Poisson
    pois = poisson_distribution_metrics(mu=4.0, k_values=[4])
    assert pois["mean"] == 4.0
    assert pois["variance"] == 4.0

    # Normality test
    np.random.seed(42)
    norm_sample = np.random.normal(0, 1, size=150)
    res = evaluate_normality_ks(norm_sample)
    assert res["is_normal_05"] == 1.0


def test_statistics_hypothesis_testing() -> None:
    np.random.seed(42)
    # One sample
    data = np.random.normal(loc=10.0, scale=1.0, size=50)
    res_1 = one_sample_t_test(data, pop_mean=10.0)
    assert res_1["reject_null"] is False

    # Two sample
    treatment = np.random.normal(loc=15.0, scale=1.0, size=50)
    res_2 = two_sample_t_test(data, treatment)
    assert res_2["reject_null"] is True
    assert res_2["diff_means"] == pytest.approx(5.0, abs=0.5)

    # Paired
    post = data + np.random.normal(loc=2.0, scale=0.5, size=50)
    res_paired = paired_t_test(data, post)
    assert res_paired["reject_null"] is True
    assert res_paired["mean_change"] == pytest.approx(2.0, abs=0.3)

    # ANOVA
    grp3 = np.random.normal(loc=20.0, scale=1.0, size=50)
    res_anova = one_way_anova(data, treatment, grp3)
    assert res_anova["reject_null"] is True

    # Chi-Square
    contingency = [[50, 10], [10, 50]]
    res_chi = chi_square_test_of_independence(contingency)
    assert res_chi["reject_null"] is True

    # Mann-Whitney
    res_mw = mann_whitney_u_test(data, treatment)
    assert res_mw["reject_null"] is True


def test_statistics_regression() -> None:
    # Simple linear
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([3.0, 5.0, 7.0, 9.0, 11.0])  # y = 2x + 1
    slr = simple_linear_regression(x, y)
    assert slr["slope"] == pytest.approx(2.0)
    assert slr["intercept"] == pytest.approx(1.0)
    assert slr["r_squared"] == pytest.approx(1.0)
    assert slr["rmse"] == pytest.approx(0.0)

    # Multiple linear
    X = np.array([[1.0, 2.0], [2.0, 1.0], [3.0, 4.0], [4.0, 2.0], [5.0, 5.0]])
    # y = 10 + 3*x1 + 4*x2
    y_mult = 10.0 + 3.0 * X[:, 0] + 4.0 * X[:, 1]
    mlr = multiple_linear_regression(X, y_mult, feature_names=["f1", "f2"])
    assert mlr["intercept"] == pytest.approx(10.0)
    assert mlr["coefficients"]["f1"] == pytest.approx(3.0)
    assert mlr["coefficients"]["f2"] == pytest.approx(4.0)
    assert mlr["r_squared"] == pytest.approx(1.0)

    # Prediction
    pred = predict_linear(np.array([[2.0, 3.0]]), mlr)
    # 10 + 3*2 + 4*3 = 10 + 6 + 12 = 28
    assert pred[0] == pytest.approx(28.0)
