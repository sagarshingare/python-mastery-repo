"""Production API patterns: Correlation ID, request timing, RFC 7807 Problem Details,
health/readiness probes, and lifespan context management.
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

logger = logging.getLogger("production_api")


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncGenerator[None, None]:
    """Modern FastAPI lifespan context manager for startup and graceful shutdown."""
    logger.info("Initializing application resources (database pools, caches)...")
    yield
    logger.info("Gracefully releasing application resources...")


def setup_production_middleware(app: FastAPI) -> None:
    """Register correlation ID, request timing, and access logging middleware."""

    @app.middleware("http")
    async def correlation_and_timing_middleware(request: Request, call_next: Callable) -> Response:
        start_time = time.monotonic()

        # Extract or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid4()))
        request.state.correlation_id = correlation_id

        logger.info(
            "Incoming request",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            duration_ms = (time.monotonic() - start_time) * 1000.0
            logger.exception(
                "Unhandled exception processing request: %s (duration=%.2fms)",
                exc,
                duration_ms,
                extra={"correlation_id": correlation_id},
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "type": "about:blank",
                    "title": "Internal Server Error",
                    "status": 500,
                    "detail": "An unexpected server error occurred.",
                    "instance": request.url.path,
                    "correlation_id": correlation_id,
                },
                headers={"X-Correlation-ID": correlation_id},
            )

        duration_ms = (time.monotonic() - start_time) * 1000.0
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"

        logger.info(
            "Request completed",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response


def register_problem_details_handler(app: FastAPI) -> None:
    """Register standard RFC 7807 problem details exception handler."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": "about:blank",
                "title": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
                "status": exc.status_code,
                "detail": str(exc.detail),
                "instance": request.url.path,
                "correlation_id": correlation_id,
            },
            headers={"X-Correlation-ID": correlation_id},
        )


def register_health_probes(app: FastAPI) -> None:
    """Register Kubernetes-standard liveness and readiness probe endpoints."""

    @app.get("/healthz", tags=["Observability"], summary="Liveness probe")
    def liveness() -> dict[str, str]:
        """Returns 200 OK if the application process is running."""
        return {"status": "alive"}

    @app.get("/readyz", tags=["Observability"], summary="Readiness probe")
    def readiness() -> dict[str, str]:
        """Returns 200 OK if the application is ready to accept user traffic."""
        # In real systems, verify DB connection, Redis, downstream dependencies here
        return {"status": "ready"}
