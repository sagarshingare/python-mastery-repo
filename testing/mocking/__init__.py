"""Mocking patterns and examples package."""

from testing.mocking.mock_examples import (
    EmailClient,
    OrderService,
    PaymentGatewayClient,
    demo_basic_mock,
    demo_service_mocking,
    demo_side_effects,
    run_all,
)

__all__ = [
    "PaymentGatewayClient",
    "EmailClient",
    "OrderService",
    "demo_basic_mock",
    "demo_side_effects",
    "demo_service_mocking",
    "run_all",
]
