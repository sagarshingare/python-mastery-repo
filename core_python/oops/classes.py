"""Object-oriented programming examples for enterprise-ready Python.

This module demonstrates core OOP concepts including:
- Class definition and instantiation
- Data classes for simple data structures
- Order processing with business logic
- Revenue calculation and reporting

Python version: 3.10+
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Order:
    """An immutable order with calculated properties.

    Demonstrates data classes and computed properties.
    """
    product_name: str
    quantity: int
    unit_price: float

    def __post_init__(self) -> None:
        """Validate order data after initialization."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")

    @property
    def total_price(self) -> float:
        """Calculate total price for this order.

        Returns:
            Total price rounded to 2 decimal places.
        """
        return round(self.quantity * self.unit_price, 2)

    @property
    def is_bulk_order(self) -> bool:
        """Check if this is a bulk order.

        Returns:
            True if quantity >= 100.
        """
        return self.quantity >= 100

    def apply_discount(self, discount_percent: float) -> 'Order':
        """Create a new order with discount applied.

        Args:
            discount_percent: Discount percentage (0-100).

        Returns:
            New Order instance with discounted price.

        Raises:
            ValueError: If discount is invalid.
        """
        if not 0 <= discount_percent <= 100:
            raise ValueError("Discount must be between 0 and 100")

        discounted_price = self.unit_price * (1 - discount_percent / 100)
        return Order(self.product_name, self.quantity, discounted_price)


@dataclass
class Customer:
    """A customer with order history.

    Demonstrates mutable data classes and relationships.
    """
    id: int
    name: str
    email: str
    orders: list[Order] = None

    def __post_init__(self) -> None:
        """Initialize orders list if not provided."""
        if self.orders is None:
            self.orders = []

    @property
    def total_spent(self) -> float:
        """Calculate total amount spent by customer.

        Returns:
            Total spent across all orders.
        """
        return sum(order.total_price for order in self.orders)

    @property
    def order_count(self) -> int:
        """Get number of orders.

        Returns:
            Number of orders placed.
        """
        return len(self.orders)

    def add_order(self, order: Order) -> None:
        """Add an order to customer's history.

        Args:
            order: Order to add.
        """
        self.orders.append(order)

    def get_loyalty_status(self) -> str:
        """Determine customer loyalty status.

        Returns:
            Loyalty status based on spending.
        """
        spent = self.total_spent
        if spent >= 1000:
            return "Platinum"
        elif spent >= 500:
            return "Gold"
        elif spent >= 100:
            return "Silver"
        else:
            return "Bronze"


class OrderProcessor:
    """Business logic for processing orders.

    Demonstrates classes with complex behavior.
    """

    def __init__(self) -> None:
        """Initialize order processor."""
        self._processed_orders: list[Order] = []
        self._total_revenue = 0.0

    def process_order(self, order: Order) -> dict[str, any]:
        """Process a single order.

        Args:
            order: Order to process.

        Returns:
            Processing result.
        """
        self._processed_orders.append(order)
        self._total_revenue += order.total_price

        logger.info("Processed order: %s x%d @ $%.2f = $%.2f",
                   order.product_name, order.quantity,
                   order.unit_price, order.total_price)

        return {
            "success": True,
            "order": order,
            "revenue_added": order.total_price,
            "is_bulk": order.is_bulk_order
        }

    def process_orders(self, orders: Iterable[Order]) -> dict[str, any]:
        """Process multiple orders.

        Args:
            orders: Orders to process.

        Returns:
            Processing summary.
        """
        results = []
        total_revenue = 0.0
        bulk_orders = 0

        for order in orders:
            result = self.process_order(order)
            results.append(result)
            total_revenue += result["revenue_added"]
            if result["is_bulk"]:
                bulk_orders += 1

        return {
            "total_orders": len(results),
            "total_revenue": total_revenue,
            "bulk_orders": bulk_orders,
            "results": results
        }

    @property
    def total_revenue(self) -> float:
        """Get total revenue processed.

        Returns:
            Total revenue.
        """
        return self._total_revenue

    @property
    def processed_count(self) -> int:
        """Get number of processed orders.

        Returns:
            Number of orders processed.
        """
        return len(self._processed_orders)


def calculate_total_revenue(orders: Iterable[Order]) -> float:
    """Calculate total revenue from orders.

    Args:
        orders: Orders to calculate revenue for.

    Returns:
        Total revenue rounded to 2 decimal places.
    """
    total = 0.0
    for order in orders:
        total += order.total_price
        logger.debug("Added order %s revenue %s", order.product_name, order.total_price)

    revenue = round(total, 2)
    logger.info("Total revenue computed: %s", revenue)
    return revenue


def get_revenue_by_product(orders: Iterable[Order]) -> dict[str, float]:
    """Calculate revenue grouped by product.

    Args:
        orders: Orders to analyze.

    Returns:
        Dictionary mapping product names to revenue.
    """
    revenue_by_product = {}
    for order in orders:
        product = order.product_name
        revenue_by_product[product] = revenue_by_product.get(product, 0) + order.total_price

    return revenue_by_product
