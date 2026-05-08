"""Run Python advanced patterns examples with a simple CLI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from core_python.advanced_patterns.design_patterns import (
    CoffeeDecorator,
    DatabaseConnection,
    EmailNotifier,
    MilkDecorator,
    PaymentProcessor,
    PayPalPayment,
    ShapeFactory,
    SimpleCoffee,
    SMSNotifier,
    Subject,
    SugarDecorator,
)

logger = logging.getLogger(__name__)


def run_singleton_examples() -> None:
    """Demonstrate singleton pattern."""
    logger.info("Running singleton pattern examples")

    db1 = DatabaseConnection("host1", 5432)
    db2 = DatabaseConnection("host2", 5433)

    print(f"db1.connect() -> {db1.connect()}")
    print(f"db2.connect() -> {db2.connect()}")
    print(f"db1 is db2 -> {db1 is db2}")  # Should be True for singleton


def run_factory_examples() -> None:
    """Demonstrate factory pattern."""
    logger.info("Running factory pattern examples")

    circle = ShapeFactory.create_shape("circle", radius=5.0)
    rectangle = ShapeFactory.create_shape("rectangle", width=10.0, height=20.0)

    print(f"Circle area: {circle.area()}")
    print(f"Circle perimeter: {circle.perimeter()}")
    print(f"Rectangle area: {rectangle.area()}")
    print(f"Rectangle perimeter: {rectangle.perimeter()}")


def run_observer_examples() -> None:
    """Demonstrate observer pattern."""
    logger.info("Running observer pattern examples")

    subject = Subject()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()

    subject.attach(email_notifier)
    subject.attach(sms_notifier)

    print("Notifying observers:")
    subject.notify("System maintenance scheduled")

    subject.detach(email_notifier)
    print("Notifying remaining observers:")
    subject.notify("Maintenance completed")


def run_strategy_examples() -> None:
    """Demonstrate strategy pattern."""
    logger.info("Running strategy pattern examples")

    processor = PaymentProcessor(PayPalPayment())
    print(f"processor.process_payment(100.0) -> {processor.process_payment(100.0)}")

    processor.set_strategy(PayPalPayment())
    print(f"processor.process_payment(50.0) -> {processor.process_payment(50.0)}")


def run_decorator_examples() -> None:
    """Demonstrate decorator pattern."""
    logger.info("Running decorator pattern examples")

    coffee = SimpleCoffee()
    print(f"coffee.description() -> {coffee.description()}")
    print(f"coffee.cost() -> {coffee.cost()}")

    coffee_with_milk = MilkDecorator(coffee)
    print(f"coffee_with_milk.description() -> {coffee_with_milk.description()}")
    print(f"coffee_with_milk.cost() -> {coffee_with_milk.cost()}")

    fancy_coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
    print(f"fancy_coffee.description() -> {fancy_coffee.description()}")
    print(f"fancy_coffee.cost() -> {fancy_coffee.cost()}")


def main() -> None:
    """Main entry point for running examples."""
    parser = argparse.ArgumentParser(description="Run Python advanced patterns examples")
    parser.add_argument(
        "--module",
        choices=["singleton", "factory", "observer", "strategy", "decorator"],
        help="Specific module to run examples for",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.module == "singleton":
        run_singleton_examples()
    elif args.module == "factory":
        run_factory_examples()
    elif args.module == "observer":
        run_observer_examples()
    elif args.module == "strategy":
        run_strategy_examples()
    elif args.module == "decorator":
        run_decorator_examples()
    else:
        # Run all examples
        run_singleton_examples()
        run_factory_examples()
        run_observer_examples()
        run_strategy_examples()
        run_decorator_examples()


if __name__ == "__main__":
    main()