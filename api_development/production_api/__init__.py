"""Production API architecture patterns."""

from api_development.production_api.production_patterns import (
    lifespan_handler,
    register_health_probes,
    register_problem_details_handler,
    setup_production_middleware,
)

__all__ = [
    "lifespan_handler",
    "setup_production_middleware",
    "register_problem_details_handler",
    "register_health_probes",
]
