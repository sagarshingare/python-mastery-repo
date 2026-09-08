"""Comprehensive test suite for SQL & Relational Databases module."""

from __future__ import annotations

import pytest

# SQL Fundamentals
from sql.basics import (
    batch_insert_employees,
    create_connection as create_basics_conn,
    delete_inactive_employees,
    filter_employees,
    get_department_metrics,
    init_fundamentals_db,
    insert_employee,
    paginate_employees,
    update_employee_salary,
)

# SQL Joins
from sql.joins import (
    create_connection as create_joins_conn,
    get_anti_join_departments,
    get_cross_join_combinations,
    get_full_outer_join_simulation,
    get_inner_join_records,
    get_left_join_records,
    get_self_join_hierarchy,
    init_joins_db,
)

# SQL CTEs
from sql.cte import (
    create_connection as create_cte_conn,
    generate_number_sequence,
    get_modular_pipeline_cte,
    get_org_chart_hierarchy,
    init_cte_db,
)

# SQL Window Functions
from sql.window_functions import (
    create_connection as create_window_conn,
    get_month_over_month_growth,
    get_moving_aggregations,
    get_ranking_metrics,
    get_top_earners_per_dept,
    init_window_db,
)

# SQL Query Optimization
from sql.optimization import (
    benchmark_single_column_index,
    create_connection as create_opt_conn,
    demonstrate_composite_prefix_rule,
    demonstrate_sargability,
    explain_query_plan,
    init_optimization_db,
)

# SQL Advanced Patterns
from sql.advanced_queries import (
    create_connection as create_adv_conn,
    detect_gaps_and_islands,
    get_user_preference,
    init_advanced_db,
    pivot_role_headcount,
    query_json_metadata,
    unpivot_quarterly_sales,
    upsert_user_preference,
)


# ============================================================================
# STEP 4.1: SQL FUNDAMENTALS TESTS
# ============================================================================

def test_sql_fundamentals_crud() -> None:
    conn = create_basics_conn()
    try:
        init_fundamentals_db(conn)

        # Single insert
        new_id = insert_employee(
            conn,
            first_name="Barbara",
            last_name="Liskov",
            email="barbara@example.com",
            department_id=1,
            salary=145000.0,
            hire_date="2024-01-01",
        )
        assert new_id > 0

        # Batch insert
        batch_records = [
            ("Dennis", "Ritchie", "dennis@example.com", 1, 155000.0, "2024-02-01", 1),
            ("Ken", "Thompson", "ken@example.com", 1, 150000.0, "2024-02-01", 1),
        ]
        inserted = batch_insert_employees(conn, batch_records)
        assert inserted == 2

        # Update
        updated = update_employee_salary(conn, department_id=1, multiplier=1.10)
        assert updated >= 5

        # Delete inactive
        deleted = delete_inactive_employees(conn, hire_date_before="2024-01-01")
        assert deleted == 1
    finally:
        conn.close()


def test_sql_fundamentals_filtering_and_pagination() -> None:
    conn = create_basics_conn()
    try:
        init_fundamentals_db(conn)

        # Filtering
        results = filter_employees(
            conn,
            department_ids=[1, 2],
            min_salary=130000.0,
            email_domain="example.com",
            active_only=True,
        )
        assert len(results) == 4
        assert all(r["salary"] >= 130000.0 for r in results)

        # Aggregation
        metrics = get_department_metrics(conn, min_headcount=2)
        assert len(metrics) == 2
        depts = {m["department_name"]: m for m in metrics}
        assert "Engineering" in depts
        assert depts["Engineering"]["employee_count"] == 3

        # Pagination
        total, page_1 = paginate_employees(conn, page=1, page_size=2)
        assert total == 5
        assert len(page_1) == 2
        assert page_1[0]["salary"] >= page_1[1]["salary"]

        _, page_2 = paginate_employees(conn, page=2, page_size=2)
        assert len(page_2) == 2
        assert page_1 != page_2
    finally:
        conn.close()


# ============================================================================
# STEP 4.2: SQL JOIN PATTERNS TESTS
# ============================================================================

def test_sql_joins_varieties() -> None:
    conn = create_joins_conn()
    try:
        init_joins_db(conn)

        # Inner join
        inner = get_inner_join_records(conn)
        assert len(inner) == 3
        assert all(r["department_name"] is not None for r in inner)

        # Left join (preserves Contractor Dan with Unassigned)
        left = get_left_join_records(conn)
        assert len(left) == 4
        unassigned = [r for r in left if r["employee_name"] == "Contractor Dan"]
        assert len(unassigned) == 1
        assert unassigned[0]["department_name"] == "Unassigned"

        # Anti-join (finds empty departments)
        anti = get_anti_join_departments(conn)
        anti_names = {r["department_name"] for r in anti}
        assert "Marketing" in anti_names
        assert "Unused Operations" in anti_names

        # Self-join (resolves manager)
        self_join = get_self_join_hierarchy(conn)
        turing = next(r for r in self_join if r["employee_name"] == "Alan Turing")
        assert turing["manager_name"] == "Ada Lovelace"

        # Cross join (2 products * 3 sizes = 6 rows)
        cross = get_cross_join_combinations(conn)
        assert len(cross) == 6
        assert cross[0]["sku"] == "TSHIRT-01-S"

        # Full outer join simulation
        full = get_full_outer_join_simulation(conn)
        assert len(full) >= 5
    finally:
        conn.close()


# ============================================================================
# STEP 4.3: COMMON TABLE EXPRESSIONS TESTS
# ============================================================================

def test_sql_cte_pipelines_and_recursion() -> None:
    conn = create_cte_conn()
    try:
        init_cte_db(conn)

        # Modular non-recursive CTE
        orders = get_modular_pipeline_cte(conn)
        assert len(orders) == 3  # North America orders
        assert all(o["region"] == "North America" for o in orders)

        # Recursive sequence generator
        seq = generate_number_sequence(conn, start=1, end=5)
        assert seq == [1, 2, 3, 4, 5]

        # Recursive tree hierarchy (Org Chart)
        org = get_org_chart_hierarchy(conn)
        assert len(org) == 6
        ceo = org[0]
        assert ceo["name"] == "Ada Lovelace" and ceo["depth"] == 1
        assert ceo["management_path"] == "Ada Lovelace"

        # Leaves at depth 4
        depth_4 = [e for e in org if e["depth"] == 4]
        assert len(depth_4) == 2
        assert any("Alan Turing -> John von Neumann" in e["management_path"] for e in depth_4)
    finally:
        conn.close()


# ============================================================================
# STEP 4.4: WINDOW FUNCTIONS TESTS
# ============================================================================

def test_sql_window_functions() -> None:
    conn = create_window_conn()
    try:
        init_window_db(conn)

        # Ranking metrics
        ranking = get_ranking_metrics(conn)
        assert len(ranking) == 7
        eng_ada = next(r for r in ranking if r["name"] == "Ada Lovelace")
        assert eng_ada["row_num"] == 1
        assert eng_ada["rank_pos"] == 1
        assert eng_ada["dense_rank_pos"] == 1

        # Ties in salary (Grace Hopper & Alan Turing at $140,000)
        eng_grace = next(r for r in ranking if r["name"] == "Grace Hopper")
        eng_alan = next(r for r in ranking if r["name"] == "Alan Turing")
        assert eng_grace["rank_pos"] == 2
        assert eng_alan["rank_pos"] == 2
        assert eng_grace["dense_rank_pos"] == 2
        assert eng_alan["dense_rank_pos"] == 2

        # Top 2 earners per department
        top_2 = get_top_earners_per_dept(conn, top_n=2)
        assert len(top_2) == 5  # 3 in Engineering (due to tie) + 2 in Product

        # Lead / Lag MoM growth
        growth = get_month_over_month_growth(conn)
        assert len(growth) == 6
        assert growth[0]["prior_month_revenue"] is None
        assert growth[1]["prior_month_revenue"] == 50000.0
        assert growth[1]["mom_growth_pct"] == 16.0  # (58k - 50k)/50k = 16%

        # Moving window frames
        moving = get_moving_aggregations(conn)
        assert moving[0]["cumulative_revenue"] == 50000.0
        assert moving[1]["cumulative_revenue"] == 108000.0
        assert moving[2]["moving_avg_3m"] == round((50000.0 + 58000.0 + 62000.0) / 3, 2)
    finally:
        conn.close()


# ============================================================================
# STEP 4.5: ADVANCED SQL PATTERNS TESTS
# ============================================================================

def test_sql_advanced_patterns() -> None:
    conn = create_adv_conn()
    try:
        init_advanced_db(conn)

        # Conditional aggregation pivot
        pivoted = pivot_role_headcount(conn)
        assert len(pivoted) == 2
        eng = next(r for r in pivoted if r["department_name"] == "Engineering")
        assert eng["engineers"] == 3
        assert eng["managers"] == 0
        assert eng["designers"] == 0

        # Unpivoting
        unpivoted = unpivot_quarterly_sales(conn)
        assert len(unpivoted) == 8  # 2 products * 4 quarters

        # Atomic UPSERT
        before = get_user_preference(conn, 42)
        assert before is not None and before["theme"] == "dark"
        upsert_user_preference(
            conn,
            user_id=42,
            theme="solarized-light",
            notifications_enabled=False,
            updated_at="2026-06-15 14:30:00",
        )
        after = get_user_preference(conn, 42)
        assert after is not None and after["theme"] == "solarized-light"
        assert after["notifications_enabled"] == 0

        # Semi-structured JSON querying
        json_staff = query_json_metadata(conn)
        assert len(json_staff) == 3
        names = {r["name"] for r in json_staff}
        assert "Ada Lovelace" in names
        assert "Grace Hopper" in names

        # Gaps & Islands streak detection
        streaks = detect_gaps_and_islands(conn, min_streak_days=3)
        assert len(streaks) == 1
        streak = streaks[0]
        assert streak["user_id"] == 101
        assert streak["consecutive_days"] == 4
        assert streak["streak_start"] == "2026-03-01"
        assert streak["streak_end"] == "2026-03-04"
    finally:
        conn.close()


# ============================================================================
# STEP 4.6: QUERY OPTIMIZATION TESTS
# ============================================================================

def test_sql_optimization_and_plans() -> None:
    conn = create_opt_conn()
    try:
        init_optimization_db(conn)

        # Explain query plan returns valid output
        plan = explain_query_plan(conn, "SELECT COUNT(*) FROM orders WHERE total_amount > 400.0;")
        assert len(plan) > 0

        # Single column indexing plan transition
        idx_bench = benchmark_single_column_index(conn)
        assert "SCAN" in idx_bench["plan_before_index"]
        assert "USING INDEX" in idx_bench["plan_after_index"]

        # Composite index leftmost prefix rule
        comp = demonstrate_composite_prefix_rule(conn)
        assert "USING INDEX" in comp["query_prefix_and_second"]["plan"]
        assert "USING INDEX" in comp["query_prefix_only"]["plan"]
        assert "SCAN" in comp["query_non_prefix_only"]["plan"]

        # Sargability verification
        sarg = demonstrate_sargability(conn)
        assert "SCAN" in sarg["non_sargable"]["plan"]
        assert "USING INDEX" in sarg["sargable"]["plan"]
    finally:
        conn.close()
