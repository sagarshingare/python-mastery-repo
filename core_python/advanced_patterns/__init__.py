"""
Advanced Design Patterns Module.
===============================
Covers classic GoF patterns in Python:
- Singleton Pattern
- Factory Pattern
- Observer Pattern
- Strategy Pattern
- Decorator Pattern
"""

from .design_patterns import (
    Circle,
    Coffee,
    CoffeeDecorator,
    CreditCardStrategy,
    DatabaseConnection,
    EmailNotifier,
    MilkDecorator,
    Observer,
    PaymentProcessor,
    PaymentStrategy,
    PayPalStrategy,
    Rectangle,
    Shape,
    ShapeFactory,
    SMSNotifier,
    Subject,
    SugarDecorator,
)

__all__ = [
    "Circle",
    "Coffee",
    "CoffeeDecorator",
    "CreditCardStrategy",
    "DatabaseConnection",
    "EmailNotifier",
    "MilkDecorator",
    "Observer",
    "PaymentProcessor",
    "PaymentStrategy",
    "PayPalStrategy",
    "Rectangle",
    "Shape",
    "ShapeFactory",
    "SMSNotifier",
    "Subject",
    "SugarDecorator",
]
