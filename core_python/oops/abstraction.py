"""Object-oriented programming: abstraction and design patterns.

This module demonstrates abstraction techniques including:
- Abstract base classes and interfaces
- Data classes for simple abstractions
- Factory patterns
- Strategy pattern
- Composition over inheritance

Python version: 3.10+
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


# Abstract base classes
class PaymentProcessor(ABC):
    """Abstract base class for payment processing.

    Demonstrates abstraction through interface definition.
    """

    @abstractmethod
    def process_payment(self, amount: float, currency: str = "USD") -> dict[str, Any]:
        """Process a payment.

        Args:
            amount: Payment amount.
            currency: Payment currency.

        Returns:
            Payment result dictionary.
        """
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> dict[str, Any]:
        """Refund a payment.

        Args:
            transaction_id: ID of transaction to refund.
            amount: Refund amount.

        Returns:
            Refund result dictionary.
        """
        pass

    def validate_amount(self, amount: float) -> bool:
        """Validate payment amount (concrete method).

        Args:
            amount: Amount to validate.

        Returns:
            True if amount is valid.
        """
        return amount > 0 and amount <= 10000  # Max $10k


class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor implementation."""

    def __init__(self, api_key: str) -> None:
        """Initialize credit card processor.

        Args:
            api_key: API key for payment gateway.
        """
        self.api_key = api_key

    def process_payment(self, amount: float, currency: str = "USD") -> dict[str, Any]:
        """Process credit card payment.

        Args:
            amount: Payment amount.
            currency: Payment currency.

        Returns:
            Payment result.
        """
        if not self.validate_amount(amount):
            return {"success": False, "error": "Invalid amount"}

        # Simulate payment processing
        return {
            "success": True,
            "transaction_id": f"cc_{hash(str(amount)) % 10000}",
            "amount": amount,
            "currency": currency,
            "method": "credit_card"
        }

    def refund_payment(self, transaction_id: str, amount: float) -> dict[str, Any]:
        """Process credit card refund.

        Args:
            transaction_id: Transaction to refund.
            amount: Refund amount.

        Returns:
            Refund result.
        """
        return {
            "success": True,
            "refund_id": f"refund_{transaction_id}",
            "amount": amount,
            "original_transaction": transaction_id
        }


class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor implementation."""

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Initialize PayPal processor.

        Args:
            client_id: PayPal client ID.
            client_secret: PayPal client secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret

    def process_payment(self, amount: float, currency: str = "USD") -> dict[str, Any]:
        """Process PayPal payment.

        Args:
            amount: Payment amount.
            currency: Payment currency.

        Returns:
            Payment result.
        """
        if not self.validate_amount(amount):
            return {"success": False, "error": "Invalid amount"}

        return {
            "success": True,
            "transaction_id": f"pp_{hash(str(amount)) % 10000}",
            "amount": amount,
            "currency": currency,
            "method": "paypal"
        }

    def refund_payment(self, transaction_id: str, amount: float) -> dict[str, Any]:
        """Process PayPal refund.

        Args:
            transaction_id: Transaction to refund.
            amount: Refund amount.

        Returns:
            Refund result.
        """
        return {
            "success": True,
            "refund_id": f"refund_{transaction_id}",
            "amount": amount,
            "original_transaction": transaction_id
        }


# Data classes for abstraction
@dataclass(frozen=True)
class User:
    """User data class with immutable properties.

    Demonstrates abstraction through data classes.
    """
    id: int
    username: str
    email: str
    is_active: bool = True

    def get_display_name(self) -> str:
        """Get display name for the user.

        Returns:
            Formatted display name.
        """
        return f"{self.username} ({self.email})"


@dataclass
class Product:
    """Product data class.

    Demonstrates mutable data abstraction.
    """
    id: int
    name: str
    price: float
    category: str

    def apply_discount(self, percentage: float) -> None:
        """Apply discount to product price.

        Args:
            percentage: Discount percentage (0-100).
        """
        if 0 <= percentage <= 100:
            self.price *= (1 - percentage / 100)

    def get_discounted_price(self, percentage: float) -> float:
        """Get price after discount (without modifying object).

        Args:
            percentage: Discount percentage.

        Returns:
            Discounted price.
        """
        if 0 <= percentage <= 100:
            return self.price * (1 - percentage / 100)
        return self.price


# Factory pattern
class ShapeFactory:
    """Factory for creating different shapes.

    Demonstrates factory pattern for object creation abstraction.
    """

    @staticmethod
    def create_circle(radius: float) -> 'Circle':
        """Create a circle.

        Args:
            radius: Circle radius.

        Returns:
            Circle instance.
        """
        return Circle(radius)

    @staticmethod
    def create_rectangle(width: float, height: float) -> 'Rectangle':
        """Create a rectangle.

        Args:
            width: Rectangle width.
            height: Rectangle height.

        Returns:
            Rectangle instance.
        """
        return Rectangle(width, height)

    @staticmethod
    def create_triangle(base: float, height: float) -> 'Triangle':
        """Create a triangle.

        Args:
            base: Triangle base.
            height: Triangle height.

        Returns:
            Triangle instance.
        """
        return Triangle(base, height)


class Shape(ABC):
    """Abstract shape class."""

    @abstractmethod
    def area(self) -> float:
        """Calculate area.

        Returns:
            Shape area.
        """
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter.

        Returns:
            Shape perimeter.
        """
        pass


class Circle(Shape):
    """Circle implementation."""

    def __init__(self, radius: float) -> None:
        """Initialize circle.

        Args:
            radius: Circle radius.
        """
        self.radius = radius

    def area(self) -> float:
        """Calculate circle area.

        Returns:
            Circle area.
        """
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        """Calculate circle perimeter.

        Returns:
            Circle circumference.
        """
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    """Rectangle implementation."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle.

        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate rectangle area.

        Returns:
            Rectangle area.
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate rectangle perimeter.

        Returns:
            Rectangle perimeter.
        """
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Triangle implementation."""

    def __init__(self, base: float, height: float) -> None:
        """Initialize triangle.

        Args:
            base: Triangle base.
            height: Triangle height.
        """
        self.base = base
        self.height = height

    def area(self) -> float:
        """Calculate triangle area.

        Returns:
            Triangle area.
        """
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        """Calculate triangle perimeter (approximate).

        Returns:
            Triangle perimeter approximation.
        """
        # Approximate perimeter for equilateral triangle
        side = math.sqrt((self.base/2)**2 + self.height**2)
        return self.base + 2 * side


# Strategy pattern
class SortingStrategy(ABC):
    """Abstract sorting strategy."""

    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        """Sort the data.

        Args:
            data: List to sort.

        Returns:
            Sorted list.
        """
        pass


class BubbleSortStrategy(SortingStrategy):
    """Bubble sort implementation."""

    def sort(self, data: list[int]) -> list[int]:
        """Sort using bubble sort.

        Args:
            data: List to sort.

        Returns:
            Sorted list.
        """
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortingStrategy):
    """Quick sort implementation."""

    def sort(self, data: list[int]) -> list[int]:
        """Sort using quick sort.

        Args:
            data: List to sort.

        Returns:
            Sorted list.
        """
        arr = data.copy()
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return self.sort(left) + middle + self.sort(right)


class Sorter:
    """Sorter that uses different sorting strategies."""

    def __init__(self, strategy: SortingStrategy) -> None:
        """Initialize sorter with strategy.

        Args:
            strategy: Sorting strategy to use.
        """
        self.strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        """Sort data using current strategy.

        Args:
            data: List to sort.

        Returns:
            Sorted list.
        """
        return self.strategy.sort(data)

    def set_strategy(self, strategy: SortingStrategy) -> None:
        """Change sorting strategy.

        Args:
            strategy: New sorting strategy.
        """
        self.strategy = strategy