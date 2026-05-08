"""Run Python OOP examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from core_python.oops.abstraction import (
    CreditCardProcessor,
    PayPalProcessor,
    ShapeFactory,
    Sorter,
)
from core_python.oops.classes_basics import BankAccount, Counter, Rectangle
from core_python.oops.inheritance import AdvancedVehicle, Car, ElectricCar
from core_python.oops.polymorphism import Dog, Cat, Vector, Painter

logger = logging.getLogger(__name__)


def run_classes_basics_examples() -> None:
    """Demonstrate basic class concepts."""
    logger.info("Running classes basics examples")

    # BankAccount example
    account = BankAccount("John Doe", 1000.0)
    print(f"Created account: {account}")
    account.deposit(500.0)
    print(f"After deposit: {account}")
    account.withdraw(200.0)
    print(f"After withdrawal: {account}")

    # Rectangle example
    rect = Rectangle(10.0, 5.0)
    print(f"Rectangle area: {rect.area}")
    print(f"Rectangle perimeter: {rect.perimeter}")

    # Counter example
    counter = Counter()
    counter.increment()
    counter.increment()
    print(f"Counter value: {counter.value}")


def run_inheritance_examples() -> None:
    """Demonstrate inheritance concepts."""
    logger.info("Running inheritance examples")

    car = Car("Toyota", "Camry", 2020, 4)
    print(f"Car description: {car.get_description()}")
    print(f"Car start: {car.start_engine()}")
    print(f"Car fuel efficiency: {car.get_fuel_efficiency()}")

    electric_car = ElectricCar("Tesla", "Model 3", 2023, 75)
    print(f"Electric car description: {electric_car.get_description()}")
    print(f"Electric car start: {electric_car.start_engine()}")
    print(f"Electric car range: {electric_car.get_range()}")

    advanced_vehicle = AdvancedVehicle("BMW", "X5", 2022)
    print(f"Advanced vehicle: {advanced_vehicle.get_description()}")
    advanced_vehicle.log_action("Started")


def run_polymorphism_examples() -> None:
    """Demonstrate polymorphism concepts."""
    logger.info("Running polymorphism examples")

    dog = Dog("Buddy")
    cat = Cat("Whiskers")

    print(f"Dog speak: {dog.speak()}")
    print(f"Cat speak: {cat.speak()}")

    # Vector operations
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 * 2 = {v1 * 2}")

    # Painter with different shapes
    painter = Painter()
    painter.add_shape("circle", 5)
    painter.add_shape("rectangle", 10, 20)
    painter.add_shape("text", "Hello World")
    painter.draw_all()


def run_abstraction_examples() -> None:
    """Demonstrate abstraction concepts."""
    logger.info("Running abstraction examples")

    # Payment processors
    credit_processor = CreditCardProcessor("1234-5678-9012-3456")
    paypal_processor = PayPalProcessor("user@example.com")

    print(f"Credit card validation: {credit_processor.validate_payment(100.0)}")
    print(f"PayPal validation: {paypal_processor.validate_payment(50.0)}")

    # Shape factory
    factory = ShapeFactory()
    circle = factory.create_shape("circle", radius=5)
    rectangle = factory.create_shape("rectangle", width=10, height=20)
    triangle = factory.create_shape("triangle", base=6, height=8)

    print(f"Circle area: {circle.area()}")
    print(f"Rectangle area: {rectangle.area()}")
    print(f"Triangle area: {triangle.area()}")

    # Sorter with different strategies
    sorter = Sorter()
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original data: {data}")
    sorter.sort(data.copy(), "bubble")
    sorter.sort(data.copy(), "quick")


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python OOP examples")
    parser.add_argument(
        "--module",
        choices=["classes_basics", "inheritance", "polymorphism", "abstraction"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "classes_basics":
        run_classes_basics_examples()
    elif args.module == "inheritance":
        run_inheritance_examples()
    elif args.module == "polymorphism":
        run_polymorphism_examples()
    elif args.module == "abstraction":
        run_abstraction_examples()
    else:
        # Run all examples
        run_classes_basics_examples()
        run_inheritance_examples()
        run_polymorphism_examples()
        run_abstraction_examples()


if __name__ == "__main__":
    main()