"""Object-oriented programming: polymorphism and duck typing.

This module demonstrates polymorphism patterns including:
- Method overriding and dynamic dispatch
- Duck typing in Python
- Operator overloading
- Polymorphic functions
- Abstract base classes and protocols

Python version: 3.10+
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol


# Protocol-based polymorphism (structural typing)
class Drawable(Protocol):
    """Protocol for objects that can be drawn."""

    def draw(self) -> str:
        """Draw the object.

        Returns:
            String representation of the drawing.
        """
        ...


class Speakable(Protocol):
    """Protocol for objects that can speak."""

    def speak(self) -> str:
        """Make a sound.

        Returns:
            Sound made by the object.
        """
        ...


class Animal(ABC):
    """Abstract base class for animals.

    Demonstrates polymorphism through abstract methods.
    """

    def __init__(self, name: str) -> None:
        """Initialize an animal.

        Args:
            name: Name of the animal.
        """
        self.name = name

    @abstractmethod
    def speak(self) -> str:
        """Make the animal's sound.

        Returns:
            Sound made by the animal.
        """
        pass

    @abstractmethod
    def move(self) -> str:
        """Describe how the animal moves.

        Returns:
            Movement description.
        """
        pass

    def describe(self) -> str:
        """Get a description of the animal.

        Returns:
            Description string.
        """
        return f"{self.name} says '{self.speak()}' and {self.move()}"


class Dog(Animal):
    """A dog that implements the Animal interface."""

    def speak(self) -> str:
        """Dog's sound.

        Returns:
            Dog's bark.
        """
        return "Woof!"

    def move(self) -> str:
        """Dog's movement.

        Returns:
            Dog's movement description.
        """
        return "runs on four legs"


class Cat(Animal):
    """A cat that implements the Animal interface."""

    def speak(self) -> str:
        """Cat's sound.

        Returns:
            Cat's meow.
        """
        return "Meow!"

    def move(self) -> str:
        """Cat's movement.

        Returns:
            Cat's movement description.
        """
        return "walks gracefully"


class Bird(Animal):
    """A bird that implements the Animal interface."""

    def speak(self) -> str:
        """Bird's sound.

        Returns:
            Bird's chirp.
        """
        return "Chirp!"

    def move(self) -> str:
        """Bird's movement.

        Returns:
            Bird's movement description.
        """
        return "flies through the air"


def animal_sounds(animals: list[Animal]) -> list[str]:
    """Get sounds from a list of animals (polymorphic function).

    Args:
        animals: List of animal instances.

    Returns:
        List of sounds from each animal.
    """
    return [animal.speak() for animal in animals]


def describe_animals(animals: list[Animal]) -> list[str]:
    """Describe a list of animals polymorphically.

    Args:
        animals: List of animal instances.

    Returns:
        List of descriptions.
    """
    return [animal.describe() for animal in animals]


# Operator overloading example
class Vector:
    """A 2D vector with operator overloading.

    Demonstrates polymorphism through operator methods.
    """

    def __init__(self, x: float, y: float) -> None:
        """Initialize a vector.

        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        """Add two vectors.

        Args:
            other: Another vector.

        Returns:
            Sum vector.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        """Subtract two vectors.

        Args:
            other: Another vector.

        Returns:
            Difference vector.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector:
        """Multiply vector by scalar.

        Args:
            scalar: Scalar value.

        Returns:
            Scaled vector.
        """
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other: Any) -> bool:
        """Check equality with another vector.

        Args:
            other: Object to compare.

        Returns:
            True if vectors are equal.
        """
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """String representation of the vector.

        Returns:
            Formatted vector string.
        """
        return f"Vector({self.x}, {self.y})"

    def magnitude(self) -> float:
        """Calculate the magnitude of the vector.

        Returns:
            Magnitude value.
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5


# Duck typing examples
class Painter:
    """A painter that works with drawable objects (duck typing)."""

    @staticmethod
    def draw_shape(shape: Drawable) -> str:
        """Draw any object that has a draw method.

        Args:
            shape: Object that implements the Drawable protocol.

        Returns:
            Drawing result.
        """
        return shape.draw()


class Circle:
    """A circle that can be drawn (duck typing)."""

    def __init__(self, radius: float) -> None:
        """Initialize a circle.

        Args:
            radius: Circle radius.
        """
        self.radius = radius

    def draw(self) -> str:
        """Draw the circle.

        Returns:
            Drawing description.
        """
        return f"Drawing a circle with radius {self.radius}"


class Rectangle:
    """A rectangle that can be drawn (duck typing)."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize a rectangle.

        Args:
            width: Rectangle width.
            height: Rectangle height.
        """
        self.width = width
        self.height = height

    def draw(self) -> str:
        """Draw the rectangle.

        Returns:
            Drawing description.
        """
        return f"Drawing a rectangle {self.width}x{self.height}"


class Text:
    """Text that can be drawn (duck typing)."""

    def __init__(self, content: str) -> None:
        """Initialize text.

        Args:
            content: Text content.
        """
        self.content = content

    def draw(self) -> str:
        """Draw the text.

        Returns:
            Text rendering description.
        """
        return f"Rendering text: '{self.content}'"


def render_scene(drawables: list[Drawable]) -> list[str]:
    """Render a scene with multiple drawable objects.

    Args:
        drawables: List of objects that can be drawn.

    Returns:
        List of drawing results.
    """
    painter = Painter()
    return [painter.draw_shape(item) for item in drawables]