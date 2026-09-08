"""Run metaclass and __init_subclass__ examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
from core_python.metaclasses.metaclass_examples import (
    AttributeTrackerMeta,
    BaseTrackedModel,
    InterfaceEnforcerMeta,
    PluginRegistryBase,
    SingletonMeta,
)

logger = logging.getLogger(__name__)


def run_attribute_tracker() -> None:
    """Demonstrate attribute tracking metaclass."""
    print("\n--- Attribute Tracker Metaclass ---")

    class UserAccountModel(BaseTrackedModel):
        username = "anonymous"
        access_level = 1

        def describe(self) -> str:
            return f"{self.username}:{self.access_level}"

    print(f"  Class: {UserAccountModel.__name__}")
    print(f"  Tracked attributes: {UserAccountModel._tracked_attributes}")
    assert "username" in UserAccountModel._tracked_attributes
    assert "access_level" in UserAccountModel._tracked_attributes


def run_singleton_metaclass() -> None:
    """Demonstrate singleton metaclass pattern."""
    print("\n--- Singleton Metaclass ---")

    class AppConfig(metaclass=SingletonMeta):
        def __init__(self) -> None:
            self.debug = False
            self.database_url = "sqlite:///app.db"

    config1 = AppConfig()
    config2 = AppConfig()
    print(f"  config1 is config2: {config1 is config2}")
    assert config1 is config2

    config1.debug = True
    print(f"  config2.debug (after config1 modification): {config2.debug}")
    assert config2.debug is True


def run_validation_metaclass() -> None:
    """Demonstrate metaclass that enforces class contracts."""
    print("\n--- Validation Metaclass ---")

    class WorkerMeta(InterfaceEnforcerMeta):
        required_methods = ["process", "cleanup"]

    class WorkerBase(metaclass=WorkerMeta):
        pass

    class ValidWorker(WorkerBase):
        def process(self) -> str:
            return "processing"

        def cleanup(self) -> str:
            return "cleaned"

    worker = ValidWorker()
    print(f"  ValidWorker instantiated successfully: {worker.process()}, {worker.cleanup()}")

    try:
        class IncompleteWorker(WorkerBase):  # type: ignore[misc]
            def process(self) -> str:
                return "only process"

    except TypeError as err:
        print(f"  Caught expected contract violation: {err}")


def run_init_subclass_examples() -> None:
    """Demonstrate modern PEP 487 __init_subclass__ registry pattern."""
    print("\n--- Modern __init_subclass__ Pattern ---")

    class AuthPlugin(PluginRegistryBase, plugin_name="oauth2"):
        def authenticate(self) -> str:
            return "authenticated via oauth2"

    class JwtPlugin(PluginRegistryBase, plugin_name="jwt"):
        def authenticate(self) -> str:
            return "authenticated via jwt"

    plugins = PluginRegistryBase.list_plugins()
    print(f"  Registered plugins in registry: {plugins}")
    assert "oauth2" in plugins
    assert "jwt" in plugins

    plugin_cls = PluginRegistryBase.get_plugin("oauth2")
    assert plugin_cls is not None
    print(f"  Instantiated {plugin_cls.__name__}: {plugin_cls().authenticate()}")


def main() -> None:
    """Main entry point for metaclass examples."""
    parser = argparse.ArgumentParser(description="Run metaclass examples")
    parser.add_argument(
        "--module",
        choices=["tracker", "singleton", "validation", "subclass", "all"],
        default="all",
        help="Specific example to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "tracker":
        run_attribute_tracker()
    elif args.module == "singleton":
        run_singleton_metaclass()
    elif args.module == "validation":
        run_validation_metaclass()
    elif args.module == "subclass":
        run_init_subclass_examples()
    else:
        run_attribute_tracker()
        run_singleton_metaclass()
        run_validation_metaclass()
        run_init_subclass_examples()


if __name__ == "__main__":
    main()
