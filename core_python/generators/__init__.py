"""
Generators module for lazy evaluation and streaming data pipelines.
"""

from .generator_examples import (
    apply_tax_and_format,
    chunked_generator,
    fibonacci_generator,
    filter_completed_events,
    filter_generator,
    flatten_nested,
    normalized_strings,
    run_pipeline,
    running_average,
    stream_raw_events,
)

__all__ = [
    "apply_tax_and_format",
    "chunked_generator",
    "fibonacci_generator",
    "filter_completed_events",
    "filter_generator",
    "flatten_nested",
    "normalized_strings",
    "run_pipeline",
    "running_average",
    "stream_raw_events",
]
