"""Object-oriented programming: inheritance and method overriding.

This module demonstrates inheritance patterns including:
- Single inheritance
- Method overriding
- Calling parent methods with super()
- Multiple inheritance and method resolution order
- Abstract base classes

Python version: 3.10+
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Any


class Vehicle:
    """Base class for all vehicles.

    Demonstrates basic inheritance structure.
    """

    def __init__(self, make: str, model: str, year: int) -> None:
        """Initialize a vehicle.

        Args:
            make: Vehicle manufacturer.
            model: Vehicle model name.
            year: Manufacturing year.
        """
        self.make = make
        self.model = model
        self.year = year

    def get_description(self) -> str:
        """Get a description of the vehicle.

        Returns:
            Formatted description string.
        """
        return f"{self.year} {self.make} {self.model}"

    def start_engine(self) -> str:
        """Start the vehicle engine.

        Returns:
            Engine start message.
        """
        return "Engine started"

    def __str__(self) -> str:
        """Return string representation of the vehicle."""
        return self.get_description()


class Car(Vehicle):
    """A car that inherits from Vehicle.

    Demonstrates single inheritance and method overriding.
    """

    def __init__(self, make: str, model: str, year: int, num_doors: int = 4) -> None:
        """Initialize a car.

        Args:
            make: Car manufacturer.
            model: Car model name.
            year: Manufacturing year.
            num_doors: Number of doors.
        """
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def get_description(self) -> str:
        """Get a detailed description of the car.

        Returns:
            Formatted description including doors.
        """
        base_desc = super().get_description()
        return f"{base_desc} ({self.num_doors}-door)"

    def start_engine(self) -> str:
        """Start the car engine with car-specific behavior.

        Returns:
            Car engine start message.
        """
        base_message = super().start_engine()
        return f"{base_message} - Car systems initialized"


class ElectricCar(Car):
    """An electric car that inherits from Car.

    Demonstrates multi-level inheritance.
    """

    def __init__(self, make: str, model: str, year: int, battery_capacity: float) -> None:
        """Initialize an electric car.

        Args:
            make: Car manufacturer.
            model: Car model name.
            year: Manufacturing year.
            battery_capacity: Battery capacity in kWh.
        """
        super().__init__(make, model, year, num_doors=4)
        self.battery_capacity = battery_capacity
        self._charge_level = 100.0  # Start fully charged

    @property
    def charge_level(self) -> float:
        """Get the current battery charge level."""
        return self._charge_level

    def start_engine(self) -> str:
        """Start the electric car.

        Returns:
            Electric start message.
        """
        if self._charge_level < 10:
            return "Cannot start: Battery too low"
        return "Electric motor started - Silent and smooth"

    def charge(self, amount: float) -> None:
        """Charge the battery.

        Args:
            amount: Amount to charge (0-100).
        """
        self._charge_level = min(100.0, self._charge_level + amount)


class Motorcycle(Vehicle):
    """A motorcycle that inherits from Vehicle.

    Demonstrates inheritance with different behavior.
    """

    def __init__(self, make: str, model: str, year: int, has_sidecar: bool = False) -> None:
        """Initialize a motorcycle.

        Args:
            make: Motorcycle manufacturer.
            model: Motorcycle model name.
            year: Manufacturing year.
            has_sidecar: Whether the motorcycle has a sidecar.
        """
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def get_description(self) -> str:
        """Get a description of the motorcycle.

        Returns:
            Formatted description including sidecar info.
        """
        base_desc = super().get_description()
        sidecar_info = " with sidecar" if self.has_sidecar else ""
        return f"{base_desc}{sidecar_info}"


# Abstract base class example
class Shape(ABC):
    """Abstract base class for geometric shapes.

    Demonstrates abstract methods and inheritance contracts.
    """

    def __init__(self, name: str) -> None:
        """Initialize a shape.

        Args:
            name: Name of the shape.
        """
        self.name = name

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape.

        Returns:
            Area of the shape.
        """
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape.

        Returns:
            Perimeter of the shape.
        """
        pass

    def describe(self) -> str:
        """Get a description of the shape.

        Returns:
            Description string.
        """
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    """A circle that implements the Shape interface."""

    def __init__(self, radius: float) -> None:
        """Initialize a circle.

        Args:
            radius: Radius of the circle (must be positive).

        Raises:
            ValueError: If radius is not positive.
        """
        if radius <= 0:
            raise ValueError("Radius must be positive")
        super().__init__("Circle")
        self.radius = radius

    def area(self) -> float:
        """Calculate the area of the circle.

        Returns:
            Area of the circle.
        """
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        """Calculate the perimeter (circumference) of the circle.

        Returns:
            Circumference of the circle.
        """
        return 2 * math.pi * self.radius


class Square(Shape):
    """A square that implements the Shape interface."""

    def __init__(self, side: float) -> None:
        """Initialize a square.

        Args:
            side: Length of a side (must be positive).

        Raises:
            ValueError: If side is not positive.
        """
        if side <= 0:
            raise ValueError("Side must be positive")
        super().__init__("Square")
        self.side = side

    def area(self) -> float:
        """Calculate the area of the square.

        Returns:
            Area of the square.
        """
        return self.side ** 2

    def perimeter(self) -> float:
        """Calculate the perimeter of the square.

        Returns:
            Perimeter of the square.
        """
        return 4 * self.side


# Multiple inheritance example
class LoggerMixin:
    """Mixin class that adds logging capabilities."""

    def log_action(self, action: str) -> None:
        """Log an action.

        Args:
            action: Action to log.
        """
        print(f"[LOG] {self.__class__.__name__}: {action}")


class TimestampMixin:
    """Mixin class that adds timestamp capabilities."""

    def get_timestamp(self) -> str:
        """Get current timestamp.

        Returns:
            Current timestamp string.
        """
        from datetime import datetime
        return datetime.now().isoformat()


class AdvancedVehicle(Vehicle, LoggerMixin, TimestampMixin):
    """Vehicle with logging and timestamp capabilities.

    Demonstrates multiple inheritance with mixins.
    """

    def start_engine(self) -> str:
        """Start the engine with logging.

        Returns:
            Engine start message.
        """
        message = super().start_engine()
        self.log_action(f"Engine started at {self.get_timestamp()}")
        return message