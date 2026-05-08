"""Object-oriented programming fundamentals: classes, encapsulation, and basic patterns.

This module demonstrates core OOP concepts including:
- Class definition and instantiation
- Encapsulation with private attributes
- Property decorators for controlled access
- Class and instance methods
- Basic inheritance patterns

Python version: 3.10+
"""

from __future__ import annotations

from typing import Any


class BankAccount:
    """A simple bank account with encapsulation and validation.

    This class demonstrates encapsulation by hiding the balance
    and providing controlled access through properties and methods.
    """

    def __init__(self, account_holder: str, initial_balance: float = 0.0) -> None:
        """Initialize a bank account.

        Args:
            account_holder: Name of the account holder.
            initial_balance: Starting balance (must be non-negative).

        Raises:
            ValueError: If initial_balance is negative.
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_holder = account_holder
        self._balance = initial_balance  # Private attribute

    @property
    def balance(self) -> float:
        """Get the current account balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit money into the account.

        Args:
            amount: Amount to deposit (must be positive).

        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account.

        Args:
            amount: Amount to withdraw (must be positive and not exceed balance).

        Raises:
            ValueError: If amount is invalid or insufficient funds.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def __str__(self) -> str:
        """Return string representation of the account."""
        return f"BankAccount(holder='{self.account_holder}', balance={self._balance})"


class Rectangle:
    """A rectangle with calculated properties.

    Demonstrates property decorators and computed attributes.
    """

    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle.

        Args:
            width: Width of the rectangle (must be positive).
            height: Height of the rectangle (must be positive).

        Raises:
            ValueError: If dimensions are not positive.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")

        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        """Get the width of the rectangle."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the width of the rectangle.

        Args:
            value: New width (must be positive).

        Raises:
            ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self) -> float:
        """Get the height of the rectangle."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set the height of the rectangle.

        Args:
            value: New height (must be positive).

        Raises:
            ValueError: If value is not positive.
        """
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle."""
        return 2 * (self._width + self._height)

    def __str__(self) -> str:
        """Return string representation of the rectangle."""
        return f"Rectangle(width={self._width}, height={self._height})"


class Counter:
    """A simple counter with class and instance methods.

    Demonstrates class variables, class methods, and instance methods.
    """

    # Class variable shared by all instances
    total_instances = 0

    def __init__(self, start: int = 0) -> None:
        """Initialize a counter.

        Args:
            start: Starting value for the counter.
        """
        self.value = start
        Counter.total_instances += 1

    def increment(self) -> None:
        """Increment the counter by 1."""
        self.value += 1

    def decrement(self) -> None:
        """Decrement the counter by 1."""
        self.value -= 1

    def reset(self) -> None:
        """Reset the counter to 0."""
        self.value = 0

    @classmethod
    def get_total_instances(cls) -> int:
        """Get the total number of Counter instances created.

        Returns:
            Total number of instances.
        """
        return cls.total_instances

    @classmethod
    def create_from_list(cls, values: list[int]) -> 'Counter':
        """Create a counter initialized with the sum of a list.

        Args:
            values: List of integers to sum.

        Returns:
            New Counter instance.
        """
        return cls(sum(values))

    def __str__(self) -> str:
        """Return string representation of the counter."""
        return f"Counter(value={self.value})"