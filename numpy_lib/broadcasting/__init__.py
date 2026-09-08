"""NumPy Broadcasting module: Rules, dimension expansion, scaling, and pairwise distance."""

from .broadcasting_examples import (
    center_and_scale,
    check_broadcast_compatibility,
    expand_dimension,
    outer_product_grid,
    pairwise_euclidean_distance,
)

__all__ = [
    "check_broadcast_compatibility",
    "expand_dimension",
    "center_and_scale",
    "outer_product_grid",
    "pairwise_euclidean_distance",
]
