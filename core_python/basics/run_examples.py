"""Run Python basic concept examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path

from core_python.basics.collections_utils import (
    build_deque,
    build_frozenset,
    build_named_person,
    build_ordered_counts,
    count_keywords,
    flatten_list,
    frozenset_operations,
    group_by_category,
    list_to_tuple,
    merge_config_maps,
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
from core_python.basics.debugging_logging import (
    log_debug_context,
    log_exception,
    record_processing_step,
    setup_logger,
    time_execution,
)
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
    filter_map_example,
    fibonacci,
    keyword_only_example,
    make_power,
    merge_options,
    positional_only_example,
    safe_divide,
)
from core_python.basics.variables import compute_discounted_price

logger = setup_logger("core_python_basics_examples")


def run_variables_examples() -> None:
    logger.info("Running variables examples")
    print("compute_discounted_price(100.0, 0.25) ->", compute_discounted_price(100.0, 0.25))


def run_control_flow_examples() -> None:
    logger.info("Running control flow examples")
    print("filter_positive_numbers([-2, 0, 3, 8]) ->", filter_positive_numbers([-2, 0, 3, 8]))
    print("categorize_scores([82, 91, 67, 54]) ->", categorize_scores([82, 91, 67, 54]))
    print("cumulative_sum([1, 2, 3, 4]) ->", cumulative_sum([1, 2, 3, 4]))
    print("classify_numbers([1, 2, 3]) ->", classify_numbers([1, 2, 3]))
    print("while_sum(5) ->", while_sum(5))
    print("find_first_divisible([5, 7, 10], 5) ->", find_first_divisible([5, 7, 10], 5))
    print("zip_and_enumerate(['a', 'b'], [1, 2]) ->", zip_and_enumerate(["a", "b"], [1, 2]))
    print("loop_else_search([1, 2, 3], 4) ->", loop_else_search([1, 2, 3], 4))
    print("list(repeated_pattern(3)) ->", list(repeated_pattern(3)))


def run_function_examples() -> None:
    logger.info("Running functions examples")
    values = [10.0, 20.0, 30.0]
    print("calculate_summary_statistics([10.0, 20.0, 30.0]) ->", calculate_summary_statistics(values))
    print("apply_transformations('data', str.upper, lambda x: x + '!') ->", apply_transformations("data", str.upper, lambda x: x + "!"))
    print("fibonacci(7) ->", fibonacci(7))
    print("build_greeting('Hello', 'world', 'from', 'Python') ->", build_greeting("Hello", "world", "from", "Python"))
    print("safe_divide(10.0, 0.0, default=1.0) ->", safe_divide(10.0, 0.0, default=1.0))
    print("merge_options({'a': 1}, {'b': 2}, a=3) ->", merge_options({"a": 1}, {"b": 2}, a=3))
    print("compose(str.upper, lambda s: s + '!')('hello') ->", compose(str.upper, lambda s: s + "!")("hello"))
    print("positional_only_example(1, 2, 3, d=4) ->", positional_only_example(1, 2, 3, d=4))
    print("keyword_only_example(3, factor=4) ->", keyword_only_example(3, factor=4))
    print("make_power(2)(3.0) ->", make_power(2)(3.0))
    print("filter_map_example([1,2,3,4], lambda x: x % 2 == 0, lambda x: x * 10) ->", filter_map_example([1, 2, 3, 4], lambda x: x % 2 == 0, lambda x: x * 10))


def run_data_type_examples() -> None:
    logger.info("Running data type examples")
    print("parse_bool('Yes') ->", parse_bool("Yes"))
    print("parse_int('42') ->", parse_int("42"))
    print("parse_float('3.14') ->", parse_float("3.14"))
    print("parse_date('2026-05-07') ->", parse_date("2026-05-07"))
    print("parse_iso_datetime('2026-05-07T12:00:00') ->", parse_iso_datetime("2026-05-07T12:00:00"))
    print("parse_list('a, b, c') ->", parse_list("a, b, c"))
    print("safe_cast('100', int) ->", safe_cast("100", int))
    print("safe_cast('invalid', int, default=0) ->", safe_cast("invalid", int, default=0))
    print("normalize_string('  Hello World ') ->", normalize_string("  Hello World "))
    print("stringify(None) ->", stringify(None))


def run_collection_examples() -> None:
    logger.info("Running collection examples")
    print("flatten_list([[1, 2], [3, 4]]) ->", flatten_list([[1, 2], [3, 4]]))
    print("list_to_tuple([1, 2, 3]) ->", list_to_tuple([1, 2, 3]))
    print("tuple_to_list((4, 5, 6)) ->", tuple_to_list((4, 5, 6)))
    print("count_keywords(['python','code','python']) ->", count_keywords(["python", "code", "python"]))
    print("unique_preserve_order([1, 2, 1, 3]) ->", unique_preserve_order([1, 2, 1, 3]))
    print("build_frozenset([1, 2, 2]) ->", build_frozenset([1, 2, 2]))
    print("frozenset_operations(frozenset({1, 2}), frozenset({2, 3})) ->", frozenset_operations(frozenset({1, 2}), frozenset({2, 3})))
    print("set_operations({1,2,3}, {2,3,4}) ->", set_operations({1, 2, 3}, {2, 3, 4}))
    print("build_named_person('Alice', 30, 'Engineer') ->", build_named_person("Alice", 30, "Engineer"))
    print("build_ordered_counts(['a','b','a']) ->", build_ordered_counts(["a", "b", "a"]))
    print("merge_config_maps({'env':'prod'}, {'timeout': '30'}) ->", merge_config_maps({"env": "prod"}, {"timeout": "30"}))
    dq = build_deque([1, 2, 3], maxlen=5)
    print("build_deque([1,2,3], maxlen=5) ->", dq)
    print("rotate_deque(dq, 1) ->", rotate_deque(dq, 1))


def run_file_io_examples() -> None:
    logger.info("Running file I/O examples")
    asset_dir = Path("./core_python/basics/assets/file_io")
    text_path = asset_dir / "sample_text.txt"
    write_text_file(text_path, "Hello Python file I/O\n")
    append_text_file(text_path, "This is appended text.\n")
    print("Read text file ->", read_text_file(text_path))

    safe_path = asset_dir / "sample_safe.txt"
    safe_write_text_file(safe_path, "Safe write example\n")
    print("Safe text file exists ->", file_exists(safe_path))

    yaml_path = asset_dir / "sample_data.yaml"
    yaml_data = {"project": "python-mastery", "version": "3.10+", "features": ["JSON", "CSV", "YAML"]}
    write_yaml_file(yaml_path, yaml_data)
    print("Read YAML ->", read_yaml_file(yaml_path))

    binary_path = asset_dir / "sample_bytes.bin"
    write_binary_file(binary_path, b"\x00\x01\x02\x03")
    print("Read binary bytes ->", read_binary_file(binary_path))

    csv_rows = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
    csv_output = asset_dir / "sample_output.csv"
    write_dicts_to_csv(csv_output, csv_rows)
    print("CSV dict rows ->", read_csv_to_dicts(csv_output))

    print("Directory listing ->", [entry.name for entry in list_directory(resolve_path(asset_dir)) if entry.suffix in {".txt", ".json", ".csv", ".yaml", ".bin"}])


def run_logging_examples() -> None:
    logger.info("Running logging examples")
    record_processing_step(logger, "example_step")
    log_debug_context(logger, "Processing order", {"order_id": 1001, "status": "received"})

    try:
        raise ValueError("sample failure for logging demonstration")
    except ValueError as error:
        log_exception(logger, error, "Example exception caught")

    @time_execution
    def sample_task() -> str:
        return "timed task completed"

    print("sample_task() ->", sample_task())
    print("See logged output at the console for structured logging examples.")


def run_all_examples() -> None:
    run_variables_examples()
    run_control_flow_examples()
    run_function_examples()
    run_data_type_examples()
    run_collection_examples()
    run_file_io_examples()
    run_logging_examples()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run core Python basics examples.")
    parser.add_argument("--module", choices=["variables", "control_flow", "functions", "data_types", "collections", "file_io", "logging", "all"], default="all", help="Module to run")
    args = parser.parse_args()

    if args.module == "variables":
        run_variables_examples()
    elif args.module == "control_flow":
        run_control_flow_examples()
    elif args.module == "functions":
        run_function_examples()
    elif args.module == "data_types":
        run_data_type_examples()
    elif args.module == "collections":
        run_collection_examples()
    elif args.module == "file_io":
        run_file_io_examples()
    elif args.module == "logging":
        run_logging_examples()
    else:
        run_all_examples()


if __name__ == "__main__":
    main()
