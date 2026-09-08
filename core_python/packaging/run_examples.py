"""Run Python packaging and distribution examples with a simple CLI."""

from __future__ import annotations
import argparse
import logging
from pathlib import Path
from core_python.packaging.packaging_guide import (
    BuildSystem,
    ConsoleScript,
    DistributionType,
    PackageLayout,
    PackageMetadata,
    render_pyproject_toml,
    render_setup_py,
    validate_package_layout,
)

logger = logging.getLogger(__name__)


def run_packaging_metadata_examples() -> None:
    """Demonstrate packaging metadata and pyproject.toml generation."""
    print("\n--- Package Metadata & pyproject.toml ---")

    metadata = PackageMetadata(
        name="python-mastery-core",
        version="1.0.0",
        description="Core Python mastery curriculum and production patterns",
        author="Sagar Shingare",
        author_email="sagar@example.com",
        python_requires=">=3.9",
        keywords=["python", "mastery", "concurrency", "oop"],
        dependencies=["pydantic>=2.0", "fastapi>=0.100.0"],
    )

    toml_output = render_pyproject_toml(metadata)
    print("Rendered pyproject.toml preview:")
    for line in toml_output.strip().splitlines()[:12]:
        print(f"  {line}")


def run_console_script_and_distribution_examples() -> None:
    """Demonstrate console scripts and distribution formats."""
    print("\n--- Console Scripts & Distributions ---")

    cli = ConsoleScript("mastery-cli", "core_python.cli", "main")
    print(f"Entrypoint mapping: {cli.to_toml_entry()}")
    assert "mastery-cli" in cli.to_toml_entry()

    print("Distribution formats:")
    for dist in DistributionType:
        print(f"  - {dist.name}: {dist.value}")


def run_package_layout_examples() -> None:
    """Demonstrate layout validation."""
    print("\n--- Package Layout Validation ---")

    repo_root = Path.cwd()
    layout = PackageLayout(root=repo_root, src_layout=False, package_name="core_python")
    status = validate_package_layout(layout)
    print(f"Checked repo layout for {layout.package_name}: {status}")


def main() -> None:
    """Main CLI entrypoint for packaging examples."""
    parser = argparse.ArgumentParser(description="Run Python packaging examples")
    parser.add_argument(
        "--module",
        choices=["metadata", "scripts", "layout", "all"],
        default="all",
        help="Specific module to run",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.module == "metadata":
        run_packaging_metadata_examples()
    elif args.module == "scripts":
        run_console_script_and_distribution_examples()
    elif args.module == "layout":
        run_package_layout_examples()
    else:
        run_packaging_metadata_examples()
        run_console_script_and_distribution_examples()
        run_package_layout_examples()


if __name__ == "__main__":
    main()
