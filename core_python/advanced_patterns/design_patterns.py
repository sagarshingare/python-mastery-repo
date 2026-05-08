"""Advanced Python patterns and design patterns.

This module demonstrates advanced programming patterns including:
- Singleton pattern
- Factory pattern
- Observer pattern
- Strategy pattern
- Decorator pattern

Python version: 3.10+
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Protocol


# Singleton Pattern
class SingletonMeta(type):
    """Metaclass for implementing the Singleton pattern."""

    _instances: Dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create or return the singleton instance."""
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """Database connection using Singleton pattern."""

    def __init__(self, host: str = "localhost", port: int = 5432) -> None:
        """Initialize database connection."""
        self.host = host
        self.port = port
        self._connected = False

    def connect(self) -> str:
        """Connect to the database."""
        if not self._connected:
            self._connected = True
            return f"Connected to database at {self.host}:{self.port}"
        return "Already connected"

    def disconnect(self) -> str:
        """Disconnect from the database."""
        if self._connected:
            self._connected = False
            return "Disconnected from database"
        return "Not connected"


# Factory Pattern
class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def area(self) -> float:
        """Calculate area of the shape."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter of the shape."""
        ...


class Circle(Shape):
    """Circle shape."""

    def __init__(self, radius: float) -> None:
        """Initialize circle with radius."""
        self.radius = radius

    def area(self) -> float:
        """Calculate circle area."""
        return 3.14159 * self.radius * self.radius

    def perimeter(self) -> float:
        """Calculate circle perimeter."""
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    """Rectangle shape."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize rectangle with width and height."""
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate rectangle area."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Calculate rectangle perimeter."""
        return 2 * (self.width + self.height)


class ShapeFactory:
    """Factory for creating shapes."""

    @staticmethod
    def create_shape(shape_type: str, **kwargs: Any) -> Shape:
        """Create a shape based on type."""
        if shape_type == "circle":
            return Circle(kwargs["radius"])
        elif shape_type == "rectangle":
            return Rectangle(kwargs["width"], kwargs["height"])
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")


# Observer Pattern
class Observer(Protocol):
    """Protocol for observers."""

    def update(self, message: str) -> None:
        """Update method called by subject."""
        ...


class Subject:
    """Subject that observers can subscribe to."""

    def __init__(self) -> None:
        """Initialize subject with empty observers list."""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(message)


class EmailNotifier:
    """Email notification observer."""

    def update(self, message: str) -> None:
        """Send email notification."""
        print(f"Email: {message}")


class SMSNotifier:
    """SMS notification observer."""

    def update(self, message: str) -> None:
        """Send SMS notification."""
        print(f"SMS: {message}")


# Strategy Pattern
class PaymentStrategy(ABC):
    """Abstract payment strategy."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Process payment."""
        ...


class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy."""

    def pay(self, amount: float) -> str:
        """Process credit card payment."""
        return f"Paid ${amount} with credit card"


class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy."""

    def pay(self, amount: float) -> str:
        """Process PayPal payment."""
        return f"Paid ${amount} with PayPal"


class PaymentProcessor:
    """Payment processor using strategy pattern."""

    def __init__(self, strategy: PaymentStrategy) -> None:
        """Initialize with payment strategy."""
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        """Change payment strategy."""
        self._strategy = strategy

    def process_payment(self, amount: float) -> str:
        """Process payment using current strategy."""
        return self._strategy.pay(amount)


# Decorator Pattern
class Coffee(ABC):
    """Abstract coffee base class."""

    @abstractmethod
    def cost(self) -> float:
        """Get cost of coffee."""
        ...

    @abstractmethod
    def description(self) -> str:
        """Get description of coffee."""
        ...


class SimpleCoffee(Coffee):
    """Basic coffee."""

    def cost(self) -> float:
        """Cost of simple coffee."""
        return 2.0

    def description(self) -> str:
        """Description of simple coffee."""
        return "Simple coffee"


class CoffeeDecorator(Coffee):
    """Base decorator for coffee."""

    def __init__(self, coffee: Coffee) -> None:
        """Initialize with decorated coffee."""
        self._coffee = coffee

    def cost(self) -> float:
        """Get cost including decorator."""
        return self._coffee.cost()

    def description(self) -> str:
        """Get description including decorator."""
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    """Milk decorator."""

    def cost(self) -> float:
        """Cost with milk."""
        return self._coffee.cost() + 0.5

    def description(self) -> str:
        """Description with milk."""
        return f"{self._coffee.description()} with milk"


class SugarDecorator(CoffeeDecorator):
    """Sugar decorator."""

    def cost(self) -> float:
        """Cost with sugar."""
        return self._coffee.cost() + 0.2

    def description(self) -> str:
        """Description with sugar."""
        return f"{self._coffee.description()} with sugar"