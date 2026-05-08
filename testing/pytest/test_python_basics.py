"""Tests for Python basics modules."""

from __future__ import annotations

from collections import OrderedDict
from datetime import date
import logging
from pathlib import Path

import pytest

from core_python.basics.collections_utils import (
    build_deque,
    build_frozenset,
    build_named_person,
    build_ordered_counts,
    count_keywords,
    flatten_list,
    frozenset_operations,
    group_by_category,
    invert_dictionary,
    list_to_tuple,
    merge_config_maps,
    merge_dictionaries,
    normalize_mapping_keys,
    rotate_deque,
    set_operations,
    tuple_to_list,
    unique_preserve_order,
)
from core_python.basics.control_flow import (
    categorize_scores,
    classify_numbers,
    cumulative_sum,
    filter_positive_numbers,
    find_first_divisible,
    loop_else_search,
    repeated_pattern,
    while_sum,
    zip_and_enumerate,
)
from core_python.basics.data_types import (
    normalize_string,
    parse_bool,
    parse_date,
    parse_float,
    parse_int,
    parse_iso_datetime,
    parse_list,
    safe_cast,
    stringify,
)
from core_python.basics.debugging_logging import log_debug_context, log_exception, setup_logger, time_execution
from core_python.basics.file_io import (
    append_text_file,
    file_exists,
    list_directory,
    read_binary_file,
    read_csv_to_dicts,
    read_json_file,
    read_text_file,
    read_yaml_file,
    resolve_path,
    safe_write_text_file,
    write_binary_file,
    write_dicts_to_csv,
    write_json_file,
    write_text_file,
    write_yaml_file,
)
from core_python.basics.functions import (
    apply_transformations,
    build_greeting,
    calculate_summary_statistics,
    compose,
    fibonacci,
    keyword_only_example,
    make_power,
    merge_options,
    positional_only_example,
    safe_divide,
)
from core_python.basics.modules_packages import (
    get_module_attribute,
    get_module_file_path,
    get_module_version,
    import_module_from_path,
    is_module_installed,
    is_package,
    list_module_attributes,
    reload_module,
    safe_import_module,
)
from core_python.basics.variables import (
    PYTHON_VERSION,
    DEFAULT_DISCOUNT_RATE,
    compute_compound_interest,
    compute_discounted_price,
    describe_sequence_behavior,
    split_full_name,
    swap_values,
)


def test_compute_discounted_price() -> None:
    assert compute_discounted_price(200.0, 0.25) == 150.0


def test_default_discount_rate_and_version_metadata() -> None:
    assert DEFAULT_DISCOUNT_RATE == 0.1
    assert PYTHON_VERSION.count(".") >= 2


def test_swap_values() -> None:
    assert swap_values("a", "b") == ("b", "a")


def test_split_full_name() -> None:
    assert split_full_name("Jane Doe") == ("Jane", "Doe")


def test_compute_compound_interest() -> None:
    assert compute_compound_interest(1000.0, 0.05, 2) == 1102.5


def test_describe_sequence_behavior() -> None:
    values, sequence = describe_sequence_behavior([1, 2, 3])
    assert values == [1, 2, 3]
    assert sequence == (1, 2, 3)


def test_filter_positive_numbers() -> None:
    assert filter_positive_numbers([-1, 0, 3, 7]) == [3, 7]


def test_categorize_scores() -> None:
    assert categorize_scores([95, 75, 64, 50]) == ["excellent", "good", "needs_improvement", "failed"]


def test_cumulative_sum() -> None:
    assert cumulative_sum([1, 2, 3]) == [1, 3, 6]


def test_classify_numbers() -> None:
    assert classify_numbers([1, 2, 3]) == ["odd", "even", "odd"]


def test_while_sum() -> None:
    assert while_sum(5) == 15


def test_find_first_divisible() -> None:
    assert find_first_divisible([5, 7, 10], 5) == 5
    assert find_first_divisible([1, 2, 3], 7) is None


def test_zip_and_enumerate() -> None:
    assert zip_and_enumerate(["a", "b"], [1, 2]) == [(0, "a", 1), (1, "b", 2)]


def test_loop_else_search() -> None:
    assert loop_else_search([1, 2, 3], 2) == "found"
    assert loop_else_search([1, 2, 3], 5) == "not found"


def test_repeated_pattern() -> None:
    assert list(repeated_pattern(3)) == [0, 1, 2]


def test_calculate_summary_statistics() -> None:
    values = [1.0, 2.0, 3.0]
    assert calculate_summary_statistics(values)["average"] == 2.0


def test_apply_transformations() -> None:
    assert apply_transformations("hello", str.upper, lambda x: x + "!") == "HELLO!"


def test_build_greeting() -> None:
    assert build_greeting("Hello", "world", "from", "Python") == "Hello world from Python"


def test_safe_divide() -> None:
    assert safe_divide(10.0, 2.0) == 5.0
    assert safe_divide(10.0, 0.0, default=1.0) == 1.0


def test_merge_options() -> None:
    assert merge_options({"a": 1}, {"b": 2}, a=3) == {"a": 3, "b": 2}


def test_compose() -> None:
    composed = compose(str.upper, lambda x: x + "!")
    assert composed("hello") == "HELLO!"


def test_positional_and_keyword_only_examples() -> None:
    assert positional_only_example(1, 2, 3, d=4) == 10
    assert keyword_only_example(3, factor=4) == 12


def test_make_power() -> None:
    assert make_power(2)(3.0) == 9.0


def test_fibonacci() -> None:
    assert fibonacci(10) == 55


def test_parse_bool() -> None:
    assert parse_bool("YES") is True
    assert parse_bool("no") is False


def test_parse_int() -> None:
    assert parse_int("42") == 42
    assert parse_int("0xff", base=16) == 255


def test_parse_float() -> None:
    assert parse_float("3.14") == 3.14


def test_parse_date() -> None:
    assert parse_date("2026-05-07") == date(2026, 5, 7)


def test_parse_iso_datetime() -> None:
    assert parse_iso_datetime("2026-05-07T09:00:00").year == 2026


def test_parse_list() -> None:
    assert parse_list("a, b, c") == ["a", "b", "c"]


def test_safe_cast() -> None:
    assert safe_cast("100", int) == 100
    assert safe_cast("invalid", int, default=0) == 0


def test_normalize_string() -> None:
    assert normalize_string("  Hello World ") == "hello world"


def test_stringify() -> None:
    assert stringify(None) == "<null>"
    assert stringify(2.0) == "2"


def test_flatten_list() -> None:
    assert flatten_list([[1, 2], [3]]) == [1, 2, 3]


def test_count_keywords() -> None:
    assert count_keywords(["python", "python", "code"]) == {"python": 2, "code": 1}


def test_group_by_category() -> None:
    assert group_by_category([("a", 1), ("b", 2), ("a", 3)]) == {"a": [1, 3], "b": [2]}


def test_unique_preserve_order() -> None:
    assert unique_preserve_order([1, 2, 1, 3, 2]) == [1, 2, 3]


def test_list_tuple_conversion() -> None:
    assert list_to_tuple([1, 2, 3]) == (1, 2, 3)
    assert tuple_to_list((4, 5, 6)) == [4, 5, 6]


def test_build_frozenset_and_operations() -> None:
    frozen_a = build_frozenset([1, 2, 2])
    assert frozen_a == frozenset({1, 2})
    operations = frozenset_operations(frozen_a, frozenset({2, 3}))
    assert operations["intersection"] == frozenset({2})


def test_invert_dictionary() -> None:
    assert invert_dictionary({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


def test_merge_dictionaries() -> None:
    assert merge_dictionaries({"a": 1}, {"a": 2, "b": 3}) == {"a": 2, "b": 3}


def test_set_operations() -> None:
    assert set_operations({1, 2, 3}, {2, 3, 4})["intersection"] == {2, 3}


def test_build_named_person() -> None:
    assert build_named_person("Alice", 30, "Engineer").name == "Alice"


def test_build_ordered_counts() -> None:
    assert build_ordered_counts(["a", "b", "a"]) == OrderedDict({"a": 2, "b": 1})


def test_merge_config_maps() -> None:
    merged = merge_config_maps({"env": "prod"}, {"timeout": "30"})
    assert merged["env"] == "prod" and merged["timeout"] == "30"


def test_build_deque_rotate() -> None:
    dq = build_deque([1, 2, 3], maxlen=5)
    assert rotate_deque(dq, 1)[0] == 3


def test_normalize_mapping_keys() -> None:
    normalized = normalize_mapping_keys({"A": 1, "B": 2})
    assert normalized["a"] == 1 and normalized["b"] == 2


def test_read_write_json_file(tmp_path: Path) -> None:
    data = {"message": "hello"}
    path = tmp_path / "data.json"
    write_json_file(path, data)
    assert read_json_file(path) == data


def test_read_write_text_file(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    write_text_file(path, "hello world")
    assert read_text_file(path) == "hello world"


def test_append_text_file(tmp_path: Path) -> None:
    path = tmp_path / "append.txt"
    write_text_file(path, "first line\n")
    append_text_file(path, "second line\n")
    assert read_text_file(path).splitlines() == ["first line", "second line"]


def test_safe_write_text_file(tmp_path: Path) -> None:
    path = tmp_path / "safe.txt"
    safe_write_text_file(path, "safe content")
    assert read_text_file(path) == "safe content"


def test_read_write_binary_file(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    write_binary_file(path, b"\x00\x01\x02")
    assert read_binary_file(path) == b"\x00\x01\x02"


def test_read_write_yaml_file(tmp_path: Path) -> None:
    data = {"project": "python", "version": 3.10}
    path = tmp_path / "sample.yaml"
    write_yaml_file(path, data)
    assert read_yaml_file(path) == data


def test_write_dicts_to_csv(tmp_path: Path) -> None:
    rows = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
    path = tmp_path / "sample.csv"
    write_dicts_to_csv(path, rows)
    assert read_csv_to_dicts(path) == rows


def test_resolve_path_and_directory_helpers(tmp_path: Path) -> None:
    nested = tmp_path / "nested" / "file.txt"
    assert not file_exists(nested)
    write_text_file(nested, "content")
    assert file_exists(nested)
    assert resolve_path(nested).suffix == ".txt"
    assert tmp_path in list_directory(tmp_path)[0].parents


def test_read_csv_to_dicts(tmp_path: Path) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")
    assert read_csv_to_dicts(csv_file) == [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]


def test_get_module_attribute() -> None:
    assert get_module_attribute("math", "pi") == 3.141592653589793


def test_safe_import_module() -> None:
    assert safe_import_module("json") is not None
    assert safe_import_module("nonexistent_module_xyz") is None


def test_is_module_installed() -> None:
    assert is_module_installed("json") is True
    assert is_module_installed("nonexistent_module_xyz") is False


def test_is_package() -> None:
    assert is_package("importlib") is True
    assert is_package("sys") is False


def test_list_module_attributes() -> None:
    attrs = list_module_attributes("math")
    assert "pi" in attrs and "sin" in attrs


def test_get_module_file_path() -> None:
    path = get_module_file_path("json")
    assert path.exists()
    assert path.suffix == ".py"


def test_reload_module() -> None:
    import json as json_module

    reloaded = reload_module(json_module)
    assert reloaded is json_module
    assert "dump" in dir(reloaded)


def test_import_module_from_path(tmp_path: Path) -> None:
    source = tmp_path / "sample_module.py"
    source.write_text("VALUE = 42\n", encoding="utf-8")
    module = import_module_from_path(source)
    assert module.VALUE == 42


def test_get_module_version() -> None:
    assert get_module_version("sys") is None
    assert isinstance(get_module_version("json"), (str, type(None)))


def test_setup_logger(tmp_path: Path) -> None:
    logger = setup_logger("pytest_logger", log_file=tmp_path / "test.log")
    assert logger.name == "pytest_logger"


def test_log_debug_context(caplog: pytest.LogCaptureFixture) -> None:
    logger = setup_logger("debug_test")
    logger.setLevel(logging.DEBUG)
    caplog.set_level(logging.DEBUG, logger="debug_test")
    log_debug_context(logger, "Inspect context", {"user": "alice", "retry": 3})
    assert "Inspect context | context: user='alice', retry=3" in caplog.text


def test_log_exception(caplog: pytest.LogCaptureFixture) -> None:
    logger = setup_logger("exception_test")
    logger.setLevel(logging.DEBUG)
    caplog.set_level(logging.DEBUG, logger="exception_test")
    try:
        raise RuntimeError("test error")
    except RuntimeError as error:
        log_exception(logger, error, "caught problem")
    assert "caught problem: test error" in caplog.text
    assert "Traceback:" in caplog.text


def test_time_execution(caplog: pytest.LogCaptureFixture) -> None:
    logger = setup_logger("timer_test")
    logger.setLevel(logging.INFO)
    caplog.set_level(logging.INFO, logger="timer_test")

    @time_execution
    def sample() -> str:
        return "done"

    assert sample() == "done"
    assert "Completed sample in" in caplog.text
