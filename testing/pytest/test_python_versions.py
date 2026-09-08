"""
Unit tests for Python Versions module (3.8 — 3.13).
"""

from __future__ import annotations
import sys
import pytest
from core_python.python_versions.version_matrix import (
    get_all_capabilities,
    has_walrus_operator,
    has_dict_merge_operators,
    has_removeprefix_suffix,
)
from core_python.python_versions.python_38 import (
    compute_discount,
    filter_and_transform_data,
    parse_query_params,
    calculate_metrics,
)
from core_python.python_versions.python_39 import (
    merge_configs,
    update_in_place,
    sanitize_identifier,
    resolve_build_dependencies,
)
from core_python.python_versions.python_310 import (
    evaluate_event,
    safe_zip,
    parse_response_status,
)
from core_python.python_versions.python_311 import (
    parse_record_with_notes,
    parse_toml_string,
    QueryBuilder,
)
from core_python.python_versions.python_312 import (
    get_head,
    CustomWorker,
    demonstrate_fstring_enhancements,
)
from core_python.python_versions.python_313 import (
    is_free_threaded_build,
    get_gil_architecture_notes,
    fetch_user_v1,
)


def test_capability_matrix():
    caps = get_all_capabilities()
    assert len(caps) >= 15
    assert has_walrus_operator() is True
    assert has_dict_merge_operators() is True
    assert has_removeprefix_suffix() is True


def test_python_38_features():
    # Positional-only parameter check
    res = compute_discount(100.0, 0.10, "USD", tax=0.05)
    assert res == 94.5
    with pytest.raises(TypeError):
        compute_discount(price=100.0, discount_rate=0.10)  # type: ignore

    # Walrus in comprehension
    items = ["a", "ab", "abc", "abcd", "python"]
    filtered = filter_and_transform_data(items)
    assert len(filtered) == 2
    assert [x["item"] for x in filtered] == ["abcd", "python"]

    # Walrus in regex while loop
    parsed = parse_query_params("a=1&b=2")
    assert parsed == {"a": "1", "b": "2"}

    # Math
    prod, root = calculate_metrics([2, 5, 10], 81)
    assert prod == 100
    assert root == 9


def test_python_39_features():
    # Dict merge & update
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 20, "c": 30}
    merged = merge_configs(d1, d2)
    assert merged == {"a": 1, "b": 20, "c": 30}

    in_place = {"x": 10}
    update_in_place(in_place, {"y": 20})
    assert in_place == {"x": 10, "y": 20}

    # removeprefix / suffix
    assert sanitize_identifier("tbl_users_temp") == "users"

    # Topological sorter
    graph = {"B": {"A"}, "C": {"B"}, "A": set()}
    order = resolve_build_dependencies(graph)
    assert order == ["A", "B", "C"]


def test_python_310_features():
    # Pattern matching dispatcher
    assert "Clicked at coordinates" in evaluate_event({"type": "click", "x": 10, "y": 20})
    assert evaluate_event({"type": "keypress", "key": "Enter"}) == "Submit action triggered"
    assert "Server error" in evaluate_event({"type": "error", "code": 500})
    assert "Client/Request error" in evaluate_event({"type": "error", "code": 404})
    assert "CLI command" in evaluate_event(["docker", "ps"])

    # Strict zip
    assert safe_zip([1, 2], ["a", "b"]) == [(1, "a"), (2, "b")]
    with pytest.raises(ValueError):
        safe_zip([1, 2, 3], ["a", "b"])

    # Union status
    assert parse_response_status(200) == "SUCCESS"
    assert parse_response_status("404") == "CLIENT_ERROR"


def test_python_311_features():
    # Exception notes
    with pytest.raises(ValueError):
        parse_record_with_notes({"id": "err-1", "value": "-10"})

    # TOML parser
    toml_str = 'app = "Mastery"\nversion = "2.0"'
    parsed = parse_toml_string(toml_str)
    assert parsed.get("app") == "Mastery"

    # QueryBuilder Self chaining
    q = QueryBuilder().select("*").from_table("items").where("qty > 0").build()
    assert q == "SELECT * FROM items WHERE qty > 0"


def test_python_312_features():
    # Generic head
    assert get_head([10, 20, 30]) == 10
    assert get_head(["a", "b"]) == "a"

    # typing.override
    worker = CustomWorker()
    assert worker.execute() == "customized worker execution"

    # fstrings
    fstr = demonstrate_fstring_enhancements()
    assert "Items: alpha, beta" in fstr


def test_python_313_features():
    # Free-threaded build detection
    assert isinstance(is_free_threaded_build(), bool)

    notes = get_gil_architecture_notes()
    assert "Immortal Objects" in notes
    assert "Mimalloc Integration" in notes

    # Deprecated decorator
    with pytest.deprecated_call():
        user = fetch_user_v1(1)
        assert user["version"] == 1
