"""Comprehensive mocking patterns using unittest.mock.

Demonstrates MagicMock, Mock, patch decorators, patch context managers,
autospec, side_effect sequences, AsyncMock, and real-world service mocking.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, create_autospec, patch


# ---------------------------------------------------------------------------
# Example Domain: Order & Notification Service
# ---------------------------------------------------------------------------


class PaymentGatewayClient:
    """Client for external third-party payment gateway."""

    def charge(self, user_id: str, amount_cents: int) -> dict[str, Any]:
        # Real implementation would make HTTP call
        raise NotImplementedError("Real gateway requires network access")

    def refund(self, transaction_id: str) -> bool:
        raise NotImplementedError("Real gateway requires network access")


class EmailClient:
    """Client for transactional emails."""

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        raise NotImplementedError("Real email requires SMTP/API access")


class OrderService:
    """Business logic orchestrating payment and notification."""

    def __init__(self, payment_client: PaymentGatewayClient, email_client: EmailClient) -> None:
        self.payment_client = payment_client
        self.email_client = email_client

    def checkout(self, user_id: str, email: str, amount_cents: int) -> dict[str, Any]:
        if amount_cents <= 0:
            raise ValueError("Amount must be positive.")

        charge_result = self.payment_client.charge(user_id=user_id, amount_cents=amount_cents)

        if not charge_result.get("success"):
            return {"status": "failed", "error": charge_result.get("error", "Charge failed")}

        tx_id = charge_result["transaction_id"]
        self.email_client.send_email(
            recipient=email,
            subject="Order Confirmation",
            body=f"Thank you for your order! Tx ID: {tx_id}",
        )

        return {"status": "completed", "transaction_id": tx_id}


# ---------------------------------------------------------------------------
# Mock Demonstration Functions
# ---------------------------------------------------------------------------


def demo_basic_mock() -> None:
    """Demonstrate basic Mock and MagicMock return values and assertions."""
    mock = MagicMock()
    mock.calculate.return_value = 42

    result = mock.calculate(10, factor=2)
    assert result == 42
    mock.calculate.assert_called_once_with(10, factor=2)
    print("✓ Basic MagicMock and call assertions verified.")


def demo_side_effects() -> None:
    """Demonstrate side_effects for exceptions, sequential returns, and dynamic callables."""
    # 1. Raising exceptions
    error_mock = Mock(side_effect=ConnectionError("Database unavailable"))
    try:
        error_mock()
    except ConnectionError:
        print("✓ Mock side_effect exception verified.")

    # 2. Sequential return values (e.g. retry simulation)
    retry_mock = Mock(side_effect=[False, False, True])
    results = [retry_mock() for _ in range(3)]
    assert results == [False, False, True]
    print("✓ Mock sequential return values verified.")

    # 3. Dynamic callable side effect
    double_mock = Mock(side_effect=lambda x: x * 2)
    assert double_mock(21) == 42
    print("✓ Mock dynamic callable side effect verified.")


def demo_service_mocking() -> None:
    """Demonstrate mocking domain dependencies with autospec."""
    # Use create_autospec to guarantee mocks conform strictly to real interfaces
    mock_payment = create_autospec(PaymentGatewayClient, instance=True)
    mock_email = create_autospec(EmailClient, instance=True)

    # Configure mock responses
    mock_payment.charge.return_value = {"success": True, "transaction_id": "tx_998877"}
    mock_email.send_email.return_value = True

    service = OrderService(payment_client=mock_payment, email_client=mock_email)
    outcome = service.checkout(user_id="usr_1", email="alice@example.com", amount_cents=5000)

    assert outcome["status"] == "completed"
    assert outcome["transaction_id"] == "tx_998877"

    mock_payment.charge.assert_called_once_with(user_id="usr_1", amount_cents=5000)
    mock_email.send_email.assert_called_once_with(
        recipient="alice@example.com",
        subject="Order Confirmation",
        body="Thank you for your order! Tx ID: tx_998877",
    )
    print("✓ Domain service checkout flow mocked and verified.")


def demo_patch_decorator_and_context() -> None:
    """Demonstrate patch as context manager and decorator."""
    with patch("os.getenv", return_value="production") as mock_env:
        import os

        env_val = os.getenv("ENVIRONMENT")
        assert env_val == "production"
        mock_env.assert_called_once_with("ENVIRONMENT")

    print("✓ patch context manager verified.")


async def demo_async_mock() -> None:
    """Demonstrate AsyncMock for coroutines and asynchronous APIs."""

    class AsyncDataFetcher:
        async def fetch_user_data(self, user_id: int) -> dict[str, str]:
            await asyncio.sleep(0.01)
            return {"user_id": str(user_id), "name": "Real Name"}

    mock_fetcher = create_autospec(AsyncDataFetcher, instance=True)
    mock_fetcher.fetch_user_data = AsyncMock(return_value={"user_id": "42", "name": "Mocked Name"})

    data = await mock_fetcher.fetch_user_data(42)
    assert data["name"] == "Mocked Name"
    mock_fetcher.fetch_user_data.assert_awaited_once_with(42)
    print("✓ AsyncMock coroutine mocking and assertion verified.")


def run_all() -> None:
    print("\n--- Testing: Mocking Patterns ---")
    demo_basic_mock()
    demo_side_effects()
    demo_service_mocking()
    demo_patch_decorator_and_context()
    asyncio.run(demo_async_mock())


if __name__ == "__main__":
    run_all()
