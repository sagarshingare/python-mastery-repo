"""NumPy Arrays module: Creation, slicing, masking, and linear algebra."""

from .array_operations import (
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

__all__ = [
    "create_grid",
    "reshape_array",
    "flatten_array",
    "slice_submatrix",
    "stack_arrays",
    "split_array",
    "filter_by_mask",
    "replace_outliers",
    "normalize_vector",
    "batch_dot",
    "matrix_properties",
]